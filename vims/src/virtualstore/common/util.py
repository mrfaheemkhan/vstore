from encodings.base64_codec import base64_encode, base64_decode
from string import lower, replace
from uuid import uuid4
from vims import settings
from virtualstore.models import Resource, Store, Category, Item
from virtualstore.services import file_zip
import json
import os
import random
import string

class Empty:
    empty = None 

def save_with_uuid(instance):
    saved = False
    
    while saved == False:
        new_uuid = uuid4().hex
        if len(new_uuid) > 32:
            new_uuid = new_uuid[len(new_uuid)-32:]
        instance.id = new_uuid
        
        try:
            instance.save()
            saved = True
        except Exception, e:
            pass   
    return saved

def save_with_pattern_key(instance, digit_count=4, char_count=4):
    saved = False
    
    while saved == False:
        digits = "".join( [random.choice(string.digits) for i in xrange(digit_count)] )
        chars = "".join( [random.choice(string.lowercase) for i in xrange(char_count)] )
        instance.id = chars+digits
        try:
            instance.save()
            saved = True
        except Exception, e:
            pass   
    return saved

def save(instance):
    saved = False
    
    try:
        instance.save()
        saved = True
    except Exception, e:
        pass   
    return saved

def extract_view_name(view):
    
    if view.rfind('/') != -1:
        view = view[view.rfind('/'):]
    
    elif view.rfind('\\') != -1:
        view = view[view.rfind('\\')+1:]
    
    if view.find('.') != -1:
        view = view[0:view.rfind('.')]
        
    if view[0] == '/':
        view = view[1:]
        
    return view

def is_none_or_empty(input_string, perform_strip=True):
    if input_string == None:
        return True
    elif not perform_strip and len(input_string) <= 0:
        return True
    elif perform_strip and len(input_string.strip()) <= 0:
        return True
    else:
        return False
    
def encode_base64(string_to_encode):
    return base64_encode(string_to_encode)[0]

def decode_base64(string_to_decode):
    return base64_decode(string_to_decode)[0]

def parse_json(json_str):
    if is_none_or_empty(json_str) == False:
        return json.loads(json_str)
    else:
        return None
    
def export_json(object_to_export):
    if object_to_export != None:
        return json.dumps(object_to_export)
    else:
        return ""

def get_float_or_default(value, default_value=None):    
    try:
        value = str(value).strip()
        value = float(value)
    except:
        return default_value
    return value

def get_custom_attribtes_widget_dict(store_obj, form, value_from_instance = True):    
    if form.instance.__class__.__name__ == 'Category':
        custom_attributes = store_obj.category_attributes.all().order_by('name')
    else:
        custom_attributes = store_obj.item_attributes.all().order_by('name')
        
    custom_attributes_dicts = []
    temp = Empty
    temp.errors = ''
    
    for ca_obj in custom_attributes:
        custom_attributes_dicts.append({'label' : ca_obj.name,
                                        'id'    : 'id_'+ca_obj.mapped_column,
                                        'name'  : ca_obj.mapped_column,
                                        'widget' : ca_obj.type,
                                        'widget_meta' : ca_obj.type_meta_data,
                                        'widget_value': getattr(form.instance, ca_obj.mapped_column) if value_from_instance else form._raw_value(ca_obj.mapped_column) ,
                                        'errors' : form._errors.get(ca_obj.mapped_column, '') if form._errors != None else ''                     
                                        })
    return custom_attributes_dicts       
    
def get_value_by_type(val, type):
    if type == 'number':
        return float(val)
    elif type == 'boolean':
        return int(val)
    elif type in ['text', 'currency', 'datetime']:
        return str(val)
    else:
        return parse_json(val)
    
