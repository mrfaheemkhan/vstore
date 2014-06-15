
from inspect import stack
from virtualstore.common import http_util, util
from virtualstore.forms import GameForm, CurrencyForm
from virtualstore.models import Company, Game, Currency
 
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
            result_set = Currency.objects.filter(game__id=parent).order_by('name')
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
            obj = Currency(created_by=1, modified_by=1, game=parent_obj)
            form = CurrencyForm(instance=obj)
            response = http_util.response_with_template(request, 
                                                        str(__file__), 
                                                        stack()[0][3], 
                                                        form,
                                                        {'parent_obj' : parent_obj})    
        elif request.method == "POST":
            form = CurrencyForm(request.POST)
            if form.is_valid():
                instance = form.instance
                instance.name = instance.name.strip()
                util.save(instance)
                response = http_util.redirect_with_message(str(__file__), 
                                                           'list',
                                                           { 'message': util.encode_base64('Currency added successfully'),
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
        result_set = Currency.objects.filter(id=obj_id)
            
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
                    form = CurrencyForm(instance=obj)
                    response = http_util.response_with_template(request, 
                                                                str(__file__), 
                                                                stack()[0][3], 
                                                                form,
                                                                {'parent_obj' : parent_obj}
                                                                )
                else:
                    response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               { 'message' : util.encode_base64('No Currency found with Id:'+str(obj_id)),
                                                                'parent' : parent}
                                                               )    
            elif request.method == 'POST':
                if len(result_set) == 1:                
                    obj = result_set[0]
                    form = CurrencyForm(request.POST, instance=obj)
                    
                    if form.is_valid():
                        instance = form.instance
                        instance.name = instance.name.strip()
                        util.save(instance)
                        response = http_util.redirect_with_message(str(__file__), 
                                                               'list', 
                                                               {'message' : util.encode_base64('Currency edited successfully'),
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
                                                               {'message' : util.encode_base64('No Currency found with Id:'+str(obj_id)),
                                                                'parent' : parent }
                                                               )
    return response