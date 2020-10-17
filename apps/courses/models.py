from datetime import datetime

from django.db import models

# Create your models here.
from orgs.models import OrgInfo, TeacherInfo


class CourseInfo(models.Model):
    image = models.ImageField(upload_to='course/', max_length=50, verbose_name='课程封面', null=True)
    name = models.CharField(max_length=20, verbose_name='课程名称')
    study_time = models.IntegerField(default=0, verbose_name='课程时长')
    study_num = models.IntegerField(default=0, verbose_name='学习人数')
    level = models.CharField(choices=(('hard', '高级'), ('normal', '中级'), ('easy', '初级')), max_length=20, verbose_name='课程难度')
    love_num = models.IntegerField(default=0, verbose_name='收藏数')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    desc = models.CharField(max_length=200, verbose_name='课程简介', null=True)
    detail = models.TextField(verbose_name='课程详情', null=True)
    category = models.CharField(choices=(('qd', '前端开发'), ('hd', '后端开发')), max_length=20)
    course_notice = models.CharField(max_length=200, verbose_name='课程公告', null=True)
    course_need = models.CharField(max_length=100, verbose_name='课程须知', null=True)
    teacher_tell = models.CharField(max_length=200, verbose_name='教学指导', null=True)
    orginfo = models.ForeignKey(OrgInfo, verbose_name='所属机构', on_delete=models.CASCADE)
    teacherinfo = models.ForeignKey(TeacherInfo, verbose_name='所属讲师', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name


class LessionInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='章节名称')
    course = models.ForeignKey(CourseInfo, verbose_name='所属课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '章节信息'
        verbose_name_plural = verbose_name


class VideoInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='视频名称')
    study_time = models.IntegerField(default=0, verbose_name='视频时长')
    url = models.URLField(default='http://www.atuguigu.com', verbose_name='添加时间')
    lessoninfo = models.ForeignKey(LessionInfo, verbose_name='所属章节', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name


class SourceInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='资源名称')
    down_load = models.FileField(upload_to='source/', max_length=200, verbose_name='下载路径')
    courseinfo = models.ForeignKey(CourseInfo, verbose_name='所属课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '资源信息'
        verbose_name_plural = verbose_name
