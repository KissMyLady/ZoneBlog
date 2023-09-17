from django.db.models import Count, Q
from django.http import Http404, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, reverse
from django.utils.text import slugify
from django.views import generic
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.core.cache import cache

from apps.blog.models import Article, Tag, Category, Timeline, Silian, AboutBlog, FriendLink
from apps.blog.utils import site_full_url, CustomHtmlFormatter, ApiResponse, ErrorApiResponse

import markdown
from markdown.extensions.toc import TocExtension  # 锚点的拓展
from markdown.extensions.codehilite import CodeHiliteExtension
import time

from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet


def test_page_view(request):
    return render(request, 'test.html')


class ArchiveView(generic.ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'articles'
    paginate_by = 200
    paginate_orphans = 50

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(is_publish=True)


class IndexView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        # url参数中可以传排序参数
        sort = self.request.GET.get('sort')
        if sort == 'views':
            return '-views', '-update_date', '-id'
        return '-is_top', '-create_date'

    def get_queryset(self, **kwargs):
        queryset = super(IndexView, self).get_queryset().filter(is_publish=True)
        sort = self.request.GET.get('sort')
        if sort == 'comment':
            queryset = queryset.annotate(com=Count('article_comments')).order_by('-com', '-views')
        return queryset


class DetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    # slug_field = 'id'  # 通过id查询
    slug_url_kwarg = 'slug'  # 通过slug查询

    def get_queryset(self):
        # 普通用户只能看发布的文章，作者和管理员可以看到未发布的
        queryset = super().get_queryset()
        # 非登录用户可以访问全部发布的文章
        if not self.request.user.is_authenticated:
            return queryset.filter(is_publish=True, is_delete=False)
        # 超级管理员访问所有
        if self.request.user.is_superuser:
            return queryset.filter(is_delete=False)
        # 登录用户访问所有发布和自己的未发布
        return queryset.filter(Q(author=self.request.user) | Q(is_publish=True, is_delete=False))

    def get_object(self, queryset=None):
        obj = super().get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = self.context_object_name + ':read:{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if u == obj.author or u.is_superuser:
            pass
        else:
            if not is_read_time:
                obj.update_views()
                ses[the_key] = time.time()
            else:
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:
                    obj.update_views()
                    ses[the_key] = time.time()
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = self.context_object_name + ':markdown:{}:{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md and settings.DEBUG is False:
            obj.body, obj.toc = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown_checklist.extension',
                CodeHiliteExtension(pygments_formatter=CustomHtmlFormatter),
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            cache.set(md_key, (obj.body, obj.toc), 3600 * 24 * 7)
        return obj


class SubjectDetailView(DetailView):
    """
    专题文章视图
    """
    template_name = 'blog/subjectDetail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(topic__isnull=False)


class CategoryView(generic.ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(CategoryView, self).get_ordering()
        # url参数中可以传排序参数
        sort = self.request.GET.get('sort')
        if sort == 'views':
            return '-views', '-update_date', '-id'
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate, is_publish=True)

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate
        return context_data


class TagView(generic.ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(TagView, self).get_ordering()
        # url参数中可以传排序参数
        sort = self.request.GET.get('sort')
        if sort == 'views':
            return '-views', '-update_date', '-id'
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(TagView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag, is_publish=True)

    def get_context_data(self, **kwargs):
        context_data = super(TagView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章标签'
        context_data['search_instance'] = tag
        return context_data


def AboutView(request):
    obj = AboutBlog.objects.first()
    if obj:
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = 'about:markdown:{}:{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md and settings.DEBUG is False:
            body = cache_md
        else:
            body = obj.body_to_markdown()
            cache.set(md_key, body, 3600 * 24 * 15)
    else:
        repo_url = 'https://github.com/Hopetree'
        body = '<li>作者 Github 地址：<a href="{}">{}</a></li>'.format(repo_url, repo_url)
    return render(request, 'blog/about.html', context={'body': body})


class TimelineView(generic.ListView):
    model = Timeline
    template_name = 'blog/timeline.html'
    context_object_name = 'timeline_list'

    def get_ordering(self):
        return '-update_date',


class SilianView(generic.ListView):
    model = Silian
    template_name = 'blog/silian.xml'
    context_object_name = 'badurls'


class FriendLinkView(generic.ListView):
    model = FriendLink
    template_name = 'blog/friend.html'
    context_object_name = 'friend_list'

    def get_queryset(self):
        queryset = super(FriendLinkView, self).get_queryset()
        return queryset.filter(is_show=True, is_active=True)


# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    template_name = 'search/blog/search.html'
    context_object_name = 'search_list'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    queryset = SearchQuerySet().order_by('-views').filter(is_publish=True)


def robots(request):
    site_url = site_full_url()
    return render(request, 'robots.txt', context={'site_url': site_url}, content_type='text/plain')


class DetailEditView(generic.DetailView):
    """
    文章编辑视图
    """
    model = Article
    template_name = 'blog/articleEdit.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super(DetailEditView, self).get_object()
        # 非作者及超管无权访问
        if not self.request.user.is_superuser and obj.author != self.request.user:
            raise Http404('Invalid request.')
        return obj


@require_http_methods(["POST"])
def update_article(request):
    """更新文章，仅管理员和作者可以更新"""
    if request.method == 'POST':
        article_slug = request.POST.get('article_slug')
        article_body = request.POST.get('article_body')
        article_img_link = request.POST.get('article_img_link')
        change_img_link_flag = request.POST.get('change_img_link_flag')

        try:
            article = Article.objects.get(slug=article_slug)
            # 检查当前用户是否是作者
            if not request.user.is_superuser and article.author != request.user:
                return HttpResponseForbidden("You don't have permission to update this article.")

            # 更新article模型的数据
            article.body = article_body
            if change_img_link_flag == 'true':
                article.img_link = article_img_link  # 更新封面图地址
            article.save()  # 这里不要设置更新的字段，不然会导致其他要在save更新的字段不更新

            callback = article.get_absolute_url()
            response_data = {'message': 'Success', 'data': {'callback': callback}, 'code': 0}
            return JsonResponse(response_data)
        except Article.DoesNotExist:
            return HttpResponseBadRequest("Article not found.")
    return HttpResponseBadRequest("Invalid request.")


def friend_add(request):
    """
    申请友链
    @param request:
    @return:
    """
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        description = data.get('description')
        link = data.get('link')

        try:
            friend = FriendLink.objects.create(name=name,
                                               description=description,
                                               link=link,
                                               is_active=False,
                                               is_show=True,
                                               )
            resp = ApiResponse()
            resp.data = {'id': friend.id}
            return resp.as_json_response()
        except Exception as e:
            resp = ErrorApiResponse()
            resp.error = str(e)
            return resp.as_json_response()

    return render(request, 'blog/friendAdd.html')