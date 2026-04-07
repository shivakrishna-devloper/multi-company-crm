import jwt
from django.conf import settings
from django.http import JsonResponse

class JWTAuthMiddleware:
    PUBLIC = ['/api/auth/login/', '/api/auth/register/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in self.PUBLIC:
            return self.get_response(request)
        token = request.headers.get('Authorization','').replace('Bearer ','')
        if not token:
            return JsonResponse({'error': 'No token'}, status=401)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        if payload.get('company_id') != request.tenant_id:
            return JsonResponse({'error': 'Company mismatch'}, status=403)
        request.user_id = payload['user_id']
        request.user_role = payload['role']
        return self.get_response(request)