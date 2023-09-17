from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Ouser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    link = models.URLField('个人网址', blank=True, help_text='提示：网址必须填写以http开头的完整形式')
    avatar = ProcessedImageField(upload_to='avatar/upload/%Y/%m/%d/%H-%M-%S',
                                 default='avatar/default/default.png',
                                 verbose_name='头像',
                                 processors=[ResizeToFill(80, 80)])
    note = models.TextField(verbose_name="备注信息", null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username


# 用户选项配置
class UserOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Ouser, on_delete=models.CASCADE)
    # 用户配置的编辑器选项，1表示Editormd编辑器，2表示Vditor编辑器，默认为1
    # editor_mode = models.IntegerField(default=1, verbose_name="编辑器选项")

    u_key = models.CharField(verbose_name="key", max_length=255, default="")
    u_value = models.CharField(verbose_name="value", max_length=255, default="", blank=True, null=True)
    note = models.TextField(verbose_name="备注项目", default="", blank=True, null=True)
    is_delete = models.BooleanField(default=False, null=True, blank=True, verbose_name="删除")
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='修改时间')

    class Meta:
        db_table = 'user_options'
        verbose_name = '用户设置'
        verbose_name_plural = verbose_name
