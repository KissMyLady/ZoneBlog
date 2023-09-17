from django import template
from markdown.extensions.toc import TocExtension  # 锚点的拓展
from markdown.extensions.codehilite import CodeHiliteExtension
from apps.blog.utils import CustomHtmlFormatter
from apps.comment.models import emoji_info
from django.utils.text import slugify
import markdown

# 创建了新的tags标签文件后必须重启服务器
register = template.Library()


@register.simple_tag
def get_comment_count(entry):
    """获取一个文章的评论总数"""
    lis = entry.article_comments.all()
    return lis.count()


@register.simple_tag
def get_parent_comments(entry):
    """获取一个文章的父评论列表，逆序只选取后面的20个评论"""
    lis = entry.article_comments.filter(parent=None).order_by("-id")[:20]
    return lis


@register.simple_tag
def get_child_comments(com):
    """获取一个父评论的子平路列表"""
    lis = com.articlecomment_child_comments.all()
    return lis


@register.simple_tag
def get_comment_user_count(entry):
    """获取评论人总数"""
    p = []
    lis = entry.article_comments.all()
    for each in lis:
        if each.author not in p:
            p.append(each.author)
    return len(p)


@register.simple_tag
def get_notifications(user, f=None):
    """获取一个用户的对应条件下的提示信息"""
    if f == 'true':
        # 获取所有已读通知
        lis = []
        lis.extend(user.notification_get.filter(is_read=True))
        lis.extend(user.systemnotification_recipient.filter(is_read=True))
    elif f == 'false':
        # 获取所有未读通知
        lis = []
        lis.extend(user.notification_get.filter(is_read=False))
        lis.extend(user.systemnotification_recipient.filter(is_read=False))
    else:
        # 获取所有通知
        lis = []
        lis.extend(user.notification_get.all())
        lis.extend(user.systemnotification_recipient.all())

    # 按照 create_date 字段进行汇总后重新排序
    lis = sorted(lis, key=lambda x: x.create_date, reverse=True)
    return lis[:50]


@register.simple_tag
def get_notifications_count(user, f=None):
    """获取一个用户的对应条件下的提示信息总数"""
    if f == 'true':
        num = 0
        num += user.notification_get.filter(is_read=True).count()
        num += user.systemnotification_recipient.filter(is_read=True).count()
    elif f == 'false':
        num = 0
        num += user.notification_get.filter(is_read=False).count()
        num += user.systemnotification_recipient.filter(is_read=False).count()
    else:
        num = 0
        num += user.notification_get.all().count()
        num += user.systemnotification_recipient.all().count()
    return num


@register.simple_tag
def get_emoji_imgs():
    """
    返回一个列表，包含表情信息
    :return:
    """
    return emoji_info


@register.filter(is_safe=True)
def emoji_to_url(value):
    """
    将emoji表情的名称转换成图片地址
    """
    emoji_static_url = 'comment/weibo/{}.png'
    return emoji_static_url.format(value)


emoji_list = [
    ('aini_org', '爱你'),
    ('baibai_thumb', '拜拜'),
    ('baobao_thumb', '抱抱'),
    ('beishang_org', '悲伤'),
    ('bingbujiandan_thumb', '并不简单'),
    ('bishi_org', '鄙视'),
    ('bizui_org', '闭嘴'),
    ('chanzui_org', '馋嘴'),
    ('chigua_thumb', '吃瓜'),
    ('chongjing_org', '憧憬'),
    ('dahaqian_org', '哈欠'),
    ('dalian_org', '打脸'),
    ('ding_org', '顶'),
    ('doge02_org', 'doge'),
    ('erha_org', '二哈'),
    ('gui_org', '跪了'),
    ('guzhang_thumb', '鼓掌'),
    ('haha_thumb', '哈哈'),
    ('heng_thumb', '哼'),
    ('huaixiao_org', '坏笑'),
    ('huaxin_org', '色'),
    ('jiyan_org', '挤眼'),
    ('kelian_org', '可怜'),
    ('kuxiao_org', '允悲'),
    ('ku_org', '酷'),
    ('leimu_org', '泪'),
    ('miaomiao_thumb', '喵喵'),
    ('ningwen_org', '疑问'),
    ('nu_thumb', '怒'),
    ('qian_thumb', '钱'),
    ('sikao_org', '思考'),
    ('taikaixin_org', '太开心'),
    ('tanshou_org', '摊手'),
    ('tianping_thumb', '舔屏'),
    ('touxiao_org', '偷笑'),
    ('tu_org', '吐'),
    ('wabi_thumb', '挖鼻'),
    ('weiqu_thumb', '委屈'),
    ('wenhao_thumb', '费解'),
    ('wosuanle_thumb', '酸'),
    ('wu_thumb', '污'),
    ('xiaoerbuyu_org', '笑而不语'),
    ('xiaoku_thumb', '笑cry'),
    ('xixi_thumb', '嘻嘻'),
    ('yinxian_org', '阴险'),
    ('yun_thumb', '晕'),
    ('zhouma_thumb', '怒骂'),
    ('zhuakuang_org', '抓狂')
]


@register.simple_tag
def content_to_markdown(content):
    # 表情符号转换
    # <img src="/static/comment/weibo/chanzui_org.png" title="馋嘴" alt="chanzui_org" data-emoji=":chanzui_org:">

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown_checklist.extension',
        CodeHiliteExtension(pygments_formatter=CustomHtmlFormatter),
        TocExtension(slugify=slugify),
    ])
    body = md.convert(content)

    # 图片表情符号替换
    for emoji in emoji_list:
        emoji_code = emoji[0]
        emoji_zh = emoji[1]
        if body.__contains__(":%s:" % emoji_code):
            template_html = '<img src="/static/comment/weibo/%s.png" title="%s" alt="%s"">' % (
            emoji_code, emoji_zh, emoji_zh)
            body = body.replace(":%s:" % emoji_code, template_html)
        pass

    # toc = md.toc
    return body
