from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.forms.widgets import HiddenInput, TextInput
from virtualstore.common import util, constants
from virtualstore.models import Company, Game, Store, Currency, Category, \
    Item, CustomAttribute, Resource
from datetime import datetime

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput()}
        
        exclude = ('id',)


class GameForm(ModelForm):
    class Meta:
        model = Game
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput(),
                    'company' : HiddenInput()}
        
        exclude = ('id',)
        
class StoreForm(ModelForm):    
    class Meta:
        model = Store
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput(),
                    'version' : HiddenInput(),
                    'min_version' : HiddenInput(attrs={'value':'1.0'}),
                    'max_version' : HiddenInput(), 
                    'game' : HiddenInput()}
        
        exclude = ('id',)
        
class CategoryForm(ModelForm):
    
    def __getattribute__(self, name):
        if name.startswith('clean_attribute_'):
            n = int(name[len('clean_attribute_'):])
            def f():
                return self._custom_attribute_clean(n)
            return f
        return super(CategoryForm, self).__getattribute__(name)
    
    def clean_buy_price(self):
        return _clean_price_json(self, 'buy_price')

    def clean_sell_price(self):
        return _clean_price_json(self, 'sell_price')
        
    def _custom_attribute_clean(self, mapped_column_number):
        mapped_column = 'attribute_' + str(mapped_column_number)
        data = None
        try:
            data = self.cleaned_data[mapped_column]
        except:
            return data

        obj = Store.objects.select_related().get(id=self.cleaned_data['store'].id)
        if obj != None:
            try:
                attribute_obj = obj.category_attributes.filter(mapped_column=str(mapped_column)).get()
            except Exception:
                return data

            if attribute_obj.type == "number":
                if util.is_none_or_empty(data):
                    return data
                try:
                    float(data)
                except ValueError:
                    raise ValidationError("Enter a number.")

            elif attribute_obj.type == "boolean":
                if data != '0' and data != '1':
                    raise ValidationError("Boolean can be True or False.")

            elif attribute_obj.type == 'datetime':
                try:
                    datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    raise forms.ValidationError("Invalid DateTime format.")

            elif attribute_obj.type == 'currency':
                if Currency.objects.filter(name=data, game=obj.game).count() == 0:
                    raise ValidationError("Currency is not valid for this Game.")
        return data
    
    class Meta:
        model = Category
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput(),
                    'version' : HiddenInput(),
                    'store' : HiddenInput(),
                    'min_version' : HiddenInput(attrs={'value':'1.0'}),
                    'max_version' : HiddenInput(),
                    'visible_to' : HiddenInput(attrs={'value':'dev'}),
                    'buy_price' : TextInput(attrs={'readonly':True}),
                    'sell_price' : TextInput(attrs={'readonly':True})}
        
        exclude = ('id',)

class ItemForm(ModelForm):
    def __getattribute__(self, name):
        if name.startswith('clean_attribute_'):
            n = int(name[len('clean_attribute_'):])
            def f():
                return self._custom_attribute_clean(n)
            return f
        return super(ItemForm, self).__getattribute__(name)
    
    def clean_buy_price(self):
        return _clean_price_json(self, 'buy_price')

    def clean_sell_price(self):
        return _clean_price_json(self, 'sell_price')
        
    def _custom_attribute_clean(self, mapped_column_number):
        mapped_column = 'attribute_' + str(mapped_column_number)
        data = None
        try:
            data = self.cleaned_data[mapped_column]
        except:
            return data

        obj = Category.objects.select_related().get(id=self.cleaned_data['category'].id)
        if obj != None:
            try:
                attribute_obj = obj.store.category_attributes.filter(mapped_column=str(mapped_column)).get()
            except Exception:
                return data

            if attribute_obj.type == "number":
                if util.is_none_or_empty(data):
                    return data
                try:
                    float(data)
                except ValueError:
                    raise ValidationError("Enter a number.")

            elif attribute_obj.type == "boolean":
                if data != '0' and data != '1':
                    raise ValidationError("Boolean can be True or False.")

            elif attribute_obj.type == 'datetime':
                try:
                    datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    raise forms.ValidationError("Invalid DateTime format.")

            elif attribute_obj.type == 'currency':
                if Currency.objects.filter(name=data, game=obj.store.game).count() == 0:
                    raise ValidationError("Currency is not valid for this Game.")
        return data
    
    class Meta:
        model = Item
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput(),
                    'version' : HiddenInput(),
                    'category' : HiddenInput(),
                    'min_version' : HiddenInput(attrs={'value':'1.0'}),
                    'max_version' : HiddenInput(),
                    'visible_to' : HiddenInput(attrs={'value':'dev'}),
                    'buy_price' : TextInput(attrs={'readonly':True}),
                    'sell_price' : TextInput(attrs={'readonly':True})}
        
        exclude = ('id',)
        
