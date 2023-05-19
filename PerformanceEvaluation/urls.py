"""PerformanceEvaluation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from EvaluationApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login',views.login,name='login'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('employeeregistration',views.employeeregistration,name='employeeregistration'),
    path('deletemp',views.deletemp,name='deletemp'),
    path('managerregistration',views.managerregistration,name='managerregistration'),
    path('deletemanager',views.deletemanager,name='deletemanager'),
    path('managerhome',views.managerhome,name='managerhome'),
    path('employeehome',views.employeehome,name='employeehome'),
    path('addproject',views.addproject,name='addproject'),
    path('deleteproject',views.deleteproject,name='deleteproject'),
    path('assignproject',views.assignproject,name='assignproject'),
    path('allocatemanager',views.allocatemanager,name='allocatemanager'),
    path('viewtasksemployee',views.viewtasksemployee,name='viewtasksemployee'),
    path('taskupdation',views.taskupdation,name='taskupdation'),
    path('empworkupdate',views.empworkupdate,name='empworkupdate'),
    path('managerupdates',views.managerupdates,name='managerupdates'),
    path('manageraddfeedback',views.manageraddfeedback,name='manageraddfeedback'),
    path('adminallocation',views.adminallocation,name='adminallocation'),
    path('empappraisalrequest',views.empappraisalrequest,name='empappraisalrequest'),
    path('manageraddevaluation',views.manageraddevaluation,name='manageraddevaluation'),
    path('managerappraisal',views.managerappraisal,name='managerappraisal'),
    path('adminappraisal',views.adminappraisal,name='adminappraisal'),
    path('adminevaluation',views.adminevaluation,name='adminevaluation'),
    path('adminapproveappraisal',views.adminapproveappraisal,name='adminapproveappraisal'),
]
