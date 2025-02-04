import json
from books.models import Series, Book

def load_series(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            series_data = json.loads(line)

            print(f"Processing series {i + 1}: {series_data.get('title')}")

            series, created = Series.objects.get_or_create(
                title=series_data['title'],
                defaults={
                    'description': series_data.get('description', '')
                }
            )

            if created:
                print(f"Created new series: {series.title}")
            else:
                print(f"Existing series found: {series.title}")

            for work in series_data.get('works', []):
                book_title = work.get('title')
                book = Book.objects.filter(title=book_title).first()
                
                if book:
                    print(f"Adding book '{book.title}' to series '{series.title}'")
                    series.books.add(book)
                else:
                    print(f"Book '{book_title}' not found for series '{series.title}'")

            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1} series")

    print("Finished processing all series.")
