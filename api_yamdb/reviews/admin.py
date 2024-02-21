from django.contrib import admin

from .models import Comment, Review

admin.site.empty_value_display = 'Не задано'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ReviewAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    '''list_editable = (
        'score',
        'pub_date'
    )'''
    search_fields = ('title', 'text', 'author', 'score', 'pub_date')
    list_filter = ('title', 'author', 'score', 'pub_date')
    list_display_links = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    '''list_editable = (
        'pub_date',
    )'''
    search_fields = ('review', 'text', 'author', 'pub_date')
    list_filter = ('review', 'author', 'pub_date')
    list_display_links = ('text',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
