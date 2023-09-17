# ZoneBlog

一个以 Django 作为框架搭建的个人博客。



1, 启动命令如下
```shell
pip install -r requirements.txt

python manage.py makemigrations 
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8900
```

2, 收集静态文件
```bash
python manage.py collectstatic --noinput
python manage.py compress --force
```

3, uwsgi配置启动
```bash
uwsgi --ini uwsgi.ini
# 停止
uwsgi --stop uwsgi.pid
# 查看进程
pss uwsgi
killall -s INT uwsgi
```

## 鸣谢: 站在巨人的肩膀上

- 博客效果： https://tendcode.com/
- 源项目地址: https://github.com/Hopetree/izone

