from django.contrib import admin
from .models import Author, Book, Series

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating', 'ratings_count')
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_date', 'average_rating')
    list_filter = ('genre', 'published_date')
    search_fields = ('title', 'author__name', 'genre')

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Series, SeriesAdmin)
