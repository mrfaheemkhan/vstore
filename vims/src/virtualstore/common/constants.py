

ENTITY_VISIBILITY_OPTIONS = [('all', 'All'),
                             ('dev', 'Dev')]

CUSTOM_ATTRIBUTE_SIZE = 500

CATEGORY_DEFAULT_VISIBILE_FIELDS_FILTER_STRING = "namedescriptionvisible_idpositionis_activeis_localis_newbuy_pricesell_price"

CUSTOM_ATTRIBUTE_TYPES = [('number', 'Number'),
                          ('text', 'Text'),
                          ('datetime', 'DateTime'),
                          ('boolean', 'Boolean'),
                          ('currency', 'Currency'),
                          ('multivalue', 'Multi-Value')]

RESOURCE_UPLOAD_TYPE =    [("thumb", "Thumb"),
                            ("default_zip", "Default Zip"),
                            ("ipad_zip", "iPad Zip"),
                            ("android_zip", "Android Zip"),
                            ("ipad3_zip", "iPad3 Zip"),
                            ("sd1", "SD 1"),
                            ("hd1", "HD 1"),
                            ("sd2", "SD 2"),
                            ("hd2", "HD 2"),
                            ("thumbsd1", "Thumb SD 1"),
                            ("thumbhd1", "Thumb HD 1"),
                            ("thumbsd2", "Thumb SD 2"),
                            ("thumbhd2", "Thumb HD 2"),
                            ("store", "Store"),]

RESOURCE_UPLOAD_MAX_SIZE_KB = 100000

STORE_DISPLAY_FIELDS = {
                        "Fish" : {
                                  "__keys__" : ["buy_price", "sell_price", "can_be_breeded", "time_to_adult", "training_time", "training_bonus_percentage"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "can_be_breeded" : "boolean",
                                  "time_to_adult" : "text",
                                  "training_time" : "text",
                                  "training_bonus_percentage" : "percent",
                                  },
                        "Background" : {
                                  "__keys__" : ["buy_price", "sell_price", "happiness_points"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "happiness_points" : "text",
                                  },
                        "Decoration" : {
                                  "__keys__" : ["buy_price", "sell_price", "happiness_points"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "happiness_points" : "text",
                                  },
                        "Plants" : {
                                  "__keys__" : ["buy_price", "sell_price", "happiness_points"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "happiness_points" : "text",
                                  },
                        "Tank Sands" : {
                                  "__keys__" : ["buy_price", "sell_price", "happiness_points"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "happiness_points" : "text",
                                  },
                        "Food Brick" : {
                                  "__keys__" : ["buy_price", "sell_price", "time_to_feed"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "time_to_feed" : "text",
                                  },
                        "Breeded Fish" : {
                                  "__keys__" : ["buy_price", "sell_price", "parent_x", "parent_y", "can_be_breeded", "time_to_adult", "training_time", "training_bonus_percentage"],
                                  "buy_price" : "price",
                                  "sell_price" : "price",
                                  "parent_x" : "breed_parent",
                                  "parent_y" : "breed_parent",
                                  "can_be_breeded" : "boolean",
                                  "time_to_adult" : "text",
                                  "training_time" : "text",
                                  "training_bonus_percentage" : "percent",
                                  },
                        "Breeding Tanks" : {
                                  "__keys__" : ["buy_price"],
                                  "buy_price" : "price",
                                  },
                        "InApp" : {
                                  "__keys__" : ["description", "cost_in_dollar", "identifier", "reward_bucks", "reward_coins"],
                                  "description" : "text",
                                  "cost_in_dollar" : "text",
                                  "identifier" : "text",
                                  "reward_bucks" : "text",
                                  "reward_coins" : "text",
                                  },
                        
}