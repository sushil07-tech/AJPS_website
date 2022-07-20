from re import template
from unicodedata import name
from urllib import request
from django import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_view
from .views import *
from .forms import *

urlpatterns =[
    path('',HomeView.as_view(),name='home'),
    path('search',search_bar.as_view(),name='search'),
    path('<slug:slug>',products_by_category.as_view(),name='products_by_category'),
    path('accounts/register/',RegistrationView.as_view(),name='register'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='LoginPage.html',
    authentication_form=LoginForm),name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='home'),name='logout'),
    path('change-password/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',
    form_class=PasswordChange,success_url='/change-password/completed/'),name='changepassword'),
    path('change-password/completed/',auth_view.PasswordChangeView.as_view(template_name='changecompleted.html'),
     name='changecompleted'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',
     form_class=PasswordReset),name='resetpassword'),
    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html')
     ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
     form_class=SetPassword),name='password_reset_confirm'),
    path('password-reset-completed/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_completed.html'),
     name='password_reset_complete'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('address/',AddresView.as_view(),name='address'),
    path('add-to-cart/',Add_to_cart.as_view(),name='add_cart'),
    path('cart/',Show_cart.as_view(),name='cart'),
    path('pluscart/',Increase_Quantity.as_view(),name=''),
    path('minuscart/',Decrease_Quantity.as_view(),name=''),
    path('removeproduct/',Remove_Product.as_view(),name='rprdct'),
    path('checkout/',Checkout.as_view(),name='checkout'),
    # path('payment/',Payment.as_view(),name='payment'),
    path('place/',PlaceOrder.as_view(),name='place'),
    path('myorders/',My_Orders.as_view(),name='my_orders'),
    # path('payment/',Payment.as_view(),name='onlinepayment'),
    path('proceed-to-payment/',Razorpay.as_view(),name='razor'),
    path('detail_view/<str:t_no>',Detail_view.as_view(),name='detailview'),



    



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
