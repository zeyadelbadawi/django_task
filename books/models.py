from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=500) 
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=50)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    isbn13 = models.CharField(max_length=17, blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    favorites = models.ManyToManyField('auth.User', related_name='favorite_books', blank=True)

    def __str__(self):
        return self.title


class Series(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    books = models.ManyToManyField(Book, related_name='series')

    def __str__(self):
        return self.title