def save_resource(user_id, parent_obj, parent_type, resource_type, resource_file):

    is_saved_on_server = False
    server_file_path = None
    try:
        
        full_file_name = resource_file.name
        file_name, file_extension = os.path.splitext(full_file_name)
        file_extension = file_extension[1:]
        
        resource_obj = Resource(created_by = user_id)
        resource_obj.type = resource_type
        resource_obj.file_name = resource_file.name
        resource_obj.file_extension = file_extension
        
        save_with_pattern_key(resource_obj)
        
        parent_list = []    
        if parent_type == 'store':
            parent_list.append(parent_obj.game.company.id)
            parent_list.append(parent_obj.game.id)
            resource_obj.store = parent_obj
        elif parent_type == 'category':
            parent_list.append(parent_obj.store.game.company.id)
            parent_list.append(parent_obj.store.game.id)
            parent_list.append(parent_obj.store.id)
            resource_obj.category = parent_obj
        elif parent_type == 'item':
            parent_list.append(parent_obj.category.store.game.company.id)
            parent_list.append(parent_obj.category.store.game.id)
            parent_list.append(parent_obj.category.store.id)
            parent_list.append(parent_obj.category.id)
            resource_obj.item = parent_obj
            
        parent_list.append(parent_obj.id)
        
        server_dirs = ''.join(['/' + str(parent_id) for parent_id in parent_list])
        
        if not os.path.exists(settings.UPLOADED_CONTENT_DIR+server_dirs):
            os.makedirs(settings.UPLOADED_CONTENT_DIR+server_dirs)
            
        resource_obj.file_name = file_name
        resource_obj.file_extension = file_extension
        resource_obj.server_file_path = server_dirs
        resource_obj.server_file_name = resource_obj.id+'.'+file_extension
        save(resource_obj)
        
        server_file_path = str(settings.UPLOADED_CONTENT_DIR + server_dirs + '/' + resource_obj.server_file_name)
        server_file = open(server_file_path, 'wb+')
        
        for chunk in resource_file.chunks():
            server_file.write(chunk)
        server_file.close()
        is_saved_on_server = True
            
    except Exception, e:
        try:
            resource_obj.delete()
            if is_saved_on_server:
                os.remove(server_file_path)
        except:
            pass        
        raise e

def convert_string_for_xml_tag(str_to_convert):
    if not is_none_or_empty(str_to_convert):
        return replace(lower(str_to_convert), ' ', '_')
    else:
        return ""

def boolean_to_number(boolean_val):
    if boolean_val == "True" or boolean_val == "true" or boolean_val == True:
        return '1'
    else:
        return '0'
    
def add_text_node_to_parent_node(xml_doc, parent_node, text_node_tag, text_node_data, is_boolean=False):
    if is_boolean == True:
        text_node_element = xml_doc.createElement(text_node_tag)
        text_node_element.appendChild(xml_doc.createTextNode(unicode(boolean_to_number(text_node_data))))
        parent_node.appendChild(text_node_element)
    else:
        text_node_element = xml_doc.createElement(text_node_tag)
        text_node_element.appendChild(xml_doc.createTextNode(unicode(text_node_data)))
        parent_node.appendChild(text_node_element)
    return parent_node

def add_multi_value_node_to_parent_node(xml_doc, parent_node, node_tag, node_data_keys_json, node_data_json):
    
    multi_value_parent_node = xml_doc.createElement(node_tag+'s')
    parent_node.appendChild(multi_value_parent_node)
    data_keys = parse_json(node_data_keys_json)
    data = parse_json(node_data_json)
    
    if data != None:
        for data_ele in data:
            data_node = xml_doc.createElement(node_tag)
            for key in data_keys:
                data_node.setAttribute(key, unicode(data_ele.get(key)))
            
            multi_value_parent_node.appendChild(data_node)
    return parent_node

def add_resource_node_to_parent_node(xml_doc, parent_node, res_list):
    
    res_parent_node = xml_doc.createElement('resources')
    parent_node.appendChild(res_parent_node)
    for res in res_list:
        res_node = xml_doc.createElement('resource')
        res_node.setAttribute('server_file_name', res.server_file_name)
        res_node.setAttribute('file_extension', res.file_extension)
        res_node.setAttribute('type', res.type)
        res_node.setAttribute('id', unicode(res.id))
        
        res_parent_node.appendChild(res_node)
        
    return parent_node

