from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ['/api/books/', '/api/authors/']

        if any(request.path.startswith(path) for path in protected_paths):
            if not request.user.is_authenticated and request.method not in ['GET', 'HEAD', 'OPTIONS']:
                return redirect(reverse('login_page'))  

        return self.get_response(request)
