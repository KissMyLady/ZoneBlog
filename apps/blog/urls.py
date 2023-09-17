# -*- coding: utf-8 -*-
from django.urls import path
from apps.blog.views import IndexView, DetailView, CategoryView, TagView, AboutView
from apps.blog.views import update_article, FriendLinkView, friend_add
from apps.blog.views import SilianView, MySearchView, ArchiveView, TimelineView, DetailEditView


urlpatterns = [

    # 文章
    path('article/<slug:slug>/', DetailView.as_view(), name='detail'),  # 文章内容页
    # path('article/<int:id>/',      DetailView.as_view(), name='detail'),  # 文章内容页
    path('article-edit/<slug:slug>/', DetailEditView.as_view(), name='article_edit'),  # 文章编辑
    path('article-update/', update_article, name='article_update'),  # 文章更新

    # 文章分类
    path('category', AboutView, name='categoryType'),  # 文章分类
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),  # 分类列表
    path('tag/<slug:slug>/', TagView.as_view(), name='tag'),

    # 导航页
    path('about/', AboutView, name='about'),  # About页面
    path('timeline/', TimelineView.as_view(), name='timeline'),  # timeline页面
    path('archive/', ArchiveView.as_view(), name='archive'),      # 归档页面
    path('search/', MySearchView.as_view(), name='search_view'),  # 全文搜索

    path('silian.xml', SilianView.as_view(content_type='application/xml'), name='silian'),  # 死链页面
    path('friend/', FriendLinkView.as_view(), name='friend'),  # 友情链接
    path('friend/add/', friend_add, name='friend_add'),  # 友情链接申请

    # 专题列表页
    path('subject/', friend_add, name='subject_index'),

    # 专题详情页
    path('subject/<int:pk>/', friend_add, name='subject_page'),

    # 专题文章内容页
    path('subject/article/<slug:slug>/', friend_add, name='subject_detail'),

    path('', IndexView.as_view(), name='index'),  # 主页，自然排序
]