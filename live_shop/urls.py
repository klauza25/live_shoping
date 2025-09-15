from django.urls import path
from .views import *

urlpatterns = [
    
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', seller_dashboard, name='seller_dashboard'),
    path('add-product/', add_product, name='add_product'),
    path('become-seller/', become_seller, name='become_seller'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('products/', product_catalog, name='product_catalog'),
]
