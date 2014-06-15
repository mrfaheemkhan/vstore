from virtualstore.common import util
from virtualstore.models import Store, Company, Game, Resource
from xml.dom.minidom import Document
from django import db


def get_xml(store_id):
    
    xml_doc = Document()
    store = Store()
    store = Store.objects.select_related().get(id=store_id)
    
    #add company info
    company = Company()
    company = store.game.company
    company_node = xml_doc.createElement('company')
    company_node.setAttribute('name', company.name)
    company_node.setAttribute('id', unicode(company.id))
    
    xml_doc.appendChild(company_node)
    
    # add game info
    game = Game()
    game = store.game
    game_node = xml_doc.createElement('game')
    game_node.setAttribute('name', game.name)
    game_node.setAttribute('id', unicode(game.id))
    company_node.appendChild(game_node)
    
    # add store info
    store_node = xml_doc.createElement('store')
    store_node.setAttribute('name', store.name)
    store_node.setAttribute('id', unicode(store.id))
    
    #==========================================================================
    # TODO: versioning
    #==========================================================================
    
    store_node = util.add_text_node_to_parent_node(xml_doc, store_node, 'is_active', store.is_active, True)
    store_node = util.add_text_node_to_parent_node(xml_doc, store_node, 'position', store.position)
    store_node = util.add_text_node_to_parent_node(xml_doc, store_node, 'visible_id', store.visible_id)
    
#    if not util.is_none_or_empty(store.min_version, False):
#        store_node = util.add_text_node_to_parent_node(xml_doc, store_node, 'min_version', store.min_version)
#        
#    if not util.is_none_or_empty(store.max_version, False):
#        store_node = util.add_text_node_to_parent_node(xml_doc, store_node, 'max_version', store.max_version)
        
    store_node = util.add_resource_node_to_parent_node(xml_doc, store_node, Resource.objects.filter(store=store))
    
    # add categories
    category_parent_node = xml_doc.createElement('categorys')
    store_node.appendChild(category_parent_node)
    for category in store.category_set.all().order_by('position'):
        category_node  = xml_doc.createElement('category')
        category_node.setAttribute('name', category.name)
        category_node.setAttribute('id', unicode(category.id))
        category_parent_node.appendChild(category_node)
        
        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'is_active', category.is_active, True)
        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'is_new', category.is_new, True)
        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'is_local', category.is_local, True)
        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'position', category.position)
        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'visible_id', category.visible_id)
#        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'visible_to', category.visible_to)
        category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'description', category.description)
        category_node = util.add_multi_value_node_to_parent_node(xml_doc, category_node, 'buy_price', '["currency", "price", "campaign"]', category.buy_price)
        category_node = util.add_multi_value_node_to_parent_node(xml_doc, category_node, 'sell_price', '["currency", "price"]', category.sell_price)
        
#        if not util.is_none_or_empty(category.min_version, False):
#            category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'min_version', category.min_version)
#        
#        if not util.is_none_or_empty(category.max_version, False):
#            category_node = util.add_text_node_to_parent_node(xml_doc, category_node, 'max_version', category.max_version)
            
        # add custom attributes
        custom_attribute_parent_node = xml_doc.createElement('custom_attributes')
        category_node.appendChild(custom_attribute_parent_node)
        for custom_attribute in store.category_attributes.all():
            if custom_attribute.type == 'multivalue':
                custom_attribute_parent_node = util.add_multi_value_node_to_parent_node(xml_doc, 
                                                                                        custom_attribute_parent_node, 
                                                                                        util.convert_string_for_xml_tag(custom_attribute.name),
                                                                                        custom_attribute.type_meta_data,
                                                                                        getattr(category, custom_attribute.mapped_column)
                                                                                        )
            else:
                custom_attribute_node = xml_doc.createElement(util.convert_string_for_xml_tag(custom_attribute.name))
                custom_attribute_val = getattr(category, custom_attribute.mapped_column)
                if not util.is_none_or_empty(custom_attribute_val, False):
                    custom_attribute_node.appendChild(xml_doc.createTextNode(custom_attribute_val))
                    custom_attribute_parent_node.appendChild(custom_attribute_node) 
            
        category_node = util.add_resource_node_to_parent_node(xml_doc, category_node, Resource.objects.filter(category=category))
        
        # add items
        item_parent_node = xml_doc.createElement('items')
        category_node.appendChild(item_parent_node)
        for item in category.item_set.all().order_by('position'):
            item_node  = xml_doc.createElement('item')
            item_node.setAttribute('name', item.name)
            item_node.setAttribute('id', unicode(item.id))
            item_parent_node.appendChild(item_node)
            
            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'is_active', item.is_active, True)
            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'is_new', item.is_new, True)
            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'is_local', item.is_local, True)
            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'position', item.position)
            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'visible_id', item.visible_id)
#            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'visible_to', item.visible_to)
            item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'description', item.description)
            item_node = util.add_multi_value_node_to_parent_node(xml_doc, item_node, 'buy_price', '["currency", "price", "campaign"]', item.buy_price)
            item_node = util.add_multi_value_node_to_parent_node(xml_doc, item_node, 'sell_price', '["currency", "price"]', item.sell_price)
        
            
#            if not util.is_none_or_empty(item.min_version, False):
#                item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'min_version', item.min_version)
#            
#            if not util.is_none_or_empty(item.max_version, False):
#                item_node = util.add_text_node_to_parent_node(xml_doc, item_node, 'max_version', item.max_version)
                
            # add custom attributes
            custom_attribute_parent_node = xml_doc.createElement('custom_attributes')
            item_node.appendChild(custom_attribute_parent_node)
            for custom_attribute in store.item_attributes.all():
                if custom_attribute.type == 'multivalue':
                    custom_attribute_parent_node = util.add_multi_value_node_to_parent_node(xml_doc, 
                                                                                            custom_attribute_parent_node, 
                                                                                            util.convert_string_for_xml_tag(custom_attribute.name),
                                                                                            custom_attribute.type_meta_data,
                                                                                            getattr(item, custom_attribute.mapped_column)
                                                                                            )
                else:
                    custom_attribute_node = xml_doc.createElement(util.convert_string_for_xml_tag(custom_attribute.name))
                    custom_attribute_val = getattr(item, custom_attribute.mapped_column)
                    if not util.is_none_or_empty(custom_attribute_val, False):
                        custom_attribute_node.appendChild(xml_doc.createTextNode(custom_attribute_val))
                        custom_attribute_parent_node.appendChild(custom_attribute_node)
                
            item_node = util.add_resource_node_to_parent_node(xml_doc, item_node, Resource.objects.filter(item=item)) 
    game_node.appendChild(store_node)
    store = None
    db.reset_queries()
        
    return xml_doc.toxml('utf-8')