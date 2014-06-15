
from inspect import stack
from vims import settings
from virtualstore.common import http_util, util, constants
from virtualstore.forms import CategoryForm
from virtualstore.models import Store, Category, Resource, Item
import os
 
def list(request):
    response = None
        
    if request.method == 'GET':
        message = None
        message = request.GET.get('message', None)
        parent = request.GET.get('parent', None)
        
        if util.is_none_or_empty(parent) or len(Store.objects.filter(id=parent)) == 0:
            response = http_util.redirect_with_message('store', 
                                                        'list',                                                       
                                                        {'message' : util.encode_base64('Invalid Id:'+str(parent))})            
        else:        
            parent_obj = Store.objects.select_related().filter(id=parent)[0]
            if util.is_none_or_empty(message) == False:
                message = util.decode_base64(message)
            result_set = Category.objects.filter(store__id=parent).order_by('position')
            if len(result_set) > 0:
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            None, 
                                                            {'list_of_object' : result_set,
                                                             'object_count' : len(result_set),
                                                             'parent_obj' : parent_obj,
                                                             'message'      : message
                                                             })
            else:
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            None, 
                                                            {'message' : 'No entries',
                                                             'parent_obj' : parent_obj})
    else:
        return "ERROR"
    
    return response
    
def add(request):
    response = None 
    parent = request.REQUEST.get('parent', None)
        
    if util.is_none_or_empty(parent) or len(Store.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('store', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Store Id:'+str(parent))})
    else:
        parent_obj = Store.objects.select_related().filter(id=parent)[0] 
        currency_list = util.export_json([x for x in parent_obj.game.currency_set.values_list('name', flat=True)])
        if request.method == 'GET':
            obj = Category(created_by=1, modified_by=1, store=parent_obj, version=1)
            form = CategoryForm(instance=obj)
            custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj, form)
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj,
                                                         'currency_list' : currency_list,
                                                         'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                         'custom_attributes' : custom_attributes_list,
                                                         'custom_attributes_json' : util.export_json(custom_attributes_list)
                                                         })    
        elif request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                instance = form.instance
                instance.name = instance.name.strip()
                util.save(instance)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Category added successfully'),
                                                            'parent' : parent}
                                                           )
            else:
                custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj, form, value_from_instance=False)
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form,
                                                            {'parent_obj' : parent_obj,
                                                             'currency_list' : currency_list,
                                                             'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                             'custom_attributes' : custom_attributes_list,
                                                             'custom_attributes_json' : util.export_json(custom_attributes_list)
                                                             }
                                                            )
            
    return response
        
def edit(request):
    response = None
    parent = request.REQUEST.get('store', None)
    obj_id = request.REQUEST.get('id', None)   
    
    if util.is_none_or_empty(parent) or len(Store.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('store', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Store Id:'+str(parent))})
    else:
        parent_obj = Store.objects.select_related().filter(id=parent)[0]
        currency_list = util.export_json([x for x in parent_obj.game.currency_set.values_list('name', flat=True)])    
        result_set = Category.objects.filter(id=obj_id)
            
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
        else:
            if request.method == 'GET':
                if len(result_set) == 1:                
                    obj = result_set[0]                    
                    form = CategoryForm(instance=obj)
                    custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj, form)
                    response = http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                {'parent_obj' : parent_obj,
                                                                 'currency_list' : currency_list,
                                                                 'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                                 'custom_attributes' : custom_attributes_list,
                                                                 'custom_attributes_json' : util.export_json(custom_attributes_list)
                                                                 }
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               { 'message' : util.encode_base64('No Category found with Id:'+str(obj_id)),
                                                                'parent' : parent}
                                                               )    
            elif request.method == 'POST':
                if len(result_set) == 1:                
                    obj = result_set[0]
                    form = CategoryForm(request.POST, instance=obj)
                    
                    if form.is_valid():
                        instance = form.instance
                        instance.name = instance.name.strip()
                        util.save(instance)
                        response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('Category edited successfully'),
                                                                'parent' : parent}                                                           
                                                               )
                    else:
                        custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj, form, value_from_instance=False)
                        response =  http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                { 'parent_obj' : parent_obj,
                                                                 'currency_list' : currency_list,
                                                                 'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                                 'custom_attributes' : custom_attributes_list,
                                                                 'custom_attributes_json' : util.export_json(custom_attributes_list)                                                                 
                                                                 }
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('No Category found with Id:'+str(obj_id)),
                                                                'parent' : parent }
                                                               )
    return response

def delete(request):
    response = None
    parent = request.REQUEST.get('store', None)
    obj_id = request.REQUEST.get('id', None)  
    
    if request.method == 'POST':           
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
            
        else:
            result_set = Category.objects.filter(id=obj_id)
            if len(result_set) == 1:                
                obj = result_set[0]     
                res_path_list = []
                obj_item_list = Item.objects.all().filter(category=obj)
                if len(obj_item_list) > 0:
                    for item_obj in obj_item_list:
                        obj_item_res_list = Resource.objects.all().filter(item=item_obj)
                        for res in obj_item_res_list:
                            res_path_list.append(res.server_file_path+res.server_file_name)   
                        item_obj.delete()
                        
                obj_res_list = Resource.objects.all().filter(category=obj)
                for res in obj_res_list:
                    res_path_list.append(res.server_file_path+res.server_file_name)
                    
                obj.delete()
                
                for res_with_path in res_path_list:
                    try:
                        os.remove(settings.UPLOADED_CONTENT_DIR+res_with_path)
                    except:
                        pass
                    
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('Category deleted successfully.'),
                                                            'parent' : parent}
                                                           )                    
                 
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('No Category found with Id:'+str(obj_id)),
                                                            'parent' : parent}
                                                           ) 
                
    return response