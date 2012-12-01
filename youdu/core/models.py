# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
	user = models.OneToOneField(User, verbose_name=_(u'用户'), related_name="user_profile")
	email = models.EmailField(_(u"联系邮箱"), blank=True)
	phone = models.CharField(_(u'联系电话'), max_length=20, blank=True)
	self_intro = models.CharField(_(u'个人简介'), max_length=200, blank = True)
	avatar = models.CharField(_(u'个人头像'), max_length=200, blank=True)
	small_avatar = models.CharField(_(u'个人小头像'), max_length=200, blank=True)
	modify_at = models.DateTimeField(auto_now = True)

EVENT_TYPES = (
    (u'讲座', u'讲座'),
    (u'讨论会/沙龙', u'讨论会/沙龙'),
    (u'宣讲会', u'宣讲会'),
)
class Event(models.Model):
	user_post = models.ForeignKey(User, verbose_name=_(u'发布人'))
	type = models.CharField(_(u'类型'), max_length=10)
	title = models.CharField(_(u'标题'), max_length=25)
	site = models.CharField(_(u'地点'), max_length=50)
	start_time = models.DateTimeField(_(u'开始时间'))
	create_at = models.DateTimeField(auto_now_add = True)
	modify_at = models.DateTimeField(auto_now = True)
	poster = models.ImageField(upload_to='posters/%Y/%m/%d')
	small_poster = models.ImageField(upload_to='thumbnails/%Y/%m/%d')
	link = models.URLField()
	designer = models.CharField(_(u'设计者'), max_length=20)

class Event_User(models.Model):
	event = models.ForeignKey(Event, verbose_name=_(u'活动'))
	user = models.ForeignKey(User, verbose_name=_(u'用户'))
	join_date = models.DateField(_(u'状态变更时间'), auto_now = True)
	is_admin = models.BooleanField(_(u'活动管理员'), default = False)
	is_join = models.BooleanField(_(u'参加'), default=False)