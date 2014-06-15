
from inspect import stack
from vims import settings
from virtualstore.common import http_util, util
from virtualstore.forms import StoreForm
from virtualstore.models import Game, Store, CustomAttribute, StoreCache, \
    Item, Resource, Category
from virtualstore.services import cache
import os
import urllib2
 
def list(request):
    response = None
        
    if request.method == 'GET':
        message = None
        message = request.GET.get('message', None)
        parent = request.GET.get('parent', None)
        
        if util.is_none_or_empty(parent) or len(Game.objects.filter(id=parent)) == 0:
            response = http_util.redirect_with_message('game', 
                                                        'list',                                                       
                                                        {'message' : util.encode_base64('Invalid Id:'+str(parent))})            
        else:        
            parent_obj = Game.objects.select_related().filter(id=parent)[0]
            if util.is_none_or_empty(message) == False:
                message = util.decode_base64(message)
            result_set = Store.objects.filter(game__id=parent).order_by('position')
            if len(result_set) > 0:
                for sto_obj in result_set:
                    sto_cache_obj = StoreCache.objects.all().filter(id=sto_obj.id)
                    if len(sto_cache_obj) > 0:
                        sto_obj.last_pushed = sto_cache_obj[0].modified_datetime
                    else:
                        sto_obj.last_pushed = 'N/A'
                
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
        
    if util.is_none_or_empty(parent) or len(Game.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('game', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Game Id:'+str(parent))})
    else:
        parent_obj = Game.objects.select_related().filter(id=parent)[0]        
        if request.method == 'GET':
            obj = Store(created_by=1, modified_by=1, game=parent_obj)
            form = StoreForm(instance=obj)
            form = update_for_custom_attributes(parent, form)
            
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj})    
        elif request.method == "POST":
            form = StoreForm(request.POST)
            if form.is_valid(): 
                form.instance.name = form.instance.name.strip()
                util.save(form)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Store added successfully'),
                                                            'parent' : parent}
                                                           )
            else:                
                form = update_for_custom_attributes(parent, form)
                response = http_util.response_with_template(request, 
                                                            str(__file__), 
                                                            stack()[0][3], 
                                                            form,
                                                            {'parent_obj' : parent_obj}
                                                            )
            
    return response
        
def edit(request):
    response = None
    parent = request.REQUEST.get('game', None)
    obj_id = request.REQUEST.get('id', None)   
    
    if util.is_none_or_empty(parent) or len(Game.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('game', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Game Id:'+str(parent))})
    else:
        parent_obj = Game.objects.select_related().filter(id=parent)[0]    
        result_set = Store.objects.filter(id=obj_id)
            
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
                    form = StoreForm(instance=obj)
                    form = update_for_custom_attributes(parent, form)
                    response = http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                {'parent_obj' : parent_obj}
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               { 'message' : util.encode_base64('No Store found with Id:'+str(obj_id)),
                                                                'parent' : parent}
                                                               )    
            elif request.method == 'POST':
                if len(result_set) == 1:                
                    obj = result_set[0]
                    form = StoreForm(request.POST, instance=obj)
                    form = update_for_custom_attributes(parent, form)
                    
                    if form.is_valid():
                        form.instance.name = form.instance.name.strip()
                        util.save(form)
                        response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('Store edited successfully'),
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
                                                               {'message' : util.encode_base64('No Store found with Id:'+str(obj_id)),
                                                                'parent' : parent }
                                                               )
    return response

def push(request):
    response = None
        
    if request.method == 'POST':
        parent = request.REQUEST.get('parent', None)
        obj_id = request.REQUEST.get('id', None)
        
        result_set = Store.objects.filter(id=obj_id)
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
        else:
            if len(result_set) == 1:                
                cache.update_store_cache(obj_id)
                game_obj = result_set[0].game
                urllib2.urlopen(game_obj.web_service_url+"games/update_store?store_id="+str(result_set[0].visible_id))
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('Store pushed successfully.'),
                                                            'parent' : parent}
                                                           )
    return response    
    
def update_for_custom_attributes(parent, form):
    all_custom_attributes = CustomAttribute.objects.filter(game=parent)
    all_attribute_names = []
    for atrb in all_custom_attributes:
        all_attribute_names.append((atrb.id, atrb.name))
    form['category_attributes'].field.queryset = all_custom_attributes
    form['item_attributes'].field.queryset = all_custom_attributes
    form['category_attributes'].field.widget.choices = all_attribute_names
    form['item_attributes'].field.widget.choices = all_attribute_names
    return form

def delete(request):
    response = None
    parent = request.REQUEST.get('game', None)
    obj_id = request.REQUEST.get('id', None)  
    
    if request.method == 'POST':           
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
            
        else:
            result_set = Store.objects.filter(id=obj_id)
            if len(result_set) == 1:                
                obj = result_set[0]     
                res_path_list = []
                obj_cat_list = Category.objects.all().filter(store=obj)
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
                        
                obj_res_list = Resource.objects.all().filter(store=obj)
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
                                                           { 'message' : util.encode_base64('Store deleted successfully.'),
                                                            'parent' : parent}
                                                           )                    
                 
            else:
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list', 
                                                           { 'message' : util.encode_base64('No Store found with Id:'+str(obj_id)),
                                                            'parent' : parent}
                                                           ) 
                
    return response