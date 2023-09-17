from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from utils.generatorStr import pass_generator


class ResumeTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('模板名称', max_length=20)
    description = models.TextField('描述', max_length=240)
    content = models.TextField('css内容')

    create_date = models.DateTimeField(verbose_name='推送时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '简历模板'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 个人简历
class Resume(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者',
                               on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='简历标题')
    body = models.TextField(verbose_name='简历内容')
    slug = models.SlugField('访问地址', unique=True, default="%s" % pass_generator(11))
    is_open = models.BooleanField('是否公开', default=False)

    template = models.ForeignKey(ResumeTemplate, verbose_name='简历模板', on_delete=models.PROTECT)

    create_date = models.DateTimeField(verbose_name='推送时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '个人简历'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        if len(self.title) > 20:
            return self.title[:20] + '...'
        return self.title

    def get_absolute_url(self):
        return reverse('resume:detail', kwargs={'slug': self.slug})
