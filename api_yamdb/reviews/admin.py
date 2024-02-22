from django.contrib import admin

from .models import Comment, Review, Category, Genre, Title


admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')


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
    search_fields = ('review', 'text', 'author', 'pub_date')
    list_filter = ('review', 'author', 'pub_date')
    list_display_links = ('text',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, admin.ModelAdmin)
