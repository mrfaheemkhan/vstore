
from django.conf.urls import patterns, url
from vims import settings
from virtualstore.views import company, game, store, currency, category, \
    item, export, custom_attribute, resource


urlpatterns = patterns('virtualstore.views',
    url(r'^$',  company.list ),
    url(r'^company/add/$',  company.add ),
    url(r'^company/list/$',  company.list ),
    url(r'^company/edit/$',  company.edit ),
    url(r'^company/delete/$',  company.delete ),
    url(r'^game/add/$',  game.add ),
    url(r'^game/list/$',  game.list ),
    url(r'^game/edit/$',  game.edit ),
    url(r'^game/delete/$',  game.delete ),
    url(r'^store/add/$',  store.add ),
    url(r'^store/list/$',  store.list ),
    url(r'^store/edit/$',  store.edit ),
    url(r'^store/push/$',  store.push ),
    url(r'^store/delete/$',  store.delete ),
    url(r'^category/add/$',  category.add ),
    url(r'^category/list/$',  category.list ),
    url(r'^category/edit/$',  category.edit ),
    url(r'^category/delete/$',  category.delete ),
    url(r'^item/add/$',  item.add ),
    url(r'^item/list/$',  item.list ),
    url(r'^item/edit/$',  item.edit ),
    url(r'^item/delete/$',  item.delete ),
    url(r'^currency/add/$',  currency.add ),
    url(r'^currency/list/$',  currency.list ),
    url(r'^currency/edit/$',  currency.edit ),
    url(r'^custom_attribute/add/$',  custom_attribute.add ),
    url(r'^custom_attribute/list/$',  custom_attribute.list ),
    url(r'^custom_attribute/edit/$',  custom_attribute.edit ),
    url(r'^custom_attribute/delete/$',  custom_attribute.delete ),
    url(r'^resource/add/$',  resource.add ),
    url(r'^resource/list/$',  resource.list ),
    url(r'^resource/delete/$',  resource.delete ),    
    url(r'^export/json/$',  export.json ),
    url(r'^export/xml/$',  export.xml ),
    url(r'^export/resource/$',  export.resource ),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'shared/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/accounts/login/'}),
    url(r'^content/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_DIR}),
)
