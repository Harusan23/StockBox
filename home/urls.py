"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from page import views
from page.views import InventInView
from page.views import render_pdf_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('login/',views.login),
    path('logout/',views.logout),
    path('signinagain/',views.signup),

    path('post_signin/',views.post_signin),
    path('myprofile/',views.myprofile),
    path('profile/',views.profile),
    path('profileedit/',views.profileedit),
    path('editnow/',views.editprofile),

    path('HR/',views.hr),
    path('HR/register/',views.register),
    path('remove_user/',views.remove_user),

    path('management/', views.management),
    path('management_alert/', views.management_alert),
    path('product_ref/', views.product_ref),

    path('comingmanage/', views.comingmanage),
    path('comingmanage_alert/', views.comingmanage_alert),
    path('add_product_for_checking/', views.add_product_for_checking),
    path('add_product_for_checking_old/', views.add_product_for_checking_old),
    path('choiceaddinven/',views.choiceaddinven),
    path('cal_add_invent/',views.cal_add_invent),
    path('damage_product/',views.damage_product),

    path('Delete/',views.Delete_Order),
    path('soleoutmanage/', views.soleoutmanage),
    path('soleoutmanage_alert/', views.soleoutmanage_alert),
    path('soleoutmanage_delete/', views.soleoutmanage_Delete),
    path('Sole_Out/',views.SoleOut),
    path('xxxx/', views.xxxx),


    path('damage/',views.damage),
    path('cal_manage_damage/',views.cal_manage_damage),

    path('damageinven/',views.damageinven),

    path('movechoice/',views.movechoice),

    path('history/',views.history),
    path('history2/',views.history2),
    path('history3/',views.history3),

    path('InView/',InventInView.as_view()),
    path('pdf/',views.render_pdf_view,name ='pdf-view'),

    path('test/',views.Test),
]
