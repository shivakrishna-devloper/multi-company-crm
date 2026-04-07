from functools import wraps
from django.http import JsonResponse

ROLES = {'admin': 3, 'member': 2, 'viewer': 1}

def require_role(minimum_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if ROLES.get(request.user_role, 0) < ROLES.get(minimum_role, 0):
                return JsonResponse({'error': f'Requires {minimum_role}'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator