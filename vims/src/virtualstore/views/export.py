from virtualstore.common import http_util, util
from virtualstore.services import resource_download_url, cache
from virtualstore.models import StoreCache
import binascii

def json(request):    
    store_id  = request.REQUEST.get('store_id')
    json_content = None
    zipped_json_binary = None
    
    store_cache_list = StoreCache.objects.filter(id=store_id)
    
    if len(store_cache_list) == 0:
        cache_obj = cache.update_store_cache(store_id)
    else:
        cache_obj = store_cache_list[0]
        
    json_content = cache_obj.json_data
    zipped_json_binary = binascii.unhexlify(cache_obj.json_binary_data)
    store_cache_list = None
    cache_obj = None
    
    if request.GET.get('zip', False) == 'true':
        return http_util.response_with_attachment(request,
                                                  { 'file' : zipped_json_binary, 
                                                    'store_id' : store_id})
    else:
        return http_util.response_with_template(request,
                                                str(__file__), 
                                                'json', 
                                                None, 
                                                { 'json' : json_content})
    
def xml(request): 
    store_id  = request.REQUEST.get('store_id')
    xml_content = None
    zipped_xml_binary = None
    
    store_cache_list = StoreCache.objects.filter(id=store_id)
    
    if len(store_cache_list) == 0:
        cache_obj = cache.update_store_cache(store_id)
    else:
        cache_obj = store_cache_list[0]
        
    xml_content = cache_obj.xml_data
    zipped_xml_binary = binascii.unhexlify(cache_obj.xml_binary_data)
    store_cache_list = None
    cache_obj = None
        
    if request.GET.get('zip', False) == 'true':
        return http_util.response_with_attachment(request,
                                                  { 'file' : zipped_xml_binary, 
                                                    'store_id' : store_id})
    else:
        return http_util.response_with_template(request,
                                                str(__file__), 
                                                'xml', 
                                                None, 
                                                { 'xml' : xml_content})

    
def resource(request):    
    return http_util.redirect_to_url(resource_download_url.get_resource_path(request.REQUEST.get('id'))) 