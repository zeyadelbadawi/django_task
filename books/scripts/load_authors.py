import json
from books.models import Author

def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            author_data = json.loads(line)

            Author.objects.update_or_create(
                name=author_data['name'],
                defaults={
                    'average_rating': author_data.get('average_rating'),
                    'ratings_count': author_data.get('ratings_count'),
                    'about': author_data.get('about', ''),
                    'image_url': author_data.get('image_url', ''),
                }
            )

            if i % 100 == 0:
                print(f"Processed {i} authors")
