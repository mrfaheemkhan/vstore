
from inspect import stack
from vims import settings
from virtualstore.common import http_util, util
from virtualstore.forms import GameForm
from virtualstore.models import Company, Game, Store, Category, Resource, \
    Item
import os
 
def list(request):
    response = None
        
    if request.method == 'GET':
        message = None
        message = request.GET.get('message', None)
        parent = request.GET.get('parent', None)
        
        if util.is_none_or_empty(parent) or len(Company.objects.filter(id=parent)) == 0:
            response = http_util.redirect_with_message('company', 
                                                        'list',                                                       
                                                        {'message' : util.encode_base64('Invalid Id:'+str(parent))})            
        else:        
            parent_obj = Company.objects.select_related().filter(id=parent)[0]
            if util.is_none_or_empty(message) == False:
                message = util.decode_base64(message)
            result_set = Game.objects.filter(company__id=parent).order_by('name')
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
        
    if util.is_none_or_empty(parent) or len(Company.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('company', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Company Id:'+str(parent))})
    else:
        parent_obj = Company.objects.select_related().filter(id=parent)[0]
        if request.method == 'GET':
            obj = Game(created_by=1, modified_by=1, company=parent_obj)
            form = GameForm(instance=obj)
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj})    
        elif request.method == "POST":
            form = GameForm(request.POST)
            if form.is_valid():
                instance = form.instance
                instance.name = instance.name.strip()
                util.save_with_uuid(instance)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Game added successfully'),
                                                            'parent' : parent}
                                                           )
            else:
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form,
                                                            {'parent_obj' : parent_obj}
                                                            )
            
    return response
        
def edit(request):
    response = None
    parent = request.REQUEST.get('company', None)
    obj_id = request.REQUEST.get('id', None)   
    
    if util.is_none_or_empty(parent) or len(Company.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('company', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Company Id:'+str(parent))})
    else:
        parent_obj = Company.objects.select_related().filter(id=parent)[0]    
        result_set = Game.objects.filter(id=obj_id)
            
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
                    form = GameForm(instance=obj)
                    response = http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                {'parent_obj' : parent_obj}
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               { 'message' : util.encode_base64('No Game found with Id:'+str(obj_id)),
                                                                'parent' : parent}
                                                               )    
            elif request.method == 'POST':
                if len(result_set) == 1:                
                    obj = result_set[0]
                    form = GameForm(request.POST, instance=obj)
                    
                    if form.is_valid():
                        instance = form.instance
                        instance.name = instance.name.strip()
                        util.save(instance)
                        response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('Game edited successfully'),
                                                                'parent' : parent}                                                           
                                                               )
                    else:
                        response =  http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                { 'parent_obj' : parent_obj}
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('No Game found with Id:'+str(obj_id)),
                                                                'parent' : parent }
                                                               )
    return response

def delete(request):
    response = None
    parent = request.REQUEST.get('company', None)
    obj_id = request.REQUEST.get('id', None)  
    
    if request.method == 'POST':           
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
            
        else:
            result_set = Game.objects.filter(id=obj_id)
            if len(result_set) == 1:                
                obj = result_set[0]     
                res_path_list = []
                obj_store_list = Store.objects.all().filter(game=obj)
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
                obj.delete()
                
                for res_with_path in res_path_list:
                    try:
                        os.remove(settings.UPLOADED_CONTENT_DIR+res_with_path)
                    except:
                        pass
                    
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('Game deleted successfully.'),
                                                            'parent' : parent}
                                                           )                    
                 
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('No Game found with Id:'+str(obj_id)),
                                                            'parent' : parent}
                                                           ) 
                
    return response