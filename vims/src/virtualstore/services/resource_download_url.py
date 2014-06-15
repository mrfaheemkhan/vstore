from virtualstore.models import Resource
from vims import settings
def get_resource_path(resource_id):
    resource = Resource.objects.get(id=resource_id)
    return '/content'+settings.UPLOADED_CONTENT_SUBDIR+resource.server_file_path+'/'+resource.server_file_name
    