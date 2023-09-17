from datetime import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import markdown
import re
from utils.generatorStr import pass_generator


# 文章关键词，用来作为SEO中keywords
class Keyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('文章关键词', max_length=20)

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('文章标签', max_length=20)
    slug = models.SlugField(unique=True, default="%s" % pass_generator(11))
    description = models.TextField('描述', max_length=240, default='标签描述', null=True, blank=True,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

    def get_article_list(self):
        """返回当前标签下所有发表的文章列表"""
        return Article.objects.filter(tags=self, is_publish=True)


# 文章分类
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('文章分类', max_length=20)
    slug = models.SlugField(unique=True, default="%s" % pass_generator(11))
    description = models.TextField('描述', max_length=240, default='分类描述', null=True, blank=True,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    # 浏览次数
    visitor = models.IntegerField(verbose_name="浏览次数", default=1, blank=True, null=True)
    sort_field = models.CharField(default='', verbose_name='排序方式', max_length=32, null=True, blank=True)
    is_top = models.BooleanField(verbose_name="是否置顶", default=False)
    # 文集权限说明：0表示公开，1表示私密,2表示指定用户可见, 3表示访问码可见 默认公开
    role = models.IntegerField(choices=((0, 0), (1, 1), (2, 2), (3, 3)), default=0, verbose_name="文集权限")
    role_value = models.TextField(verbose_name="文集权限值", blank=True, null=True)
    icon = models.CharField(verbose_name="文集图标", max_length=50, blank=True, null=True, default=None)

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self, is_publish=True)


# 文章
class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Category, verbose_name='文章分类_所属项目', on_delete=models.PROTECT)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.PROTECT)
    title = models.CharField(max_length=250, verbose_name='文章标题')
    summary = models.TextField('文章摘要', max_length=250, default='文章摘要等同于网页description内容，请务必填写...', null=True, blank=True)

    # 递归目录
    parent_doc = models.IntegerField(default=0, verbose_name="上级文档")
    sort = models.IntegerField(verbose_name='排序', default=9999)

    # 主体
    body = models.TextField(verbose_name='文章内容', null=True, blank=True)
    pre_content = models.TextField(verbose_name="编辑内容", null=True, blank=True)
    # 编辑器模式：1表示Editormd编辑器，2表示Vditor编辑器，3表示iceEditor编辑器  5: Tinymce富文本
    editor_mode = models.IntegerField(default=1, verbose_name='编辑器模式')

    img_link = ProcessedImageField(upload_to='article/upload/%Y/%m/%d/',
                                   default='article/default/default.png',
                                   verbose_name='封面图',
                                   processors=[ResizeToFill(250, 150)],
                                   null=True, blank=True,
                                   help_text='上传图片大小建议使用5:3的宽高比，为了清晰度原始图片宽度应该超过250px')

    views = models.IntegerField('阅览量', default=0, null=True, blank=True)
    slug = models.SlugField(unique=True, help_text='短网址', null=True, blank=True, default="%s" % pass_generator(11))
    is_top = models.BooleanField('置顶', default=False, null=True, blank=True)
    is_publish = models.BooleanField('是否发布', default=True, null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词', null=True, blank=True,
                                      help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    # 文档状态说明：0表示草稿状态，1表示发布状态，2表示删除状态
    status = models.IntegerField(choices=((0, 0), (1, 1)), default=1, verbose_name='文档状态')
    open_children = models.BooleanField(default=False, verbose_name="展开下级目录")
    show_children = models.BooleanField(default=False, verbose_name="显示下级文档")

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return f'{self.title[:30]}...' if len(self.title) > 30 else self.title

    def save(self, *args, **kwargs):
        # 当为更新且is_publish由False变更成True的时候才执行: 发布的文章时间的创建时间以发布时间为准
        if self.pk and self.is_publish and Article.objects.filter(pk=self.pk,
                                                                  is_publish=False).exists():
            self.create_date = datetime.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """优先使用专题地址"""
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_subject_absolute_url(self):
        """获取专栏地址"""
        return reverse('blog:subject_detail', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id, is_publish=True).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id, is_publish=True).order_by('id').first()

    def get_topic_title(self):
        return self.title


# 时间线
class Timeline(models.Model):
    COLOR_CHOICE = (
        ('primary', '基本-蓝色'),
        ('success', '成功-绿色'),
        ('info', '信息-天蓝色'),
        ('warning', '警告-橙色'),
        ('danger', '危险-红色')
    )
    SIDE_CHOICE = (
        ('L', '左边'),
        ('R', '右边'),
    )
    STAR_NUM = (
        (1, '1颗星'),
        (2, '2颗星'),
        (3, '3颗星'),
        (4, '4颗星'),
        (5, '5颗星'),
    )
    id = models.BigAutoField(primary_key=True)
    side = models.CharField('位置', max_length=1, choices=SIDE_CHOICE, default='L')
    star_num = models.IntegerField('星星个数', choices=STAR_NUM, default=3)
    icon = models.CharField('图标', max_length=50, default='fa fa-pencil')
    icon_color = models.CharField('图标颜色', max_length=20, choices=COLOR_CHOICE, default='info')
    title = models.CharField('标题', max_length=100)
    update_date = models.DateTimeField('更新时间')
    content = models.TextField('主要内容')

    class Meta:
        verbose_name = '时间线'
        verbose_name_plural = verbose_name
        ordering = ['-update_date']

    def __str__(self):
        return self.title[:20]

    def content_to_markdown(self):
        """支持markdown，但是没必要用，content直接用html写更好"""
        return markdown.markdown(self.content,
                                 extensions=['markdown.extensions.extra', ])


# 幻灯片
class Carousel(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.IntegerField('编号', help_text='编号决定图片播放的顺序，图片不要多于5张')
    title = models.CharField('标题', max_length=20, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=80)
    img_url = models.CharField('图片地址', max_length=200)
    url = models.CharField('跳转链接', max_length=200, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]


# 死链
class Silian(models.Model):
    id = models.BigAutoField(primary_key=True)
    badurl = models.CharField('死链地址', max_length=200, help_text='注意：地址是以http开头的完整链接格式')
    remark = models.CharField('死链说明', max_length=50, blank=True, null=True)
    add_date = models.DateTimeField('提交日期', auto_now_add=True)

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '死链'
        verbose_name_plural = verbose_name
        ordering = ['-add_date']

    def __str__(self):
        return self.badurl


class FriendLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('网站名称', max_length=50)
    description = models.CharField('网站描述', max_length=100, null=True, blank=True)
    link = models.URLField('友链地址', help_text='请填写http或https开头的完整形式地址', null=True, blank=True)
    logo = ProcessedImageField(upload_to='friend/upload/%Y',
                               default='friend/default/default.png',
                               verbose_name='网站LOGO',
                               processors=[ResizeToFill(120, 120)],
                               null=True, blank=True,
                               help_text='上传图片大小建议120x120以上，使用友联域名命名，如tendcode.com.png')

    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否展示', default=False)
    not_show_reason = models.CharField('禁用原因', max_length=50, blank=True, null=True)

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        """提取友链的主页"""
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])


class AboutBlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    body = models.TextField(verbose_name='About 内容')

    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'About'

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
