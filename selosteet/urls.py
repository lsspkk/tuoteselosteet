from . import views

app_name = 'selosteet'

urlpatterns = [
    re_path(r'^import_foods/$', views.import_foods, name='import_foods'),
    re_path(r'^import_products/$', views.import_products,
            name='import_products'),
    re_path(r'^products/$', views.products, name='products'),
    re_path(r'^(?P<food_id>[0-9]+)/food/$', views.food, name='food'),
    re_path(r'^(?P<product_id>[0-9]+)/tuote/$', views.tuote, name='tuote'),
    re_path(
        r'^tuote/(?P<product_id>[0-9]+)/(?P<language_code>[\w]+)/$', views.tuote2, name='tuote2'),
    re_path(
        r'^setlanguage/(?P<language_code>[\w]+)/$', views.setlanguage, name='setlanguage'),
    re_path(r'^$', views.products, name='products'),
]
