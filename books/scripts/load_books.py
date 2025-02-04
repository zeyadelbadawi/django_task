import json
from datetime import datetime
from books.models import Book, Author

def load_books(file_path, limit=300):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i >= limit:
                print(f"Loaded {limit} books into the database. Stopping.")
                break

            book_data = json.loads(line)

            author_name = book_data['author_name']
            author, _ = Author.objects.get_or_create(
                name=author_name,
                defaults={
                    'average_rating': book_data.get('average_rating'),
                    'ratings_count': book_data.get('ratings_count'),
                }
            )

            try:
                published_date = datetime.strptime(book_data['publication_date'], '%Y-%m').date()
            except (ValueError, TypeError):
                published_date = None

            try:
                num_pages = int(book_data.get('num_pages', 0)) if book_data.get('num_pages') else None
            except ValueError:
                num_pages = None

            Book.objects.create(
                title=book_data['title'][:500], 
                author=author,
                description=book_data.get('description', ''),
                genre=book_data.get('genre', ''),
                published_date=published_date,
                isbn=book_data.get('isbn'),
                isbn13=book_data.get('isbn13'),
                language=book_data.get('language', ''),
                average_rating=book_data.get('average_rating'),
                ratings_count=book_data.get('ratings_count'),
                image_url=book_data.get('image_url'),
                num_pages=num_pages,
                publisher=book_data.get('publisher', ''),
            )

            if i % 10 == 0:
                print(f"Processed {i} records")
