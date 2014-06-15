from django.db import models
from virtualstore.common import constants

# Create your models here.

class Company(models.Model):
    
    id = models.CharField(db_column ='company_id',
                          max_length=32, 
                          primary_key=True, 
                          unique=True, 
                          null=False, 
                          blank=False)
    
    name = models.CharField(max_length=255,
                            unique = True,
                            null = False,
                            blank = False)
    
    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)
    
    def __unicode__(self):
        return u'%s : %s' % (self.id, self.name)

    class Meta:
        db_table = 'company'
        
class Game(models.Model):
    id = models.CharField(db_column ='game_id',
                          max_length=32, 
                          primary_key=True,
                          null=False, 
                          blank=False)
    
    company = models.ForeignKey(Company)
    
    name = models.CharField(max_length=100,
                            unique=True,
                            null=False,
                            blank=False)
    
    visible_id = models.IntegerField(max_length=11,
                                  null=False,
                                  blank=False)
    
    is_active = models.BooleanField(default=True,
                                    null=False)
    
    web_service_url = models.URLField(max_length=1000,
                                      null=False,
                                      blank=False)
    
    item_store_url = models.URLField(max_length=1000,
                                      null=False,
                                      blank=False)
    
    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)
    
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.company.name)
    
    class Meta:
        db_table = 'game'
        unique_together = (('company', 'name'),
                           ('company', 'visible_id'))

class CustomAttribute(models.Model):
    id          = models.AutoField(primary_key=True, db_column="custom_attribute_id")
    game        = models.ForeignKey(Game)
    name        = models.CharField(max_length=100)
    type        = models.CharField(max_length=50,choices=constants.CUSTOM_ATTRIBUTE_TYPES)
    mapped_column = models.CharField(max_length=13)
    type_meta_data = models.CharField(max_length=500, blank=True, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)
    
    class Meta:
        db_table = 'custom_attribute'
        unique_together = ('game', 'name')        

class Store(models.Model):
    id = models.AutoField(db_column='store_id', 
                          primary_key=True, 
                          max_length=11)
    
    game = models.ForeignKey(Game)
    
    name = models.CharField(max_length=100,
                            null=False,
                            blank=False)
    
    visible_id = models.IntegerField(max_length=11,
                                  null=False,
                                  blank=False)
    
    is_active = models.BooleanField(default=True,
                                    null=False)
    
    position    = models.IntegerField(null=False, 
                                      blank=False)
                                      
    min_version  = models.CharField(max_length=50, 
                                    null=False, 
                                    default='1.0')
    
    max_version  = models.CharField(max_length=50, 
                                    null=True, 
                                    blank=True)
    
    category_attributes = models.ManyToManyField(CustomAttribute, 
                                                 related_name="category_attributes_set", 
                                                 db_table='category_attributes', 
                                                 blank=True)
    
    item_attributes = models.ManyToManyField(CustomAttribute, 
                                                 related_name="item_attributes_set", 
                                                 db_table='item_attributes', 
                                                 blank=True)
    
    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)
    
    version     = models.IntegerField(blank=True, default=1)
    
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.company.name)
    
    class Meta:
        db_table = 'store'
        unique_together = (('game', 'name'),
                           ('game', 'visible_id'))

