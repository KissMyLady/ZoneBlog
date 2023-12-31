# Generated by Django 4.2.4 on 2023-09-17 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('content', models.TextField(verbose_name='评论内容')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(blank=True, default=False, null=True, verbose_name='删除标记')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
                'ordering': ['create_date'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='提示时间')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(blank=True, default=False, null=True, verbose_name='删除标记')),
            ],
            options={
                'verbose_name': '提示信息',
                'verbose_name_plural': '提示信息',
                'ordering': ['-create_date'],
            },
        ),
        migrations.CreateModel(
            name='SystemNotification',
            fields=[
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='推送时间')),
                ('update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(blank=True, default=False, null=True, verbose_name='删除标记')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('content', models.TextField(help_text='支持html格式的内容', verbose_name='通知内容')),
            ],
            options={
                'verbose_name': '系统通知',
                'verbose_name_plural': '系统通知',
                'ordering': ['-create_date'],
            },
        ),
    ]
