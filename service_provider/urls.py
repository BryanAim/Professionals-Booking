from unicodedata import name
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .pres_pdf import prescription_pdf

# from . --> same directory
# Views functions and urls must be linked. # of views == # of urls
# App URL file - urls related to service_provider


urlpatterns = [
    path('', views.service_provider_home, name='service_provider_home'),
    path('search/', views.search, name='search'),
    path('change-password/<int:pk>', views.change_password, name='change-password'),
    path('add-billing/', views.add_billing, name='add-billing'),
    path('appointments/', views.appointments, name='appointments'),
    path('edit-billing/', views.edit_billing, name='edit-billing'),
    path('edit-prescription/', views.edit_prescription, name='edit-prescription'),
    # path('forgot-password/', views.forgot_password,name='forgot-password'),
    path('client-dashboard/',views.client_dashboard, name='client-dashboard'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('profile-settings/',views.profile_settings, name='profile-settings'),
    path('about-us/', views.about_us, name='about-us'),
    path('client-register/', views.client_register, name='client-register'),
    path('logout/', views.logoutUser, name='logout'),
    path('multiple-service_provider/', views.multiple_service_provider, name='multiple-service_provider'),
    path('chat/<int:pk>/', views.chat, name='chat'),
    path('chat-professional/', views.chat_professional, name='chat-professional'),
    path('service_provider-profile/<int:pk>/', views.service_provider_profile, name='service_provider-profile'),
    path('checkout-payment/', views.checkout_payment, name='checkout-payment'),
    path('shop/', views.store_shop, name='store_shop'),
    path('data-table/', views.data_table, name='data-table'),
    path('testing/',views.testing, name='testing'),
    path('service_provider-profession-list/<int:pk>/', views.ServiceType_list, name='service_provider-profession-list'),
    path('service_provider-professional-list/<int:pk>/', views.service_provider_professional_list, name='service_provider-professional-list'),
    path('service_provider-professional-register/<int:pk>/', views.service_provider_professional_register, name='service_provider-professional-register'),
    path('view-report/<int:pk>', views.view_report, name='view-report'),
    path('test-cart/<int:pk>/', views.test_cart, name='test-cart'),
    path('prescription-view/<int:pk>', views.prescription_view, name='prescription-view'),
    path('pres_pdf/<int:pk>/',views.prescription_pdf, name='pres_pdf'),
    path('test-single/<int:pk>/', views.test_single, name='test-single'),
    path('test-remove-cart/<int:pk>/', views.test_remove_cart, name='test-remove-cart'),
    path('test-add-to-cart/<int:pk>/<int:pk2>/', views.test_add_to_cart, name='test-add-to-cart'),
    path('delete-prescription/<int:pk>/', views.delete_prescription, name='delete-prescription'),
    path('delete-report/<int:pk>/', views.delete_report, name='delete-report'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
