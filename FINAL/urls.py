"""FINAL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from FINALApp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('admin/', admin.site.urls),

    # ADMIN

    path('index/', views.index, name='index'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admindash/', views.admindash, name='admindash'),
    path('addevents/',views.addevents,name='addevents'),
    path('saveevent/',views.saveevent,name='saveevent'),
    path('completedevents/',views.completedevents,name='completedevents'),
    path('upcomingevents/',views.upcomingevents,name='upcomingevents'),
    path('editevent/<int:event_id>/', views.editevent, name='editevent'),
    path('deleteevent/<int:id>/', views.deleteevent, name='deleteevent'),
    path('videogallery/',views.videogallery,name='videogallery'),
    path('editvideogallery/<int:video_id>/', views.editvideogallery, name='editvideogallery'),
    path('deletevideogallery/<int:id>/',views.deletevideogallery, name='deletevideogallery'),


    path('flashnews/',views.flashnews,name='flashnews'),
    path('complaints/',views.complaints,name='complaints'),
    path('complaints/<int:apartment_number>/',views.admin_complaints,name='admin_complaints'),



    path('members/',views.members,name='members'),
    path('deleteuser/<int:id>/', views.deleteuserview, name='deleteuser'),
    path('inactivatebtn/',views.inactivatebtn,name='inactivatebtn'),
    path('activatebtn/',views.activatebtn,name='activatebtn'),

    
   
    path('user/chat/', views.user_chat, name='user_chat'),
    path('admin/chat/', views.admin_chat, name='admin_chat'),
    path('sendchat/', views.send_chat, name='send_chat'),
    path('getchats/', views.get_chats, name='get_chats'),

 

    #USER
   

    
    path('userregister/', views.userregister, name='userregister'),
    path('savenewuser/',views.savenewuser,name='savenewuser'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userhome/',views.userhome,name='userhome'),


    path('forgotpassword/', views.forgotpasswordview, name='forgotpassword'),
    path('passwordrequest/', views.passwordrequestview, name='passwordrequest'),
    
    path('change_password/', views.change_password, name='change_password'),
    path('usercompletedevents/',views.usercompletedevents,name='usercompletedevents'),
    path('userupcomingevents/',views.userupcomingevents,name='userupcomingevents'),
    path('usergallery/',views.usergallery,name='usergallery'),
    path('usercomplaints/', views.usercomplaints, name='usercomplaints'),
    path('savecomplaints/',views.savecomplaints,name='savecomplaints'),


    path('previewcomplaint/',views.previewcomplaint,name='previewcomplaint'),
    path('mark_as_done/<int:complaint_id>/', views.mark_as_done, name='mark_as_done'),

    path('dummy-payment/', views.dummy_payment_view, name='dummy_payment'),
   
    path('payment-success/', views.payment_success, name='payment_success'),

     path('view_transaction/<int:payment_id>/', views.view_transaction, name='view_transaction'),
     path('view_payments/', views.view_payments, name='view_payments'),
     


     path('payment_pdf/<int:payment_id>/', views.payment_pdf_view, name='payment_pdf'),





    
    # path('maintenance-fees/', views.maintenance_fee_list, name='maintenance_fee_list'),
    # path('maintenance-fees/pay/<int:fee_id>/', views.pay_maintenance_fee, name='pay_maintenance_fee'),

    # path('maintenance-fees/', views.maintenance_fee_list, name='maintenance_fee_list'),

    # path('admin/maintenance-fees/', views.maintenance_fee_admin_list, name='maintenance_fee_admin_list'),




]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)