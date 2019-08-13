# encoding: utf-8

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.course.models import Course,CourseCategory,Teacher
from apps.news.models import News,NewsCategory,Banner,Comment

class Command(BaseCommand):
    def handle(self, *args, **options):
        ## 1.课程组（管理课程）
        course_content_types = [
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
        ]
        course_permissions = Permission.objects.filter(content_type__in=course_content_types)
        courseGroup = Group.objects.create(name='课程组')
        courseGroup.permissions.set(course_permissions)
        courseGroup.save()
        self.stdout.write(self.style.SUCCESS('创建课程组成功'))
        ## 2.新闻组（管理新闻）
        news_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
        ]
        news_permissions = Permission.objects.filter(content_type__in=news_content_types)
        newsGrop = Group.objects.create(name='新闻组')
        newsGrop.permissions.set(news_permissions)
        newsGrop.save()
        self.stdout.write(self.style.SUCCESS('创建新闻组成功'))
        ## 3.管理员组（管理课程和新闻）
        admin_permission = course_permissions.union(news_permissions)
        adminGroup = Group.objects.create(name='管理员组')
        adminGroup.permissions.set(admin_permission)
        adminGroup.save()
        ## 4.超级管理员
        self.stdout.write(self.style.SUCCESS('创建管理员组成功'))
