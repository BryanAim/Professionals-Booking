from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .pdf import report_pdf


# from . --> same directory
# Views functions and urls must be linked. # of views == # of urls
# App URL file - urls related to hospital

urlpatterns = [
    path('', views.professional_login, name='professional-login'),
    path('professional-dashboard/',views.professional_dashboard, name='professional-dashboard'),
    path('professional-profile/<int:pk>/', views.professional_profile, name='professional-profile'),
    path('professional-change-password/<int:pk>', views.professional_change_password,name='professional-change-password'),
    path('professional-profile-settings/', views.professional_profile_settings,name='professional-profile-settings'),
    path('professional-register/', views.professional_register, name='professional-register'),
    path('professional-logout/', views.logoutProfessional, name='professional-logout'),
    path('my-patients/', views.my_patients, name='my-patients'),
    path('booking/<int:pk>/', views.booking, name='booking'),
    path('booking-success/', views.booking_success, name='booking-success'),
    path('schedule-timings/', views.schedule_timings, name='schedule-timings'),
    path('patient-id/', views.patient_id, name='patient-id'),
    path('create-prescription/<int:pk>/', views.create_prescription, name='create-prescription'),
    path('patient-profile/<int:pk>/',views.patient_profile, name='patient-profile'),
    path('delete-education/<int:pk>/',views.delete_education, name='delete-education'),
    path('delete-experience/<int:pk>/',views.delete_experience, name='delete-experience'),
    path('appointments/',views.appointments, name='appointments'),
    path('accept-appointment/<int:pk>/',views.accept_appointment, name='accept-appointment'),
    path('reject-appointment/<int:pk>/',views.reject_appointment, name='reject-appointment'),
    path('patient-search/<int:pk>/', views.patient_search, name='patient-search'),
    path('pdf/<int:pk>/',views.report_pdf, name='pdf'),
    path('professional_review/<int:pk>/', views.professional_review, name='professional_review'),
    path('professional-test-list/', views.professional_test_list, name='professional-test-list'),
    path('professional-view-prescription/<int:pk>/', views.professional_view_prescription, name='professional-view-prescription'),
    path('professional-view-report/<int:pk>/', views.professional_view_report, name='professional-view-report'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
