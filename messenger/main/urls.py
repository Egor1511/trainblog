from django.urls import path

from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    path('', views.index, name='home'),
    path('blog/', views.ShowBlog.as_view(), name='blog'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(),
         name='edit_page'),
    path('category/<slug:category_slug>/', views.ShowCategory.as_view(),
         name='category'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/delete_comment/', views.ShowPost.as_view(),
         name='delete_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('like/', views.post_like, name='like'),
    path('search/', views.post_search, name='post_search'),

]
