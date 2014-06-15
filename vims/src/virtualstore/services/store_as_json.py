from django.forms.models import model_to_dict
from virtualstore.common import util
from virtualstore.models import Store, Resource
from string import lower
from django import db

EXCLUDE_FIELD_LIST = ['created_by', 
                      'created_datetime', 
                      'modified_by', 
                      'modified_datetime',
                      'company',
                      'game',
                      'item_attributes',
                      'category_attributes',
                      'version',
                      'min_version',
                      'max_version',
                      'visible_to'
                      ]


CATEGORY_ITEM_INCLUDE_FIELD_LIST = ['id', 
                                   'name', 
                                   'description', 
                                   'visible_id',
                                   'position',
                                   'is_active',
                                   'is_local',
                                   'is_new',
                                   'active_campaign']

def get_json(store_id):
    global EXCLUDE_FIELD_LIST
    
    
    store = Store.objects.select_related().get(id=store_id)
    #===========================================================================
    # company
    #===========================================================================
    company = store.game.company
    company_dict = model_to_dict(company, exclude=EXCLUDE_FIELD_LIST)    
    
    #===========================================================================
    # game
    #===========================================================================
    
    game = store.game
    game_dict = model_to_dict(game, exclude=EXCLUDE_FIELD_LIST)
    currency_list = []
    for currency in game.currency_set.all():
        currency_list.append(model_to_dict(currency, exclude=EXCLUDE_FIELD_LIST))    
        
    if len(currency_list) > 0:
        game_dict['currency'] = currency_list
        
    #===========================================================================
    # store
    #===========================================================================
    
    store_dict = model_to_dict(store,exclude=EXCLUDE_FIELD_LIST)
    
    #===========================================================================
    # store resources
    #===========================================================================
    
    res_list = Resource.objects.filter(store=store)
    
    if len(res_list) > 0:
        res_dict_list =  []        
        for res in res_list:
            res_dict_list.append(model_to_dict(res, fields=['id', 'type', 'server_file_name', 'file_extension']))            
        store_dict['resources'] = res_dict_list            
    
    category_list = []
    
    #===========================================================================
    # categories
    #===========================================================================
    
    for cat in store.category_set.all().order_by('position'):
        cat_dict = model_to_dict(cat, fields=CATEGORY_ITEM_INCLUDE_FIELD_LIST)
        
        #=======================================================================
        # buy and sell prices
        #=======================================================================
        buy_price_dict = util.parse_json(cat.buy_price)
        if not util.is_none_or_empty(buy_price_dict, perform_strip=False):
            for bp in buy_price_dict:
                bp['price'] = float(bp['price'])
            cat_dict['buy_price'] = buy_price_dict
        
        sell_price_dict = util.parse_json(cat.sell_price)
        if not util.is_none_or_empty(sell_price_dict, perform_strip=False):
            for sp in sell_price_dict:
                sp['price'] = float(sp['price'])
            cat_dict['sell_price'] = sell_price_dict
        
        #=======================================================================
        # custom attributes
        #=======================================================================
        
        all_custom_attributes = store.category_attributes.all()
        aca_dict = {}
        for aca in all_custom_attributes:
            aca_val = getattr(cat, aca.mapped_column)
            if util.is_none_or_empty(aca_val):
                aca_val = 0 if aca.type == 'number' or aca.type == 'boolean' else '' 
            aca_name = lower(str(aca.name).replace(' ', '_'))
            aca_dict[aca_name] = util.get_value_by_type(aca_val, aca.type)
            
        if len(aca_dict.keys()) > 0:
            cat_dict['custom_attributes'] = aca_dict
            
        #=======================================================================
        # category resources    
        #=======================================================================
        
        res_list = Resource.objects.filter(category=cat)        
        
        if len(res_list) > 0:
            res_dict_list =  []        
            for res in res_list:
                res_dict_list.append(model_to_dict(res, fields=['id', 'type', 'server_file_name', 'file_extension']))            
            cat_dict['resources'] = res_dict_list
            
        item_list = []
        
        #=======================================================================
        # items
        #=======================================================================
        
        for item in cat.item_set.all().order_by('position'):
            item_dict = model_to_dict(item, fields=CATEGORY_ITEM_INCLUDE_FIELD_LIST)
            #=======================================================================
            # buy and sell prices
            #=======================================================================
            
            buy_price_dict = util.parse_json(item.buy_price)
            if not util.is_none_or_empty(buy_price_dict, perform_strip=False):
                for bp in buy_price_dict:
                    bp['price'] = float(bp['price'])
                item_dict['buy_price'] = buy_price_dict
            
            sell_price_dict = util.parse_json(item.sell_price)
            if not util.is_none_or_empty(sell_price_dict, perform_strip=False):
                for sp in sell_price_dict:
                    sp['price'] = float(sp['price'])
                item_dict['sell_price'] = sell_price_dict
            
            all_custom_attributes = store.item_attributes.all()
            aca_dict = {}
            for aca in all_custom_attributes:
                aca_val = getattr(item, aca.mapped_column)
                if util.is_none_or_empty(aca_val):
                    aca_val = 0 if aca.type == 'number' or aca.type == 'boolean' else '' 
                aca_name = lower(str(aca.name).replace(' ', '_'))
                aca_dict[aca_name] = util.get_value_by_type(aca_val, aca.type)
            
            if len(aca_dict.keys()) > 0:    
                item_dict['custom_attributes'] = aca_dict
                
                
            #=======================================================================
            # item resources    
            #=======================================================================
        
            res_list = Resource.objects.filter(item=item)        
            
            if len(res_list) > 0:
                res_dict_list =  []        
                for res in res_list:
                    res_dict_list.append(model_to_dict(res, fields=['id', 'type', 'server_file_name', 'file_extension']))            
                item_dict['resources'] = res_dict_list    
                                    
            item_list.append(item_dict)
            
        cat_dict['item'] = item_list
        category_list.append(cat_dict)
    
    store_dict['category'] = category_list
    game_dict['store'] = store_dict
    company_dict['game'] = game_dict
    store = None
    db.reset_queries()
    
    return util.export_json(company_dict)