class Category(models.Model):

    id          = models.AutoField(primary_key=True, 
                                   db_column='category_id')
    
    store       = models.ForeignKey(Store)
    
    name        = models.CharField(max_length = 100)
    
    description = models.CharField(max_length = 500,
                                   blank=True)
    
    visible_id = models.IntegerField(max_length=11,
                                       null=False,
                                       blank=False)
    
    position = models.IntegerField(null=False, 
                                   blank=False)    
    
    is_active = models.BooleanField(default=True,
                                    null=False)
    
    
    is_local = models.BooleanField(null=False, 
                                   default=True)
    
    is_new = models.BooleanField(null=False, 
                                 default=True)
    
    min_version  = models.CharField(max_length=50, 
                                    null=False, 
                                    default='1.0')
    
    max_version  = models.CharField(max_length=50, 
                                    null=True, 
                                    blank=True)
    
    visible_to   = models.CharField(max_length=10, 
                                    choices=constants.ENTITY_VISIBILITY_OPTIONS, 
                                    null=False, 
                                    default='dev')
    
    active_campaign = models.CharField(max_length=100, 
                                     default='default',
                                     editable=False)
    
    buy_price    = models.TextField(blank=True)
    
    sell_price    = models.TextField(blank=True)

    attribute_1    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_2    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_3    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_4    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_5    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_6    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_7    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_8    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_9    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_10   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_11   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_12   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_13   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_14   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_15   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_16   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_17   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_18   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_19   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_20   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_21   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_22   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_23   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_24   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_25   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_26   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_27   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_28   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_29   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_30   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_31   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_32   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_33   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_34   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_35   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_36   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_37   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_38   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_39   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_40   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_41   = models.TextField(null=True, blank=True)
    attribute_42   = models.TextField(null=True, blank=True)
    attribute_43   = models.TextField(null=True, blank=True)
    attribute_44   = models.TextField(null=True, blank=True)
    attribute_45   = models.TextField(null=True, blank=True)
    attribute_46   = models.TextField(null=True, blank=True)
    attribute_47   = models.TextField(null=True, blank=True)
    attribute_48   = models.TextField(null=True, blank=True)
    attribute_49   = models.TextField(null=True, blank=True)
    attribute_50   = models.TextField(null=True, blank=True)
    attribute_51   = models.TextField(null=True, blank=True)
    attribute_52   = models.TextField(null=True, blank=True)
    attribute_53   = models.TextField(null=True, blank=True)
    attribute_54   = models.TextField(null=True, blank=True)
    attribute_55   = models.TextField(null=True, blank=True)
    attribute_56   = models.TextField(null=True, blank=True)
    attribute_56   = models.TextField(null=True, blank=True)
    attribute_57   = models.TextField(null=True, blank=True)
    attribute_58   = models.TextField(null=True, blank=True)
    attribute_59   = models.TextField(null=True, blank=True)
    attribute_60   = models.TextField(null=True, blank=True)
    attribute_61   = models.TextField(null=True, blank=True)
    attribute_62   = models.TextField(null=True, blank=True)
    attribute_63   = models.TextField(null=True, blank=True)
    attribute_64   = models.TextField(null=True, blank=True)
    attribute_65   = models.TextField(null=True, blank=True)
    attribute_66   = models.TextField(null=True, blank=True)
    attribute_66   = models.TextField(null=True, blank=True)
    attribute_67   = models.TextField(null=True, blank=True)
    attribute_68   = models.TextField(null=True, blank=True)
    attribute_69   = models.TextField(null=True, blank=True)
    attribute_70   = models.TextField(null=True, blank=True)
    attribute_71   = models.TextField(null=True, blank=True)
    attribute_72   = models.TextField(null=True, blank=True)
    attribute_73   = models.TextField(null=True, blank=True)
    attribute_74   = models.TextField(null=True, blank=True)
    attribute_75   = models.TextField(null=True, blank=True)
    attribute_76   = models.TextField(null=True, blank=True)
    attribute_76   = models.TextField(null=True, blank=True)
    attribute_77   = models.TextField(null=True, blank=True)
    attribute_78   = models.TextField(null=True, blank=True)
    attribute_79   = models.TextField(null=True, blank=True)
    attribute_80   = models.TextField(null=True, blank=True)
    attribute_81   = models.TextField(null=True, blank=True)
    attribute_82   = models.TextField(null=True, blank=True)
    attribute_83   = models.TextField(null=True, blank=True)
    attribute_84   = models.TextField(null=True, blank=True)
    attribute_85   = models.TextField(null=True, blank=True)
    attribute_86   = models.TextField(null=True, blank=True)
    attribute_86   = models.TextField(null=True, blank=True)
    attribute_87   = models.TextField(null=True, blank=True)
    attribute_88   = models.TextField(null=True, blank=True)
    attribute_89   = models.TextField(null=True, blank=True)
    attribute_90   = models.TextField(null=True, blank=True)
    attribute_91   = models.TextField(null=True, blank=True)
    attribute_92   = models.TextField(null=True, blank=True)
    attribute_93   = models.TextField(null=True, blank=True)
    attribute_94   = models.TextField(null=True, blank=True)
    attribute_95   = models.TextField(null=True, blank=True)
    attribute_96   = models.TextField(null=True, blank=True)
    attribute_96   = models.TextField(null=True, blank=True)
    attribute_97   = models.TextField(null=True, blank=True)
    attribute_98   = models.TextField(null=True, blank=True)
    attribute_99   = models.TextField(null=True, blank=True)
    attribute_100   = models.TextField(null=True, blank=True)


    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)
    
    version     = models.IntegerField(blank=True, 
                                      default=1)


    class Meta:
        db_table = 'category'
        unique_together = (('store', 'name'),
                           ('store', 'visible_id'))
        
