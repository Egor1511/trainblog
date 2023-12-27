import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AddPostForm, CommentForm, SearchForm
from .models import MyBlog, Comment
from .utils import DataMixin

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class ShowBlog(DataMixin, ListView):
    template_name = 'main/blog.html'
    context_object_name = 'posts'
    title_page = "Блог"

    def get_queryset(self):
        return MyBlog.published.all()


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'main/addpage.html'
    title_page = 'Добавление статьи'
    model = MyBlog

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'post_slug': self.object.slug})


def index(request):
    return render(request, 'main/index.html', {'title': "Главная страница"})


class ShowPost(DataMixin, DetailView):
    template_name = 'main/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_views = r.incr(f'image:{self.kwargs[self.slug_url_kwarg]}:views')
        context['total_views'] = total_views
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(MyBlog.published, slug=self.kwargs[self.slug_url_kwarg])

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        author = MyBlog.published.author.filter(slug=self.kwargs[self.slug_url_kwarg])
        comment_form = CommentForm(request.POST)
        comments_author = Comment.objects.comments.filter(slug=self.kwargs[self.slug_url_kwarg])
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = self.request.user
            comment.save()
            comment_form = CommentForm()

        return render(request, self.template_name, {
            'post': post,
            'comment_form': comment_form,
            'author': author,
            'comments': comments_author
        })

    def delete_comment(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.author == self.request.user:
            comment.delete()

        return redirect('post', post_slug=comment.post.slug)


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = MyBlog.objects.get(pk=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except MyBlog.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


class ShowCategory(DataMixin, ListView):
    template_name = 'main/blog.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return MyBlog.published.filter(category__slug=self.kwargs['category_slug']).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context,
                                      title='Категория - ' + category.name,
                                      category_selected=category.pk,
                                      )


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = MyBlog
    fields = ['title', 'content', 'photo', 'category']
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'main.change_myblog'


def post_search(request):
    form = SearchForm(request.GET)
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = MyBlog.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
            return render(request,
                          'blog/post/search.html',
                          {'form': form,
                           'query': query,
                           'results': results})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
