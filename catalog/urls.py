from django.urls import path, re_path
from . import views

# 在設定重新導向到這裡的時候，可以在這裡定義更加細項的東西
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # path('books/<int:pk>', views.BookListView.as_view(), name='bool-detail'),
    # 下面對應model中Book所擁有的method，就是get_absolute_path 取得絕對路徑中的reverse 第一個參數 也就是在這裡定義 name = book-detail
    # 反向器(URL mapping)才可以知道 怎麼去將完整路徑兜出來
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/', views.getAuthors, name='authors')
]