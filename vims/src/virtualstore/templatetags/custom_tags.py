from django import template
from virtualstore.common import constants, util
import json
import re

register = template.Library()

@register.filter
def get_display_html(object_in_list, field_name):
    custom_attrs = object_in_list.category.store.item_attributes.all()
    store_name = object_in_list.category.store.name
    mapped_column = None
    for ca in custom_attrs:
        if ca.name == field_name:
            mapped_column = ca.mapped_column
            break
    if mapped_column is None:
        if field_name == 'buy_price' : mapped_column = 'buy_price'
        if field_name == 'sell_price' : mapped_column = 'sell_price'
        if field_name == 'description' : mapped_column = 'description'    
    if mapped_column is not None:
        return _get_display_html(getattr(object_in_list, mapped_column), constants.STORE_DISPLAY_FIELDS[store_name][field_name], object_in_list)
    return "---"

@register.filter
def get_pretty_string(ugly_string):
    pretty_string = ""
    toks = ugly_string.split('_')
    for tok in toks:
        pretty_string += tok[0].upper()+tok[1:]+' '
    return pretty_string     

def _get_display_html(value, value_type, object=None):
    html = ""
    if util.is_none_or_empty(value, False):
        html = "---"
    else:
        if value_type == 'price':
            price_dict = json.loads(value)
            html = "<ul style='margin:0px;padding:18px'>"
            for price in price_dict:
                html += "<li>"+price["price"]+" "+price["currency"]+"</li>"
            html += "</ul>"
        elif value_type == "text":
            html = value
        elif value_type == "percent":
            html = value+" %"
        elif value_type == "boolean":
            if str(value) == "1":
                html = "Yes"
            else:
                html = "No"
        elif value_type == "breed_parent":
            breed_data = util.make_breeded_dropdown(object.category)
            if util.is_none_or_empty(breed_data):
                html = "---"
            else:
                breed_data = json.loads(breed_data)
                for key in breed_data.keys():
                    breed_data[breed_data[key]] = key
                try:
                    html = breed_data[value]
                except:
                    pass
    return html
        

    
 
