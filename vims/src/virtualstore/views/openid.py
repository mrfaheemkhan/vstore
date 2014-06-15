from openid.consumer import consumer
from openid.extensions import ax
from openid.store.filestore import FileOpenIDStore
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as reverseURL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from urlparse import urljoin
from xml.dom import minidom


class OpenIDBackend(ModelBackend):

    def authenticate(self, email=None):
        try:
            user = User.objects.get(email=email)            
            return user
        except User.DoesNotExist:
            return None

def _get_base_url(req):
    """
    Given a Django web request object, returns the OpenID 'trust root'
    for that request; namely, the absolute URL to the site root which
    is serving the Django request.  The trust root will include the
    proper scheme and authority.  It will lack a port if the port is
    standard (80, 443).
    """
    name = req.META['HTTP_HOST']
    try:
        name = name[:name.index(':')]
    except:
        pass

    try:
        port = int(req.META['SERVER_PORT'])
    except:
        port = 80

    proto = req.META['SERVER_PROTOCOL']

    if 'HTTPS' in proto:
        proto = 'https'
    else:
        proto = 'http'

    if port in [80, 443] or not port:
        port = ''
    else:
        port = ':%s' % (port,)

    url = "%s://%s%s/" % (proto, name, port)
    return url

def _get_view_url(req, view_name_or_obj, args=None, kwargs=None):
    relative_url = reverseURL(view_name_or_obj, args=args, kwargs=kwargs)
    full_path = req.META.get('SCRIPT_NAME', '') + relative_url
    return urljoin(_get_base_url(req), full_path)

def openid_finish(request):
    
    try:
        
        if request.GET["openid.mode"] == 'cancel':
            raise Exception ('Login request cancelled by user.')
        storedKeys = request.session['checkKey']
        if not storedKeys:
            storedKeys = []
        if not request.GET['openid.return_to'] in storedKeys:
            raise Exception ('request tempered.')
        request.session.delete('checkKey')
        email = request.GET["openid.ext1.value.ext0"]
        user = authenticate(email = email)
        if user:
            login(request, user)            
            return HttpResponseRedirect('/company/list')
        else:
            raise Exception (email + ' not registered with VIMS, please contact VIMS admin.')
    except Exception, e:
        return HttpResponse(str(e))
        

def openid_start(request):
    try:
        openid_url = 'https://www.google.com/accounts/o8/id'
        store = FileOpenIDStore('/tmp/djopenid_c_store')
        
        c = consumer.Consumer(request.session, store)

        #may throw Discovery Exception
        auth_request = c.begin(openid_url)
        
        ax_request = ax.FetchRequest()
        ax_request.add(ax.AttrInfo("http://axschema.org/contact/email", required = True))
        auth_request.addExtension(ax_request)
        
        trust_root = _get_view_url(request, openid_start)
        #trust_root = "http://127.0.0.1:8000"
        return_to = _get_view_url(request, openid_finish)
        
        if auth_request.shouldSendRedirect():
            url = auth_request.redirectURL(trust_root, return_to)
            return HttpResponseRedirect(url)
        else:
            # Beware: this renders a template whose content is a form
            # and some javascript to submit it upon page load.  Non-JS
            # users will have to click the form submit button to
            # initiate OpenID authentication.
            form_id = 'openid_message'
            form_html = auth_request.formMarkup(trust_root, return_to,
                                                False, {'id': form_id})
            
            
            
            #hide submit button
            tree = minidom.parseString(form_html)
            inputs = tree.getElementsByTagName("input")
            #required for response verification
            checkKey = []
            
            if request.session.has_key("checkKey"):
                checkKey = request.session["checkKey"] 
                
            for element in inputs:
                if element.getAttribute("type") == "submit":
                    element.setAttribute("style" , "display:none;")
                elif element.getAttribute("name") == "openid.return_to":
                    checkKey.insert(len(checkKey), element.getAttribute("value"))                    
            if checkKey:
                request.session["checkKey"] = checkKey
                
            form_html = tree.toxml()
            auth_request.getMessage(trust_root, return_to, False)
            
            return render_to_response("openid/request_form.html", {'html': form_html})


    except Exception, e:
            return HttpResponse("Error : " + str(e))

    return HttpResponse()

def localLogout(request):
    user = request.user
    username = ''
    email = ''
    try:
        username = user.username
        email = user.email   
        logout(request)
    except:
        pass        
    return render_to_response("openid/logout.html", {'username': username, 'email':email})