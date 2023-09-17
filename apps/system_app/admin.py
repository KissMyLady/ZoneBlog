from django.contrib import admin
from .models import SysSetting


# Register your models here.


# 系统设置项模型
@admin.register(SysSetting)
class Admin_SysSetting(admin.ModelAdmin):
    list_display = ["name", "value", "types",
                    "truncated_field",
                    "is_delete", "create_time"
                    ]
    list_per_page = 20
    ordering = ["-create_time"]

    # 直接编辑
    # list_editable = ("is_delete", )
    # select选中后, 批量更新
    @admin.action(description='取消逻辑删除')
    def switch_to_noDelete(self, request, queryset):
        queryset.update(is_delete=False)

    @admin.action(description='逻辑删除')
    def switch_to_delete(self, request, queryset):
        queryset.update(is_delete=True)

    @admin.action(description='直接删除')
    def warn_delete(self, request, queryset):
        queryset.delete()

    actions = [switch_to_noDelete, switch_to_delete]

    def truncated_field(self, obj):
        # 在这里定义截断字段的逻辑
        max_length = 20  # 设置最大长度为20个字符
        field_value = getattr(obj, 'note')  # 将 'your_field_name' 替换为实际的字段名
        if field_value is not None:
            if len(field_value) > max_length:
                return field_value[:max_length] + '...'  # 如果超过最大长度，则截断并添加省略号
            return field_value
        else:
            return field_value

    truncated_field.short_description = '备注'  # 修改字段名称
