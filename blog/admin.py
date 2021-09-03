from django.contrib import admin

from .models import Author, Blog, Comment

admin.site.register(Author)
admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'post_date', 'get_short_description']
    ordering = ['-post_date']
    list_filter = ['author', 'post_date']
    search_fields = ['author__last_name', 'author__first_name', 'title']
    inlines = [CommentInline]
