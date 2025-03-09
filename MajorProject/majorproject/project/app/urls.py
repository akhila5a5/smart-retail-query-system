from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('uploadproducts/', views.uploadproducts, name='uploadproducts'),
    path('products/', views.products, name='products'),
    path('productdetails/<int:id>/', views.productdetails, name='productdetails'),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('removefromcart/<int:id>/', views.removefromcart, name='removefromcart'),
    path('search_products/', views.search_products, name='search_products'),
    path('cart/', views.cart, name='cart'),
    path('buyproduct/<int:id>/', views.buyproduct, name='buyproduct'),
    path('order/<int:id>/', views.order, name='order'),
    path('vieworders/', views.vieworders, name='vieworders'),
    path('myorders/', views.myorders, name='myorders'),
    path('reject/<int:id>/', views.reject, name='reject'),
    path('accept/<int:id>/', views.accept, name='accept'),
    path('search/', views.search, name='search'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),





]
