import json, jwt, datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from core.models.company import Company
from core.models.user import User

@require_http_methods(['POST'])
def register_view(request):
    b = json.loads(request.body)
    co = Company.objects.create(name=b['company_name'], slug=b['company_slug'])
    u = User(email=b['email'], company=co, role='admin')
    u.set_password(b['password'])
    u.save()
    return JsonResponse({'company_id': str(co.id), 'user_id': str(u.id)}, status=201)

@require_http_methods(['POST'])
def login_view(request):
    b = json.loads(request.body)
    u = User.objects.filter(email=b['email']).first()
    if not u:
        return JsonResponse({'error': 'User not found'}, status=404)
    if not u.check_password(b['password']):
        return JsonResponse({'error': 'Invalid password'}, status=401)
    token = jwt.encode({
        'user_id': str(u.id),
        'company_id': str(u.company_id),
        'role': u.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }, settings.SECRET_KEY, algorithm='HS256')
    return JsonResponse({'token': token})

@require_http_methods(['POST'])
def add_user_view(request):
    b = json.loads(request.body)
    u = User(email=b['email'], company_id=request.tenant_id, role=b['role'])
    u.set_password(b['password'])
    u.save()
    return JsonResponse({'user_id': str(u.id), 'role': u.role}, status=201)