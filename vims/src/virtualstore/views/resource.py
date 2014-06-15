
from django.forms.widgets import HiddenInput
from inspect import stack
from virtualstore.common import http_util, util, constants
from virtualstore.forms import ResourceUploadForm
from virtualstore.models import Game, Currency, Store, Category, Item, \
    Resource
import os
from vims import settings
 
def list(request):
    response = None
        
    if request.method == 'GET':
        message = None
        message = request.GET.get('message', None)
        parent = request.GET.get('parent', None)
        parent_type = request.GET.get('parent_type', None)
        
        if util.is_none_or_empty(parent) or util.is_none_or_empty(parent_type):
            response = http_util.redirect_with_message('game', 
                                                        'list',                                                       
                                                        {'message' : util.encode_base64('Invalid Id:'+str(parent))})            
        else:
            parent_obj = None
            if parent_type == 'store':
                parent_obj = Store.objects.select_related().filter(id=parent)[0]
            elif parent_type == 'category':
                parent_obj = Category.objects.select_related().filter(id=parent)[0] 
            elif parent_type == 'item':
                parent_obj = Item.objects.select_related().filter(id=parent)[0]
                
            if util.is_none_or_empty(message) == False:
                message = util.decode_base64(message)
            result_set = Resource.objects.filter(**{str(parent_type):str(parent)}).order_by('type')
            
            if len(result_set) > 0:
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            None, 
                                                            {'list_of_object' : result_set,
                                                             'object_count' : len(result_set),
                                                             'parent_obj' : parent_obj,
                                                             'parent_type' : parent_type,
                                                             'message'      : message,
                                                             'download_url' : '/export/resource/'
                                                             })
            else:
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            None, 
                                                            {'message' : 'No entries',
                                                             'parent_obj' : parent_obj,
                                                             'parent_type' : parent_type})
    else:
        return "ERROR"
    
    return response
    
def add(request):
    response = None 
    parent = request.REQUEST.get('parent', None)
    parent_type = request.REQUEST.get('parent_type', None)
        
    if util.is_none_or_empty(parent) or util.is_none_or_empty(parent_type):
        response = http_util.redirect_with_message('company', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Id:'+str(parent))})
    else:
        parent_obj = None
        if parent_type == 'store':
            parent_obj = Store.objects.select_related().filter(id=parent)[0]
        elif parent_type == 'category':
            parent_obj = Category.objects.select_related().filter(id=parent)[0] 
        elif parent_type == 'item':
            parent_obj = Item.objects.select_related().filter(id=parent)[0]
            
        if request.method == 'GET':
            form = ResourceUploadForm()
            form['resource_id'].field.widget = HiddenInput()
            form['parent'].field.widget = HiddenInput({"value": parent})
            form['parent_type'].field.widget = HiddenInput({"value": parent_type})
            
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj,
                                                         'parent_type' : parent_type
                                                         })    
        elif request.method == "POST":
            form = ResourceUploadForm(request.POST, request.FILES)
            if form.is_valid():
                resoure_type = form['type'].data
                resource_file = request.FILES.get('file')
                util.save_resource(request.user.id, parent_obj, parent_type, resoure_type, resource_file)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Resource added successfully'),
                                                            'parent' : parent,
                                                            'parent_type' : parent_type}
                                                           )
            else:
                form['resource_id'].field.widget = HiddenInput()
                form['parent'].field.widget = HiddenInput({"value": parent})
                form['parent_type'].field.widget = HiddenInput({"value": parent_type})
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form,
                                                            {'parent_obj' : parent_obj,
                                                             'parent_type' : parent_type}
                                                            )
            
    return response

def delete(request):
    response = None
    if request.method == 'POST':
        resource_id = request.REQUEST.get('id', None)
        parent = request.REQUEST.get('parent', None)
        parent_type = request.REQUEST.get('parent_type', None)
        resource = Resource.objects.get(id=resource_id)
        resource.delete()
        try:         
            os.remove(settings.UPLOADED_CONTENT_DIR+resource.server_file_path+'/'+resource.server_file_name)
        except:
            pass
        response = http_util.redirect_with_message(str(__file__), 
                                           'list',
                                           { 'message': util.encode_base64('Resource deleted successfully'),
                                            'parent' : parent,
                                            'parent_type' : parent_type}
                                           )            
    return response
            