class Item(models.Model):

    id          = models.AutoField(primary_key=True, 
                                   db_column='item_id')
    
    category       = models.ForeignKey(Category)
    
    name        = models.CharField(max_length = 100)
    
    description = models.CharField(max_length = 500,
                                   blank=True)
    
    visible_id = models.IntegerField(max_length=11,
                                       null=False,
                                       blank=False)
    
    position = models.IntegerField(null=False, 
                                   blank=False)    
    
    is_active = models.BooleanField(default=True,
                                    null=False)
    
    
    is_local = models.BooleanField(null=False, 
                                   default=True)
    
    is_new = models.BooleanField(null=False, 
                                 default=True)
    
    min_version  = models.CharField(max_length=50, 
                                    null=False, 
                                    default='1.0')
    
    max_version  = models.CharField(max_length=50, 
                                    null=True, 
                                    blank=True)
    
    visible_to   = models.CharField(max_length=10, 
                                    choices=constants.ENTITY_VISIBILITY_OPTIONS, 
                                    null=False, 
                                    default='dev')
    
    active_campaign = models.CharField(max_length=100, 
                                     default='default',
                                     editable=False)
    
    buy_price    = models.TextField(blank=True)
    
    sell_price    = models.TextField(blank=True)

    attribute_1    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_2    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_3    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_4    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_5    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_6    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_7    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_8    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_9    = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_10   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_11   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_12   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_13   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_14   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_15   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_16   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_17   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_18   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_19   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_20   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_21   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_22   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_23   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_24   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_25   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_26   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_27   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_28   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_29   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_30   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_31   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_32   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_33   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_34   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_35   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_36   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_37   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_38   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_39   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_40   = models.CharField(max_length=constants.CUSTOM_ATTRIBUTE_SIZE, null=True, blank=True)
    attribute_41   = models.TextField(null=True, blank=True)
    attribute_42   = models.TextField(null=True, blank=True)
    attribute_43   = models.TextField(null=True, blank=True)
    attribute_44   = models.TextField(null=True, blank=True)
    attribute_45   = models.TextField(null=True, blank=True)
    attribute_46   = models.TextField(null=True, blank=True)
    attribute_47   = models.TextField(null=True, blank=True)
    attribute_48   = models.TextField(null=True, blank=True)
    attribute_49   = models.TextField(null=True, blank=True)
    attribute_50   = models.TextField(null=True, blank=True)
    attribute_51   = models.TextField(null=True, blank=True)
    attribute_52   = models.TextField(null=True, blank=True)
    attribute_53   = models.TextField(null=True, blank=True)
    attribute_54   = models.TextField(null=True, blank=True)
    attribute_55   = models.TextField(null=True, blank=True)
    attribute_56   = models.TextField(null=True, blank=True)
    attribute_56   = models.TextField(null=True, blank=True)
    attribute_57   = models.TextField(null=True, blank=True)
    attribute_58   = models.TextField(null=True, blank=True)
    attribute_59   = models.TextField(null=True, blank=True)
    attribute_60   = models.TextField(null=True, blank=True)
    attribute_61   = models.TextField(null=True, blank=True)
    attribute_62   = models.TextField(null=True, blank=True)
    attribute_63   = models.TextField(null=True, blank=True)
    attribute_64   = models.TextField(null=True, blank=True)
    attribute_65   = models.TextField(null=True, blank=True)
    attribute_66   = models.TextField(null=True, blank=True)
    attribute_66   = models.TextField(null=True, blank=True)
    attribute_67   = models.TextField(null=True, blank=True)
    attribute_68   = models.TextField(null=True, blank=True)
    attribute_69   = models.TextField(null=True, blank=True)
    attribute_70   = models.TextField(null=True, blank=True)
    attribute_71   = models.TextField(null=True, blank=True)
    attribute_72   = models.TextField(null=True, blank=True)
    attribute_73   = models.TextField(null=True, blank=True)
    attribute_74   = models.TextField(null=True, blank=True)
    attribute_75   = models.TextField(null=True, blank=True)
    attribute_76   = models.TextField(null=True, blank=True)
    attribute_76   = models.TextField(null=True, blank=True)
    attribute_77   = models.TextField(null=True, blank=True)
    attribute_78   = models.TextField(null=True, blank=True)
    attribute_79   = models.TextField(null=True, blank=True)
    attribute_80   = models.TextField(null=True, blank=True)
    attribute_81   = models.TextField(null=True, blank=True)
    attribute_82   = models.TextField(null=True, blank=True)
    attribute_83   = models.TextField(null=True, blank=True)
    attribute_84   = models.TextField(null=True, blank=True)
    attribute_85   = models.TextField(null=True, blank=True)
    attribute_86   = models.TextField(null=True, blank=True)
    attribute_86   = models.TextField(null=True, blank=True)
    attribute_87   = models.TextField(null=True, blank=True)
    attribute_88   = models.TextField(null=True, blank=True)
    attribute_89   = models.TextField(null=True, blank=True)
    attribute_90   = models.TextField(null=True, blank=True)
    attribute_91   = models.TextField(null=True, blank=True)
    attribute_92   = models.TextField(null=True, blank=True)
    attribute_93   = models.TextField(null=True, blank=True)
    attribute_94   = models.TextField(null=True, blank=True)
    attribute_95   = models.TextField(null=True, blank=True)
    attribute_96   = models.TextField(null=True, blank=True)
    attribute_96   = models.TextField(null=True, blank=True)
    attribute_97   = models.TextField(null=True, blank=True)
    attribute_98   = models.TextField(null=True, blank=True)
    attribute_99   = models.TextField(null=True, blank=True)
    attribute_100   = models.TextField(null=True, blank=True)

    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)
    
    version     = models.IntegerField(blank=True, 
                                      default=1)


    class Meta:
        db_table = 'item'
        unique_together = (('category', 'name'),
                           ('category', 'visible_id'))        


