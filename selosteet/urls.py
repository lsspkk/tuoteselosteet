from django.conf.urls import url

from . import views

# namespace for url names
app_name = 'selosteet'
urlpatterns = [



    # ex: /polls/import_foods
    url(r'^import_foods/$', views.import_foods, name='import_foods'),
    url(r'^import_products/$', views.import_products, name='import_products'),


    # ex: /polls/products
    url(r'^products/$', views.products, name='products'),
    # ex: /polls/5/food/
    url(r'^(?P<food_id>[0-9]+)/food/$', views.food, name='food'),
    # ex: /polls/5/product/
    url(r'^(?P<product_id>[0-9]+)/tuote/$', views.tuote, name='tuote'),
        # ex: /polls/
    url(r'^$', views.products, name='products'),

]
