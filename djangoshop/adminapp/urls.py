from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [

    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.users, name='users'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<int:pk>/', adminapp.user_delete, name='user_delete'),

    path('categories/create/', adminapp.CategoryCreate.as_view(), name='category_create'),
    path('categories/read/', adminapp.CategoryMain.as_view(), name='categories'),
    path('categories/update/<int:pk>/', adminapp.CategoryUpdate.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDelete.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/<int:vc>', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/create/category/vc/<int:pk>/', adminapp.VendorCodeCreateView.as_view(), name='vc_create'),
    path('products/read/category/<int:pk>/', adminapp.ProductByCatView.as_view(), name='products'),
    path('products/update/<int:cat>/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:cat>/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
    path('products/disable/<int:cat>/<int:pk>/', adminapp.ProductDisableView.as_view(), name='product_disable'),
]

