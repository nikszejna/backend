from django.contrib import admin
from .models import CommentRecord, Dashboard

class DashboardAdmin(admin.ModelAdmin):
  list = ('title', 'description', 'completed')

admin.site.register(Dashboard,DashboardAdmin)
admin.site.register(CommentRecord)