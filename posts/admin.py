from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'is_expired', 'expiration_days')
    list_filter = ['pub_date', 'author']
    search_fields = ['title', 'content']
    raw_id_fields = ('author',)