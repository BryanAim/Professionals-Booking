from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.admin_login, name='admin-login'),
    path('admin-dashboard/',views.admin_dashboard, name='admin-dashboard'),
    path('service_provider-admin-profile/<int:pk>/', views.service_provider_admin_profile,name='service_provider-admin-profile'),
    path('appointment-list',views.appointment_list, name='appointment-list'),
    path('register-professional-list/', views.register_professional_list,name='register-professional-list'),
    path('pending-professional-list/', views.pending_professional_list,name='pending-professional-list'),
    path('forgot-password/', views.admin_forgot_password,name='admin_forgot_password'),
    path('service_provider-list/', views.service_provider_list,name='service_provider-list'),
    path('add-service_provider/', views.add_service_provider,name='add-service_provider'),
    path('edit-service_provider/<int:pk>/', views.edit_service_provider,name='edit-service_provider'),
    path('delete-service_provider/<int:pk>/', views.delete_service_provider,name='delete-service_provider'),
    path('service_provider-list/', views.service_provider_list,name='service_provider-list'),
    path('add-pharmacist/', views.add_pharmacist,name='add-pharmacist'),
    #path('edit-service_provider/', views.edit_service_provider,name='edit-service_provider'),
    path('invoice/',views.invoice, name='invoice'),
    path('invoice-report/',views.invoice_report, name='invoice_report'),
    path('lock-screen/', views.lock_screen,name='lock_screen'),
    path('login/',views.admin_login,name='admin_login'),
    path('client-list/',views.client_list, name='client-list'),
    # path('register/', views.register,name='register'),
    path('admin_register/',views.admin_register,name='admin_register'),
    path('transactions-list/',views.transactions_list, name='transactions_list'),
    path('admin-logout/', views.logoutAdmin, name='admin-logout'),
    path('emergency/', views.emergency_details,name='emergency'),
    path('edit-emergency-information/<int:pk>/', views.edit_emergency_information,name='edit-emergency-information'),
    path('service_provider-profile/', views.service_provider_profile ,name='service_provider-profile'),
    path('service_provider-admin-profile/<int:pk>/', views.service_provider_admin_profile,name='service_provider-admin-profile'),
    path('create-invoice/<int:pk>/', views.create_invoice,name='create-invoice'),
    path('create-report/<int:pk>/', views.create_report,name='create-report'),
    path('add-lab-worker/', views.add_lab_worker,name='add-lab-worker'),
    path('lab-worker-list/', views.view_lab_worker,name='lab-worker-list'),
    path('edit-lab-worker/<int:pk>/', views.edit_lab_worker,name='edit-lab-worker'),
    path('product-list/', views.product_list,name='product-list'),
    path('add-product/', views.add_product,name='add-product'),
    path('edit-product/<int:pk>/', views.edit_product,name='edit-product'),
    path('delete-product/<int:pk>/', views.delete_product,name='delete-product'),
    path('service_type-image-list/<int:pk>', views.service_type_image_list,name='service_type-image-list'),
    path('admin-professional-profile/<int:pk>/', views.admin_professional_profile,name='admin-professional-profile'),
    path('accept-professional/<int:pk>/', views.accept_professional,name='accept-professional'),
    path('reject-professional/<int:pk>/', views.reject_professional,name='reject-professional'),
    path('delete-service_type/<int:pk>',views.delete_service_type,name='delete-service_type'),
    path('edit-service_type/<int:pk>',views.edit_service_type,name='edit-service_type'),
    path('delete-specialization/<int:pk>/<int:pk2>/',views.delete_specialization,name='delete-specialization'),
    path('delete-service/<int:pk>/<int:pk2>/',views.delete_service,name='delete-service'),
    path('labworker-dashboard/', views.labworker_dashboard,name='labworker-dashboard'),
    path('pharmacist-list/', views.view_pharmacist,name='pharmacist-list'),
    path('edit-pharmacist/<int:pk>/', views.edit_pharmacist,name='edit-pharmacist'),
    path('myclient-list/', views.myclient_list,name='myclient-list'),
    path('prescription-list/<int:pk>', views.prescription_list,name='prescription-list'),
    path('add-test/', views.add_test,name='add-test'),
    path('test-list/', views.test_list,name='test-list'),
    path('delete-test/<int:pk>/', views.delete_test,name='delete-test'),
    path('pharmacist-dashboard/', views.pharmacist_dashboard,name='pharmacist-dashboard'),
    path('report-history/', views.report_history,name='report-history'),
    
    
]
  


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
