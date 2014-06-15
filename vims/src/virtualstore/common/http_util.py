from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from encodings.base64_codec import base64_encode
from virtualstore.common import util
import urllib


def response_with_template(request, view, template, form, view_data=None):
    
    view = util.extract_view_name(view)    
    params = { 'form': form,
               'view_data': view_data,
               'view_file': view,
               'view_method': template
               }
    
    if template.find('.') == -1:
        template += '.html'
    
    params.update(csrf(request))               
    return render_to_response(view+"/"+template, params, context_instance=RequestContext(request))

def redirect_to_url(url, params_dict=None):
    if params_dict != None:
        url = url+'?'+'&'.join([k+'='+urllib.quote(str(v)) for (k,v) in params_dict.items()])
    return HttpResponseRedirect(url)

def redirect_with_message(view, method, params_dict):
    view = util.extract_view_name(view)
    url = '/'+view+'/'+method+'/?'+'&'.join([k+'='+urllib.quote(str(v)) for (k,v) in params_dict.items()])
    return HttpResponseRedirect(url)

def response_with_attachment(request, params_dict):
    response = HttpResponse( params_dict['file'], content_type= 'multipart/x-zip' )
    response['Content-Disposition'] = 'attachment; filename="%s.zip"' % params_dict['store_id']
    return response