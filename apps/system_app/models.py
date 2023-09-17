from django.db import models
from apps.oauth.models import Ouser


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name='删除标记', null=True, blank=True)

    class Meta:
        abstract = True


# 系统设置项模型
class SysSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name="项目", max_length=50, unique=True)
    value = models.TextField(verbose_name="内容", null=True, blank=True)
    types = models.CharField(verbose_name="类型", max_length=10, default="basic")

    note = models.TextField(verbose_name="备注", null=True, blank=True)
    is_delete = models.BooleanField(default=False, null=True, blank=True, verbose_name="删除")
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='修改时间')

    class Meta:
        db_table = 'sys_setting'
        verbose_name = '系统设置'
        verbose_name_plural = verbose_name
        ordering = ["-create_time", "name"]


# 日志表
class SysLogsModel(models.Model):
    log_type = models.CharField(max_length=32, null=True, blank=True)
    log_level = models.CharField(max_length=8, null=True, blank=True, default='info')
    log_title = models.CharField(max_length=255, null=True, blank=True)

    req_ip = models.CharField(max_length=64, null=True, blank=True, verbose_name='操作IP')
    req_address = models.CharField(max_length=64, null=True, blank=True, verbose_name='地址')
    req_agent = models.CharField(max_length=512, null=True, blank=True)
    req_browser = models.CharField(max_length=255, null=True, blank=True)
    req_system = models.CharField(max_length=32, null=True, blank=True)
    req_url = models.CharField(max_length=255, null=True, blank=True)
    req_method = models.CharField(max_length=8, null=True, blank=True)
    req_params = models.TextField(null=True, blank=True, verbose_name='操作提交的数据')

    time_out = models.IntegerField(null=True, blank=True, verbose_name='执行时间')
    exception = models.TextField(null=True, blank=True, verbose_name='异常信息')
    create_by = models.CharField(max_length=255, null=True, blank=True, verbose_name='创建人')
    update_by = models.CharField(max_length=255, null=True, blank=True)

    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True, blank=True)

    class Meta:
        db_table = 'sys_logs'
        verbose_name = '系统-日志表'
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]


# 保存日志
def logInfo(params="", msg=""):
    data = SysLogsModel.objects.create(
        type=""
    )
    try:
        data.save()
    except Exception as e:
        pass
    pass


# 图片分组模型
class ImageGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Ouser, on_delete=models.CASCADE)
    group_name = models.CharField(verbose_name="图片分组", max_length=50, default="默认分组")

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'image_group'
        verbose_name = '图片分组'
        verbose_name_plural = verbose_name


# 图片模型
class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Ouser, on_delete=models.CASCADE)
    file_path = models.CharField(verbose_name="图片路径", max_length=250)
    file_name = models.CharField(verbose_name="图片名称", max_length=250, null=True, blank=True)
    group = models.ForeignKey(ImageGroup, on_delete=models.SET_NULL, null=True, verbose_name="图片分组")
    remark = models.CharField(verbose_name="图片备注", null=True, blank=True, max_length=250, default="图片描述")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'image'
        verbose_name = '素材图片'
        verbose_name_plural = verbose_name


# 附件模型
class Attachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=200, verbose_name="附件名", default='myFile_附件.zip')
    file_size = models.CharField(max_length=100, verbose_name="附件大小", blank=True, null=True)
    file_path = models.FileField(upload_to='attachment/%Y/%m/', verbose_name='附件')
    user = models.ForeignKey(Ouser, on_delete=models.CASCADE, )
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = 'attachment'
        verbose_name = '附件管理'
        verbose_name_plural = verbose_name
