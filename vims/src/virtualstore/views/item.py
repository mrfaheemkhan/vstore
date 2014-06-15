
from inspect import stack
from vims import settings
from virtualstore.common import http_util, util, constants
from virtualstore.forms import ItemForm
from virtualstore.models import Category, Item, Resource
import os
 
def list(request):
    response = None
        
    if request.method == 'GET':
        message = None
        message = request.GET.get('message', None)
        parent = request.GET.get('parent', None)
        
        if util.is_none_or_empty(parent) or len(Category.objects.filter(id=parent)) == 0:
            response = http_util.redirect_with_message('cateogry', 
                                                        'list',                                                       
                                                        {'message' : util.encode_base64('Invalid Id:'+str(parent))})            
        else:        
            parent_obj = Category.objects.select_related().filter(id=parent)[0]
            if util.is_none_or_empty(message) == False:
                message = util.decode_base64(message)
            result_set = Item.objects.filter(category__id=parent).order_by('position')
            if len(result_set) > 0:
                fields_to_display = None
                custom_attrs = None
                # custom field display logic
                if parent_obj.store.name in constants.STORE_DISPLAY_FIELDS.keys():
                    fields_to_display = constants.STORE_DISPLAY_FIELDS[parent_obj.store.name]["__keys__"]
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            None, 
                                                            {'list_of_object' : result_set,
                                                             'object_count' : len(result_set),
                                                             'parent_obj' : parent_obj,
                                                             'message'      : message,
                                                             'display_fields' : fields_to_display,
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
        
    if util.is_none_or_empty(parent) or len(Category.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('category', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Category Id:'+str(parent))})
    else:
        parent_obj = Category.objects.select_related().filter(id=parent)[0]
        currency_list = util.export_json([x for x in parent_obj.store.game.currency_set.values_list('name', flat=True)])
         
        
        if request.method == 'GET':
            breeded_dropdown_data = util.make_breeded_dropdown(parent_obj)
            obj = Item(created_by=1, modified_by=1, category=parent_obj)
            form = ItemForm(instance=obj)
            custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj.store, form)
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj,
                                                         'currency_list' : currency_list,
                                                         'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                         'custom_attributes' : custom_attributes_list,
                                                         'custom_attributes_json' : util.export_json(custom_attributes_list),
                                                         'breeded_dropdown_data' : breeded_dropdown_data
                                                         })    
        elif request.method == "POST":
            form = ItemForm(request.POST)
            if form.is_valid():
                instance = form.instance
                instance.name = instance.name.strip()
                util.save(instance)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Item added successfully'),
                                                            'parent' : parent}
                                                           )
            else:
                custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj.store, form, value_from_instance=False)
                breeded_dropdown_data = util.make_breeded_dropdown(parent_obj)
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form,
                                                            {'parent_obj' : parent_obj,
                                                             'currency_list' : currency_list,
                                                             'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                             'custom_attributes' : custom_attributes_list,
                                                             'custom_attributes_json' : util.export_json(custom_attributes_list),
                                                             'breeded_dropdown_data' : breeded_dropdown_data
                                                             }
                                                            )
            
    return response
        
def edit(request):
    response = None
    parent = request.REQUEST.get('category', None)
    obj_id = request.REQUEST.get('id', None)   
    
    if util.is_none_or_empty(parent) or len(Category.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('category', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Category Id:'+str(parent))})
    else:
        parent_obj = Category.objects.select_related().filter(id=parent)[0]
        currency_list = util.export_json([x for x in parent_obj.store.game.currency_set.values_list('name', flat=True)])    
        result_set = Item.objects.filter(id=obj_id)
            
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
                    form = ItemForm(instance=obj)
                    breeded_dropdown_data = util.make_breeded_dropdown(parent_obj)
                    luckybox_dropdown = util.make_dailybonus_dropdown(parent_obj)
                    custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj.store, form)
                    response = http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                {'parent_obj' : parent_obj,
                                                                 'currency_list' : currency_list,
                                                                 'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                                 'custom_attributes' : custom_attributes_list,
                                                                 'custom_attributes_json' : util.export_json(custom_attributes_list),
                                                                 'breeded_dropdown_data' : breeded_dropdown_data,
                                                                 'luckybox_dropdown_data' : luckybox_dropdown
                                                                 }
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               { 'message' : util.encode_base64('No Item found with Id:'+str(obj_id)),
                                                                'parent' : parent}
                                                               )    
            elif request.method == 'POST':
                if len(result_set) == 1:                
                    obj = result_set[0]
                    form = ItemForm(request.POST, instance=obj)
                    
                    if form.is_valid():
                        instance = form.instance
                        instance.name = instance.name.strip()
                        util.save(instance)
                        response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('Item edited successfully'),
                                                                'parent' : parent}                                                           
                                                               )
                    else:
                        breeded_dropdown_data = util.make_breeded_dropdown(parent_obj)
                        custom_attributes_list = util.get_custom_attribtes_widget_dict(parent_obj.store, form, value_from_instance=False)
                        response =  http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                { 'parent_obj' : parent_obj,
                                                                 'currency_list' : currency_list,
                                                                 'fields_filter': constants.CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING,
                                                                 'custom_attributes' : custom_attributes_list,
                                                                 'custom_attributes_json' : util.export_json(custom_attributes_list),
                                                                 'breeded_dropdown_data' : breeded_dropdown_data
                                                                 }
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('No Item found with Id:'+str(obj_id)),
                                                                'parent' : parent }
                                                               )
    return response

def delete(request):
    response = None
    parent = request.REQUEST.get('category', None)
    obj_id = request.REQUEST.get('id', None)  
    
    if request.method == 'POST':           
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
            
        else:
            result_set = Item.objects.filter(id=obj_id)
            if len(result_set) == 1:                
                obj = result_set[0]                    
                obj_res_list = Resource.objects.all().filter(item=obj)
                res_path_list = []
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
                                                           { 'message' : util.encode_base64('Item deleted successfully.'),
                                                            'parent' : parent}
                                                           )                    
                 
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('No Item found with Id:'+str(obj_id)),
                                                            'parent' : parent}
                                                           ) 
                
    return response