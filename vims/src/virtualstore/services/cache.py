from virtualstore.common.util import make_zip_for_xml, make_zip_for_json
from virtualstore.models import StoreCache
import binascii
from virtualstore.services import store_as_json, store_as_xml

def update_store_cache(store_id):
    store_cache_obj = None
    store_cache_list = StoreCache.objects.filter(id=store_id)
    
    if len(store_cache_list) == 0:
        store_cache_obj = StoreCache()
        store_cache_obj.id = store_id
    else:
        store_cache_obj = store_cache_list[0]
    
    if store_cache_obj:
        xml_content = store_as_xml.get_xml(store_id)
        zipped_xml_binary = make_zip_for_xml(xml_content, store_id)
        json_content = store_as_json.get_json(store_id)
        zipped_json_binary = make_zip_for_json(json_content, store_id)
        
        store_cache_obj.xml_data = xml_content
        store_cache_obj.xml_binary_data = binascii.hexlify(zipped_xml_binary)
        store_cache_obj.json_data = json_content
        store_cache_obj.json_binary_data = binascii.hexlify(zipped_json_binary)
        if len(store_cache_list) == 0:
            store_cache_obj.save(force_insert=True)
        else:
            store_cache_obj.save(force_update=True)
        
    return store_cache_obj