class Currency(models.Model):
    
    id          = models.AutoField(primary_key=True, 
                                   db_column='currency_id')
    
    game        = models.ForeignKey(Game)
    
    name        = models.CharField(max_length=100)
    
    is_active    = models.BooleanField(null=False, 
                                       default=True)

    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)
    
    modified_datetime = models.DateTimeField(auto_now=True,
                                             editable=False, 
                                             null=False, 
                                             blank=True)
    
    modified_by = models.IntegerField(max_length=11, 
                                      null=False, 
                                      blank=True)

    class Meta:
        db_table = 'game_currency'
        unique_together = ('game', 'name')
        
class Resource(models.Model):
    id = models.CharField(db_column ='resource_id',
                          max_length=10, 
                          primary_key=True, 
                          unique=True, 
                          null=False, 
                          blank=False)
    store           =   models.ForeignKey(Store, 
                                          null=True, 
                                          blank=True)
    
    category        =   models.ForeignKey(Category, 
                                          null=True, 
                                          blank=True)
    
    item       =   models.ForeignKey(Item, 
                                     null=True, 
                                     blank=True)
    
    type       =   models.CharField(max_length = 20, 
                                         choices=constants.RESOURCE_UPLOAD_TYPE) # type of resource
    
    file_extension   =   models.CharField(max_length = 20)  # png / jpg / zip
    
    file_name        =   models.CharField(max_length = 100) # 1 .png
    
    server_file_path =   models.CharField(max_length=500, 
                                          null=True, 
                                          blank=True)
    
    server_file_name  =   models.CharField(max_length=100, 
                                           null=True, 
                                           blank=True)

    created_datetime = models.DateTimeField(auto_now_add=True, 
                                            editable=False, 
                                            null=False, 
                                            blank=False)
    
    created_by = models.IntegerField(max_length=11, 
                                     null=False, 
                                     blank=False)

    def __unicode__(self):
        return u'Id: %s, GAEKey: %s, File: %s.%s' % (self.id, self.imageGAEKey, self.imageFilename, self.imageFiletype)

    class Meta:
        db_table = 'resources'
        unique_together = (('store', 'type'),
                           ('category', 'type'),                           
                           ('item', 'type'))

class StoreXml(models.Model):
    id = models.IntegerField(max_length=11,
                             primary_key=True,
                             unique=True)
    
    text_data = models.TextField()
    
    binary_data = models.TextField()
    
    created_datetime = models.DateTimeField(auto_now_add=True)
    
    modified_datetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'store_xml'
        
class StoreCache(models.Model):
    id = models.IntegerField(max_length=11,
                             primary_key=True,
                             unique=True)
    
    xml_data = models.TextField()
    
    xml_binary_data = models.TextField()
    
    json_data = models.TextField()
    
    json_binary_data = models.TextField()
    
    created_datetime = models.DateTimeField(auto_now_add=True)
    
    modified_datetime = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'store_cache'