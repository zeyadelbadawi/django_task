from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework import status
from django.core.cache import cache
from .models import Series
from .serializers import SeriesSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

class ReadOnlyIfUnauthenticated(BasePermission):
    """
    Custom permission to allow unauthenticated users to have read-only access
    (GET, HEAD, OPTIONS) while allowing authenticated users full access.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        if request.method in SAFE_METHODS: 
            return True

        return False



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [ReadOnlyIfUnauthenticated]  



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'genre', 'description', 'author__name']
    permission_classes = [ReadOnlyIfUnauthenticated] 


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user) 
            return redirect('/api/books/') 
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)


def generate_recommendations(user):
    # Get the user's favorite books
    favorite_books = user.favorite_books.all()

    if not favorite_books:
        return []

    # Combine features for each book
    def combine_features(book):
        return f"{book.title} {book.genre} {book.description or ''} {book.author.name}"

    # Collect all books excluding favorites
    all_books = list(Book.objects.exclude(id__in=favorite_books.values_list('id', flat=True)))

    # Return an empty list if there are not enough books
    if len(all_books) < 5:
        return []

    # Combine features for all favorite books and remaining books
    favorite_features = [combine_features(book) for book in favorite_books]
    all_features = favorite_features + [combine_features(book) for book in all_books]

    # Compute similarity
    vectorizer = CountVectorizer()
    feature_matrix = vectorizer.fit_transform(all_features)
    similarity = cosine_similarity(feature_matrix)

    # Average similarity scores for all favorite books
    scores = similarity[:len(favorite_features), len(favorite_features):].mean(axis=0)

    # Get top 5 recommendations
    top_indices = scores.argsort()[::-1][:5]
    recommended_books = [all_books[int(i)] for i in top_indices]  # Convert int64 to int

    # Serialize the recommended books
    return BookSerializer(recommended_books, many=True).data


@api_view(['POST'])
def add_to_favorites(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        user = request.user

        if user.is_authenticated:
            user.refresh_from_db()

            if user.favorite_books.filter(id=book.id).exists():
                return Response({'error': 'Book is already in your favorites.'}, status=400)

            if user.favorite_books.count() >= 20:
                return Response({'error': 'You can only have up to 20 favorite books.'}, status=400)

            user.favorite_books.add(book)

            recommendations = generate_recommendations(user)

            return Response({
                'message': 'Book added to favorites.',
                'recommendations': recommendations
            })

        return Response({'error': 'Authentication required.'}, status=401)

    except Book.DoesNotExist:
        return Response({'error': 'Book not found.'}, status=404)


@api_view(['POST'])
def remove_from_favorites(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        user = request.user
        if user.is_authenticated:
            user.favorite_books.remove(book)
            return Response({'message': 'Book removed from favorites.'})
        return Response({'error': 'Authentication required.'}, status=401)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found.'}, status=404)


@api_view(['GET'])
def recommend_books_by_favorites(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'Authentication required.'}, status=401)

    recommendations = generate_recommendations(user)

    return Response({
        'favorites': BookSerializer(user.favorite_books.all(), many=True).data,
        'recommendations': recommendations
    })
