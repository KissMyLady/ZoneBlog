from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView

from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap
from apps.blog.feeds import AllArticleRssFeed
from apps.blog.views import robots
from django.views.static import serve

# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),  # Django自带后台

    path('favicon.ico', RedirectView.as_view(url='/static/blog/img/favicon.ico')),

    path('accounts/', include('allauth.urls')),  # allauth
    # path('adminx/',     admin.site.urls),
    path('accounts/', include(('oauth.urls', 'apps.oauth'), namespace='oauth')),
    # path('account_logout/', account_logout, name='account_logout'),
    # oauth,只展现一个用户登录界面

    path('comment/', include(('comment.urls', 'apps.comment'), namespace='comment')),

    # comment
    path('robots.txt', robots, name='robots'),  # robots
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # 网站地图
    path('feed/', AllArticleRssFeed(), name='rss'),  # rss订阅
    path('resume/', include(('resume.urls', 'apps.resume'), namespace='resume')),  # 个人简历
    # path('nav/', include(('webstack.urls', 'webstack'), namespace='webstack')),

    # 兜底项目
    path('', include(('blog.urls', 'apps.blog'), namespace='blog')),  # blog

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件

# 是否开启[API]应用  restframework
if settings.API_FLAG:
    from apps.api.urls import router
    urlpatterns.append(path('api/v1/', include((router.urls, router.root_view_name), namespace='api')))

# 是否开启[在线工具]应用
if settings.TOOL_FLAG:
    urlpatterns.append(path('tool/', include(('tool.urls', 'tool'), namespace='tool')))

# Debug模式下, 使用django的静态文件服务
if settings.DEBUG:
    s_path = re_path('^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIR})
    m_path = re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})

    # 静态路径
    urlpatterns.insert(0, s_path)
    urlpatterns.insert(0, m_path)

    # 静态服务
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# else:
# web模式下, 使用nginx提供 media, statis服务
