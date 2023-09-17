import os, sys, datetime
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('ZONE_BLOG_SECRET_KEY', '#!kta!9e0)24d@9#=*=ra$r!0k0+p5@w+a%7g1bbof9+ad@4_(')

# 是否开启[在线工具]应用
TOOL_FLAG = os.getenv('ZONE_BLOG_TOOL_FLAG', 'True').upper() == 'TRUE'
# 是否开启[API]应用
API_FLAG = os.getenv('ZONE_BLOG_API_FLAG', 'False').upper() == 'TRUE'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv('ZONE_BLOG_DEBUG', 'True').upper() == 'TRUE'
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

# 添加了新的app需要重启服务器
INSTALLED_APPS = [
    # 'bootstrap_admin',  # 注册bootstrap后台管理界面,这个必须放在最前面
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # 添加人性化过滤器
    'django.contrib.sitemaps',  # 网站地图

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'django.contrib.sites',  # 这个是自带的，会创建一个sites表，用来存放域名
    'rest_framework',
    'django_tctip',

    'crispy_forms',  # bootstrap表单样式
    'imagekit',  # 上传图片的应用
    'haystack',  # 全文搜索应用 这个要放在其他应用之前

    # 'webstack',  # 导航应用

    'apps.blog',     # 博客应用
    'apps.tool',     # 工具
    'apps.comment',  # 评论
    'apps.resume',   # 个人简历
    'apps.oauth',    # 自定义用户应用
    'apps.system_app'  # 系统应用
]

# 自定义用户model
AUTH_USER_MODEL = 'oauth.Ouser'

# 自动主键
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# allauth配置
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# allauth需要的配置
# 当出现"SocialApp matching query does not exist"这种报错的时候就需要更换这个ID
SITE_ID = 2

# 设置登录和注册成功后重定向的页面，默认是/accounts/profile/
LOGIN_REDIRECT_URL = "/"

# Email setting
# 注册中邮件验证方法:“强制（mandatory）”,“可选（optional）【默认】”或“否（none）”之一。
# 开启邮箱验证的话，如果邮箱配置不可用会报错，所以默认关闭，根据需要自行开启
ACCOUNT_EMAIL_VERIFICATION = os.getenv('ZONE_BLOG_ACCOUNT_EMAIL_VERIFICATION', 'none')
# 登录方式，选择用户名或者邮箱都能登录
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# 设置用户注册的时候必须填写邮箱地址
ACCOUNT_EMAIL_REQUIRED = True
# 登出直接退出，不用确认
ACCOUNT_LOGOUT_ON_GET = True

# 表单插件的配置
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'ZoneBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 设置视图
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.blog.context_processors.settings_info',  # 自定义上下文管理器
            ],
        },
    },
]

WSGI_APPLICATION = 'ZoneBlog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False  # 关闭国际时间，不然数据库报错

# 统一分页设置
BASE_PAGE_BY = 10
BASE_ORPHANS = 3

# *************************************** 静态文件配置开始 ***************************************
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# 静态文件收集
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# print("STATIC_ROOT: ", STATIC_ROOT)
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
    STATICFILES_DIR = os.path.join(BASE_DIR, 'static')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# 媒体文件收集
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# *************************************** 静态文件配置结束 ***************************************


# *************************************** 全文配置开始 ***************************************
# 全文搜索应用配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',  # 选择语言解析器为自己更换的结巴分词
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),  # 保存索引文件的地址，选择主目录下，这个会自动生成
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# *************************************** 全文配置结束 ***************************************


# ************************************* restframework配置开始 **********************************
# restframework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}
# ********************************** restframework配置开始 ************************************


# *************************************** 数据库配置开始 ***************************************
# 配置数据库
zone_blog_mysql_host = os.getenv('ZONE_BLOG_MYSQL_HOST', '127.0.0.1')
zone_blog_mysql_name = os.getenv('ZONE_BLOG_MYSQL_NAME', 'ZoneBlog')
zone_blog_mysql_user = os.getenv('ZONE_BLOG_MYSQL_USER', 'root')
zone_blog_mysql_pwd = os.getenv('ZONE_BLOG_MYSQL_PWD', 'python')
zone_blog_mysql_port = os.getenv('ZONE_BLOG_MYSQL_PORT', 3306)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 修改数据库为MySQL，并进行配置
        'NAME': zone_blog_mysql_name,
        'USER': zone_blog_mysql_user,
        'PASSWORD': zone_blog_mysql_pwd,
        'HOST': zone_blog_mysql_host,
        'PORT': zone_blog_mysql_port,
        'OPTIONS': {'charset': 'utf8mb4', 'use_unicode': True}
    }
}
# *************************************** 数据库配置结束 **************************************


# *************************************** 缓存配置开始 ***************************************
# 使用django-redis缓存页面，缓存配置如下：
zoneBlog_redis_host = os.getenv('ZONE_BLOG_REDIS_HOST', '127.0.0.1')
zoneBlog_redis_port = os.getenv('ZONE_BLOG_REDIS_PORT', 6379)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/0".format(zoneBlog_redis_host, zoneBlog_redis_port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# *************************************** 缓存配置结束 ***************************************


