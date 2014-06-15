
from copy import copy
from inspect import stack
from virtualstore.common import http_util, util
from virtualstore.forms import CustomAttributeForm
from virtualstore.models import Game, CustomAttribute
 
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
            result_set = CustomAttribute.objects.filter(game__id=parent).order_by('name')
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
        
    if util.is_none_or_empty(parent) or len(Game.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('game', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Game Id:'+str(parent))})
    else:
        parent_obj = Game.objects.select_related().filter(id=parent)[0]
        if request.method == 'GET':
            obj = CustomAttribute(created_by=1, modified_by=1, game=parent_obj)
            form = CustomAttributeForm(instance=obj)
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj                                                         
                                                         })    
        elif request.method == "POST":
            form = CustomAttributeForm(request.POST)
            if form.is_valid():
                instance = form.instance
                instance.name = instance.name.strip()
#                select the proper column for multivalue
#                text columns start from index 40
                used_columns = CustomAttribute.objects.filter(game=parent_obj.id)
                column_to_use = 0
                if instance.type == "multivalue":
                    #check last 60 columns first as they are text types
                    for index in range(41,  101):
                        if used_columns.filter(mapped_column="attribute_"+str(index)).count() == 0:
                            column_to_use = index;
                            break;

                    if column_to_use == 0:                        
                        for index in range(1, 41):
                            if used_columns.filter(mapped_column="attribute_"+str(index)).count() == 0:
                                column_to_use = index;
                                break;
                else:                    
                    for index in range(1, 101):
                        if used_columns.filter(mapped_column="attribute_"+str(index)).count() == 0:
                            column_to_use = index;
                            break;
                if column_to_use != 0:
                    instance.mapped_column = "attribute_" + str(column_to_use)
                else:
                    pass
                
                util.save(instance)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Custom Attribute added successfully'),
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
    parent = request.REQUEST.get('game', None)
    obj_id = request.REQUEST.get('id', None)   
    
    if util.is_none_or_empty(parent) or len(Game.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('game', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Game Id:'+str(parent))})
    else:
        parent_obj = Game.objects.select_related().filter(id=parent)[0]    
        result_set = CustomAttribute.objects.filter(id=obj_id)
            
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
                    form = CustomAttributeForm(instance=obj)
                    form.fields['type'].widget.attrs = {'disabled':True}
                    response = http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                {'parent_obj' : parent_obj}
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               { 'message' : util.encode_base64('No Custom Attribute found with Id:'+str(obj_id)),
                                                                'parent' : parent}
                                                               )    
            elif request.method == 'POST':
                if len(result_set) == 1:                
                    obj = result_set[0]
                    post_dict = copy(request.POST)
                    post_dict['type'] = obj.type
                    form = CustomAttributeForm(post_dict, instance=obj)
                    if form.is_valid():
                        instance = form.instance
                        instance.name = instance.name.strip()
                        util.save(instance)
                        response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('Custom Attribute edited successfully'),
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
                                                               {'message' : util.encode_base64('No Custom Attribute found with Id:'+str(obj_id)),
                                                                'parent' : parent }
                                                               )
    return response

def delete(request):
    response = None
    parent = request.REQUEST.get('parent', None)
    obj_id = request.REQUEST.get('id', None)   
    
    if util.is_none_or_empty(parent) or len(Game.objects.filter(id=parent)) == 0:
        response = http_util.redirect_with_message('game', 
                                                    'list',                                                    
                                                    {'message' : util.encode_base64('Invalid Game Id:'+str(parent))})
    else:    
        result_set = CustomAttribute.objects.filter(id=obj_id)
            
        if util.is_none_or_empty(obj_id):
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid Id: '+str(obj_id)),
                                                         'parent'  : parent }
                                                        ) 
        elif request.method == 'POST':
            obj = result_set[0]
            obj.delete()
            del_name = obj.name
            response =  http_util.redirect_with_message(str(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Custom Attribute: %s deleted successfully' % (del_name)),
                                                         'parent'  : parent }
                                                        )
        else:
            response =  http_util.redirect_with_message(tr(__file__), 
                                                        'list', 
                                                        { 'message' : util.encode_base64('Invalid method call.'),
                                                         'parent'  : parent }
                                                        )
           
    return response