class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput(),
                    'game' : HiddenInput()}
        
        exclude = ('id',)
        
class CustomAttributeForm(ModelForm):
    def clean_type_meta_data(self):
        meta_data_json = self.cleaned_data['type_meta_data']
        
        if(util.is_none_or_empty(meta_data_json)):
            return meta_data_json
        else:
            sub_attribute_names = util.parse_json(meta_data_json)        
            for index, san in enumerate(sub_attribute_names):
                try:
                    if sub_attribute_names.index(san) != index or sub_attribute_names[::-1].index(san) != (len(sub_attribute_names) - index - 1):
                        raise ValidationError('Sub attribute names should be unique')
                except ValueError, e:
                    pass
            
            
        return meta_data_json
    class Meta:
        model = CustomAttribute
        widgets = { 'created_by' : HiddenInput(),
                    'modified_by' : HiddenInput(),
                    'game' : HiddenInput(),
                    'type_meta_data' : HiddenInput()}
        
        exclude = ('id','mapped_column')
        
def _clean_price_json(form, price_type):

    price_label = None
    campaign_label = None
    if price_type == 'buy_price':
        price_label = 'buy'
        campaign_label = 'same campaign'
    elif price_type == 'sell_price':
        price_label = 'sell'
        campaign_label = 'sell price'
    else:
        raise Exception("Invalid price_type.")

    price_json = None
    try:
        price_json = form.cleaned_data[price_type]
        if util.is_none_or_empty(price_json):
            return price_json
    except:
        return form.cleaned_data[price_type]

    buy_price_array = None
    try:
        buy_price_array = util.parse_json(price_json)
    except:
        raise ValidationError("Invalid %s price" % price_label)


    campaign_currency_dict = {}
    for buy_price in buy_price_array:
        currency = buy_price['currency']
        campaign = buy_price.get('campaign', 'sell_price')

        if not campaign_currency_dict.has_key(campaign):
            campaign_currency_dict[campaign] = [currency]
        else:
            currnciesList = campaign_currency_dict[campaign]
            if currency in currnciesList:
                raise ValidationError("Same currency can not be repeated in %s." % (campaign_label, ))
            currnciesList.append(currency)

        price = util.get_float_or_default(buy_price['price'])
        # Not checking for positive values
        if price == None:
            raise ValidationError("Price can only be a number.")

        int_price = int(price)
        significant_decimal = price - int_price
        if  significant_decimal == 0.0:
            price = int_price

        buy_price['price'] = str(price)

    price_json = util.export_json(buy_price_array)
    return price_json

class ResourceUploadForm(forms.Form):
    resource_id = forms.CharField(max_length=50, 
                                  required=False)
    
    file = forms.FileField(required=True)
    
    type = forms.ChoiceField(choices=constants.RESOURCE_UPLOAD_TYPE)
    
    parent = forms.CharField(max_length=50)
    
    parent_type = forms.CharField(max_length=50)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        
        parent = cleaned_data['parent']
        parent_type = cleaned_data['parent_type']
        resource_type = cleaned_data['type']
        
        if parent_type == 'store':
            res_list = Resource.objects.filter(store=str(parent), type=resource_type)
        elif parent_type == 'category':
            res_list = Resource.objects.filter(category=str(parent), type=resource_type)
        else:
            res_list = Resource.objects.filter(item=str(parent), type=resource_type)
        
        if len(res_list) > 0:
            raise ValidationError('Resource of type '+resource_type+' already exists.')
        
        resource_file = cleaned_data['file']
        
        if resource_file.size/1024 > constants.RESOURCE_UPLOAD_MAX_SIZE_KB:
            raise ValidationError('Maximum allowed file size is '+str(constants.RESOURCE_UPLOAD_MAX_SIZE_KB)+'KB')
        
        return cleaned_data
    
    class Meta:
        widgets = { 'parent' : HiddenInput(),
                    'parent_type' : HiddenInput(),
                    'resource_id' : HiddenInput()
                  }
        