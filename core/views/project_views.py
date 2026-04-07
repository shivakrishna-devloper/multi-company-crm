import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.models.project import Project
from core.decorators import require_role

@require_http_methods(['GET'])
def list_projects(request):
    projects = list(Project.objects.for_tenant(request.tenant_id).values('id','name','description'))
    return JsonResponse({'projects': projects})

@require_http_methods(['POST'])
def create_project(request):
    b = json.loads(request.body)
    p = Project.objects.create(
        company_id=request.tenant_id,
        name=b['name'],
        description=b.get('description','')
    )
    return JsonResponse({'id': str(p.id), 'name': p.name}, status=201)

@require_http_methods(['DELETE'])
@require_role('admin')
def delete_project(request, pid):
    p = Project.objects.for_tenant(request.tenant_id).filter(id=pid).first()
    if not p:
        return JsonResponse({'error': 'Not found'}, status=404)
    p.delete()
    return JsonResponse({'deleted': True})