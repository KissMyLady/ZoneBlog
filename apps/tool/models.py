from django.db import models


class ToolCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('网站分类名称', max_length=20)
    order_num = models.IntegerField('序号', default=99, help_text='序号可以用来调整顺序，越小越靠前')
    icon = models.CharField('图标', max_length=50, blank=True, null=True, default='fa fa-link')

    create_date = models.DateTimeField(verbose_name='推送时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '工具分类'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name


class ToolLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('网站名称', max_length=20)
    description = models.CharField('网站描述', max_length=100, null=True, blank=True)
    link = models.URLField('网站链接', null=True, blank=True)
    order_num = models.IntegerField('序号', default=99,
                                    help_text='序号可以用来调整顺序，越小越靠前',
                                    null=True, blank=True)
    category = models.ForeignKey(ToolCategory, verbose_name='网站分类', blank=True, null=True,
                                 on_delete=models.SET_NULL)

    create_date = models.DateTimeField(verbose_name='推送时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True, null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        verbose_name = '推荐工具'
        verbose_name_plural = verbose_name
        ordering = ['order_num', 'id']

    def __str__(self):
        return self.name
