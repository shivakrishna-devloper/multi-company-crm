from django.http import JsonResponse
from core.models.company import Company

class TenantMiddleware:
    EXCLUDED_PATHS = [
        '/api/auth/register/',
        '/api/auth/login/',
    ]
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in self.EXCLUDED_PATHS:
            return self.get_response(request)
        company = None
        host = request.get_host().split(':')[0]
        parts = host.split('.')
        if len(parts) >= 3:
            company = Company.objects.filter(slug=parts[0]).first()
        if not company:
            tid = request.headers.get('X-Tenant-ID')
            if tid:
                company = Company.objects.filter(id=tid).first()
        if not company:
            return JsonResponse({'error': 'Tenant not found'}, status=404)
        request.company = company
        request.tenant_id = str(company.id)
        return self.get_response(request)