from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from app.models import *


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
	list_display = ['caption', 'author', 'creation_time']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
	list_display = ['who', 'moment', 'effective']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['author', 'content', 'moment', 'creation_time']

TokenAdmin.raw_id_fields = ('user', )