def make_zip_for_xml(xml_content, store_id):
    xml_path = settings.UPLOADED_TEMP_FILES_DIR + '/' + str(store_id)
    if not os.path.exists( xml_path ):
        try:
            os.makedirs( xml_path )
        except Exception, e:
            pass
    
    xml_file_name = str(store_id)+'.xml'
    
    try:
        xml_file_path = os.path.join(xml_path, xml_file_name)
        xml_file = open(xml_file_path, 'w')
        xml_file.write(xml_content)
        xml_file.close()
    except:
        pass
    
    xml_zip_path = os.path.join(xml_path, str(store_id)+'.zip')
    xml_binary = file_zip.make_zip_from_file_list(xml_zip_path, [xml_file_path])
    return xml_binary

def make_zip_for_json(json_content, store_id):
    json_path = settings.UPLOADED_TEMP_FILES_DIR + '/' + str(store_id)
    if not os.path.exists( json_path ):
        try:
            os.makedirs( json_path )
        except Exception, e:
            pass
    
    json_file_name = str(store_id)+'.json'
    
    try:
        json_file_path = os.path.join(json_path, json_file_name)
        json_file = open(json_file_path, 'w')
        json_file.write(json_content)
        json_file.close()
    except:
        pass
    
    json_zip_path = os.path.join(json_path, str(store_id)+'.zip')
    json_binary = file_zip.make_zip_from_file_list(json_zip_path, [json_file_path])
    return json_binary

def make_breeded_dropdown(parent):
    stores = []
    dropdown_data = {}
    custom_att = None
    temp_store = Store.objects.filter(game=parent.store.game, name='Fish').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    temp_store = Store.objects.filter(game=parent.store.game, name='Breeded Fish').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    for store in stores:
        custom_att = store.item_attributes.filter(name='can_be_breeded')
        if len(custom_att) > 0:
            custom_att = custom_att[0].mapped_column
        else:
            custom_att = None
        categories = Category.objects.filter(store=store)
        for cat in categories:
            items = Item.objects.filter(category=cat)
            for item in items:
                if getattr(item, custom_att) is not None and getattr(item, custom_att) == '1':
                    dropdown_data[item.name+" - "+cat.name] = "_".join([str(store.visible_id), str(cat.visible_id), str(item.visible_id)])

    return export_json(dropdown_data)


def make_dailybonus_dropdown(parent):
    stores = []
    dropdown_data = {}
    temp_store = Store.objects.filter(game=parent.store.game, name='Fish').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    temp_store = Store.objects.filter(game=parent.store.game, name='Plants').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    temp_store = Store.objects.filter(game=parent.store.game, name='Decoration').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    temp_store = Store.objects.filter(game=parent.store.game, name='Tank Sands').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    temp_store = Store.objects.filter(game=parent.store.game, name='Background').order_by('name')
    if len(temp_store) > 0:
        stores.append(temp_store[0])
        
    for store in stores:
        categories = Category.objects.filter(store=store)
        for cat in categories:
            items = Item.objects.filter(category=cat)
            for item in items:
                if item.is_active == True:
                    dropdown_data[store.name+" - "+cat.name+" - "+item.name] = "_".join([str(store.visible_id), str(cat.visible_id), str(item.visible_id)])

    return export_json(dropdown_data)
    

#def update_store_cache(store_id):
#    store_cache_obj = None
#    store_cache_list = StoreCache.objects.filter(id=store_id)
#    
#    if len(store_cache_list) == 0:
#        store_cache_obj = StoreCache()
#        store_cache_obj.id = store_id
#    else:
#        store_cache_obj = store_cache_list[0]
#    
#    if store_cache_obj != None:
#        xml_content = virtualstore.services.store_as_xml.get_xml(store_id)
#        zipped_xml_binary = make_zip_for_xml(xml_content, store_id)
#        json_content = virtualstore.services.store_as_json.get_json(store_id)
#        zipped_json_binary = make_zip_for_json(json_content, store_id)
#        
#        store_cache_obj.xml_data = xml_content
#        store_cache_obj.xml_binary_data = binascii.hexlify(zipped_xml_binary)
#        store_cache_obj.json_data = json_content
#        store_cache_obj.json_binary_data = binascii.hexlify(zipped_json_binary)
#        store_cache_obj.save()
#        
#    return store_cache_obj