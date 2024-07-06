from django.urls import path
from shop.views import *
from django.conf.urls.static import static
from root import settings

urlpatterns = [
    path('', product_list, name='products'),
    path('category/<slug:category_slug>/products', product_list, name='products_of_category'),
    path('product/<slug:slug>', product_details, name='product_details'),

    # adding comments
    path('product/<slug:product_slug>/detail/add_comment', add_comment, name='comment'),

    # making orders
    path('product/<slug:slug>/detail/make_order', make_order, name='order'),

    # product actions
    path('add_product/', add_product, name='add_product'),
    path('delete_product/<slug:slug>', delete_product, name='delete_product'),
    path('update_product/<slug:slug>', update_product, name='update_product'),

    # about
    path('about/', about, name='about'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
