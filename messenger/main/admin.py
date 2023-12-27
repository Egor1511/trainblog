from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import MyBlog, Category, Comment


@admin.register(MyBlog)
class BlogAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'photo', 'content', 'time_create',
              'time_update', 'read_counter', 'category', 'author',
              'is_published']
    list_display = ('title', 'slug', 'photo', 'content', 'time_create',
                    'time_update', 'read_counter', 'category', 'author',
                    'is_published')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ('is_published',)
    search_fields = ['title__startswith', 'category__name']
    list_filter = ['category__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, post: MyBlog):
        if post.photo:
            return mark_safe(f"<img src='{post.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=MyBlog.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=MyBlog.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!",
                          messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_date',
                    'approved_comment')
    list_display_links = ('post',)
    list_filter = ['approved_comment', 'created_date']
    search_fields = ['text']