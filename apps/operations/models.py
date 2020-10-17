from datetime import datetime

from django.db import models

# Create your models here.
from courses.models import CourseInfo
from users.models import UserProfile


class UserAsk(models.Model):
    name = models.CharField(max_length=30, verbose_name='姓名')
    phone = models.CharField(max_length=11, verbose_name='电话')
    course = models.CharField(max_length=20, verbose_name='kec')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '咨询信息'
        verbose_name_plural = verbose_name


class UserLove(models.Model):
    love_user = models.ForeignKey(UserProfile, verbose_name='收藏用户', on_delete=models.CASCADE)
    love_id = models.IntegerField(verbose_name='收藏id')
    love_type = models.IntegerField(choices=((1, 'org'), (2, 'course'), (3, 'teacher')), verbose_name='收藏类别')
    love_status = models.BooleanField(default=False, verbose_name='收藏状态')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='收藏时间')

    def __str__(self):
        return self.love_user.username

    class Meta:
        verbose_name = '收藏信息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    study_man = models.ForeignKey(UserProfile, verbose_name='学习用户', on_delete=models.CASCADE)
    study_course = models.ForeignKey(CourseInfo, verbose_name='学习课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='学习时间')

    def __str__(self):
        return self.study_man.username

    class Meta:
        verbose_name = '用户学习课程信息'
        verbose_name_plural = verbose_name
        unique_together = ['study_man', 'study_course']


class UserComment(models.Model):
    comment_man = models.ForeignKey(UserProfile, verbose_name='评论用户', on_delete=models.CASCADE)
    comment_course = models.ForeignKey(CourseInfo, verbose_name='评论课程', on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=300, verbose_name='评论内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')

    def __str__(self):
        return self.comment_man.username

    class Meta:
        verbose_name = '用户评论课程信息'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    message_man = models.IntegerField(default=0, verbose_name='消息用户')   # 0代表系统消息，否则为用户消息
    message_content = models.CharField(max_length=200, verbose_name='消息内容')
    message_status = models.BooleanField(default=False, verbose_name='消息状态')    # 是否已读
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.message_content

    class Meta:
        verbose_name = '用户消息信息'
        verbose_name_plural = verbose_name
