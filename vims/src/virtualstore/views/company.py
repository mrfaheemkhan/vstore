
from encodings.base64_codec import base64_decode
from inspect import stack
from vims import settings
from virtualstore.common import http_util, util
from virtualstore.forms import CompanyForm
from virtualstore.models import Company, Game, Store, Resource, Category, \
    Item
import os
 
def list(request):
    response = None
    if request.method == 'GET':
        message = None
        message = request.GET.get('message', None)
        
        if util.is_none_or_empty(message) == False:
            message = util.decode_base64(message)
        result_set = Company.objects.order_by('created_datetime')
        if len(result_set) > 0:
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        None, 
                                                        {'list_of_object' : result_set,
                                                         'object_count' : len(result_set),
                                                         'message'      : message
                                                         })
        else:
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        None, 
                                                        {'message' : 'No entries'})
    else:
        return "ERROR"
    
    return response
    
def add(request):
    response = None
    if request.method == 'GET':
        obj = Company(created_by=1, modified_by=1)
        form = CompanyForm(instance=obj)
        response = http_util.response_with_template(request, 
                                                    str(__file__), 
                                                    stack()[0][3], 
                                                    form)    
    elif request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            instance = form.instance
            instance.name = instance.name.strip()
            util.save_with_uuid(instance)
            response = http_util.redirect_with_message(str(__file__), 
                                                       'list', 
                                                       {'message' : util.encode_base64('Company added successfully')})
        else:
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form)
            
    return response
        
def edit(request):
    response = None
    obj_id = request.REQUEST.get('id', None)
    result_set = Company.objects.filter(id=obj_id)
        
    if util.is_none_or_empty(obj_id):
        response =  http_util.redirect_with_message(str(__file__), 
                                                    'list', 
                                                    {'message' : util.encode_base64('Invalid Id: '+str(obj_id))})
    else:
        if request.method == 'GET':
            if len(result_set) == 1:                
                obj = result_set[0]
                form = CompanyForm(instance=obj)
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form)
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           {'message' : util.encode_base64('No Company found with Id:'+str(obj_id))})    
        elif request.method == 'POST':
            if len(result_set) == 1:                
                obj = result_set[0]
                form = CompanyForm(request.POST, instance=obj)
                
                if form.is_valid():
                    instance = form.instance
                    instance.name = instance.name.strip()
                    util.save(instance)
                    response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           {'message' : util.encode_base64('Company edited successfully')})
                else:
                    response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form)
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           {'message' : util.encode_base64('No Company found with Id:'+str(obj_id))})
    return response


def delete(request):
    response = None
    obj_id = request.REQUEST.get('id', None)  
    
    if request.method == 'POST':           
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         }
                                                        ) 
            
        else:
            result_set = Company.objects.filter(id=obj_id)
            if len(result_set) == 1:                
                obj = result_set[0]     
                res_path_list = []
                obj_game_list = Game.objects.all().filter(company=obj)
                if len(obj_game_list) > 0:
                    for game_obj in obj_game_list:
                        obj_store_list = Store.objects.all().filter(game=game_obj)
                        if len(obj_store_list) > 0:
                            for store_obj in obj_store_list:
                                obj_store_res_list = Resource.objects.all().filter(store=store_obj)
                                for res in obj_store_res_list:
                                    res_path_list.append(res.server_file_path+res.server_file_name)
                                obj_cat_list = Category.objects.all().filter(store=store_obj)
                                if len(obj_cat_list) > 0:
                                    for cat_obj in obj_cat_list:
                                        obj_cat_res_list = Resource.objects.all().filter(category=cat_obj)
                                        for res in obj_cat_res_list:
                                            res_path_list.append(res.server_file_path+res.server_file_name)   
                                        
                                            obj_item_list = Item.objects.all().filter(category=cat_obj)
                                            if len(obj_item_list) > 0:
                                                for item_obj in obj_item_list:
                                                    obj_item_res_list = Resource.objects.all().filter(item=item_obj)
                                                    for res in obj_item_res_list:
                                                        res_path_list.append(res.server_file_path+res.server_file_name)   
                                                    item_obj.delete()
                                        cat_obj.delete()
                                store_obj.delete()
                        game_obj.delete()   
                obj.delete()
                
                for res_with_path in res_path_list:
                    try:
                        os.remove(settings.UPLOADED_CONTENT_DIR+res_with_path)
                    except:
                        pass
                    
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('Company deleted successfully.'),
                                                            }
                                                           )                    
                 
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('No Company found with Id:'+str(obj_id)),
                                                            }
                                                           ) 
                
    return response