# ****************************************** 邮箱配置开始 ****************************************
# 配置管理邮箱，服务出现故障会收到到邮件，环境变量值的格式：name|test@test.com 多组用户用英文逗号隔开
ADMINS = []
admin_email_user = os.getenv('ZONE_BLOG_ADMIN_EMAIL_USER')
if admin_email_user:
    for each in admin_email_user.split(','):
        a_user, a_email = each.split('|')
        ADMINS.append((a_user, a_email))

# 邮箱配置
EMAIL_HOST = os.getenv('ZONE_BLOG_EMAIL_HOST', 'smtp.163.com')
EMAIL_HOST_USER = os.getenv('ZONE_BLOG_EMAIL_HOST_USER', 'your-email-address')
EMAIL_HOST_PASSWORD = os.getenv('ZONE_BLOG_EMAIL_HOST_PASSWORD',
                                'your-email-password')  # 这个不是邮箱密码，而是授权码
EMAIL_PORT = os.getenv('ZONE_BLOG_EMAIL_PORT', 465)  # 由于阿里云的25端口打不开，所以必须使用SSL然后改用465端口
EMAIL_TIMEOUT = 5
# 是否使用了SSL 或者TLS，为了用465端口，要使用这个
EMAIL_USE_SSL = os.getenv('ZONE_BLOG_EMAIL_USE_SSL', 'True').upper() == 'TRUE'
# 默认发件人，不设置的话django默认使用的webmaster@localhost，所以要设置成自己可用的邮箱
DEFAULT_FROM_EMAIL = os.getenv('ZONE_BLOG_DEFAULT_FROM_EMAIL', 'TendCode博客 <your-email-address>')
# *************************************** 邮箱配置结束 *******************************************


# ***************************************** 网站配置开始 ****************************************
# 网站默认设置和上下文信息
SITE_LOGO_NAME = os.getenv('ZONE_BLOG_LOGO_NAME', 'ZoneBlog')
SITE_END_TITLE = os.getenv('ZONE_BLOG_SITE_END_TITLE', 'ZoneBlog')
SITE_DESCRIPTION = os.getenv('ZONE_BLOG_SITE_DESCRIPTION', 'ZoneBlog 是一个使用 Django+Bootstrap4 搭建的个人博客类型网站')
SITE_KEYWORDS = os.getenv('ZONE_BLOG_SITE_KEYWORDS', 'ZoneBlog,Django博客,个人博客')
# ***************************************** 网站配置结束 *****************************************


# ***************************************** 个性化配置开始 ****************************************
# 个性化设置，非必要信息
# 网站部署日期
SITE_CREATE_DATE = os.getenv('ZONE_BLOG_SITE_CREATE_DATE', '2023-01-01')
# 个人 Github 地址
MY_GITHUB = os.getenv('ZONE_BLOG_GITHUB', 'https://github.com/Hopetree')
# 工信部备案信息
BEIAN = os.getenv('ZONE_BLOG_BEIAN', '网站备案信息')
# 站长统计（友盟）
CNZZ_PROTOCOL = os.getenv('ZONE_BLOG_CNZZ_PROTOCOL', '')
# 站长统计（51.la）
LA51_PROTOCOL = os.getenv('ZONE_BLOG_LA51_PROTOCOL', '')
# 站长推送
MY_SITE_VERIFICATION = os.getenv('ZONE_BLOG_SITE_VERIFICATION', '')
# 使用 http 还是 https （sitemap 中的链接可以体现出来）
PROTOCOL_HTTPS = os.getenv('ZONE_BLOG_PROTOCOL_HTTPS', 'HTTP').lower()
# 个人外链信息（导航栏下拉中显示）
PRIVATE_LINKS = os.getenv('ZONE_BLOG_PRIVATE_LINKS', '[]')
# ***************************************** 个性化配置结束 ****************************************


# ****************************************** 日志配置开始 *****************************************
this_day = datetime.datetime.now().date().day
this_month = datetime.datetime.now().date().month
this_year = datetime.datetime.now().date().year

y_m_d = "%s_%s_%s" % (this_year, this_month, this_day)

# 创建存储日志文件的文件夹
linux_path = os.path.join(os.path.join(BASE_DIR, "logs"), "%s_%s" % (this_year, this_month))  # 路径替换
linux_path = os.path.join(linux_path, "%s" % this_day)

if os.path.exists(linux_path) is False:
    os.makedirs(linux_path)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/debug_{}m.log'.format(linux_path, y_m_d),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 10,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/info_{}m.log'.format(linux_path, y_m_d),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 10,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
            'encoding': 'utf-8'
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/warning_{}m.log'.format(linux_path, y_m_d),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
            'encoding': 'utf-8'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/error_{}m.log'.format(linux_path, y_m_d),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'self_logger': {
            'handlers': ['console', 'debug', 'info', 'warning', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}
# ****************************************** 日志配置结束 *****************************************
