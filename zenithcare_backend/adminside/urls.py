from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    path('userlist',UserList.as_view()),
    path('vendorlist',VendorList.as_view()),
    path('verify-pending',PendingVerifyList.as_view()),
    path('block/<int:user_id>/',UserBlock.as_view()),
    path('vendor_approve/<int:user_id>/',VendorApprove.as_view()),
    path('payment-statistics/', PaymentStatisticsAPI.as_view(), name='payment-statistics-api'),
    path('adminstatisticaldata/', AdminStatisticalData.as_view(), name='adminstatisticaldata'),
    path('reports-create/', CreateReportView.as_view(), name='create-report'),
    path('reports/', ReportListCreateView.as_view(), name='report-list-create'),
    path('categories-create/', CategoryCreateView.as_view(), name='category-create'),
    path('language-create/', LanguageCreateView.as_view(), name='language-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('language/', LanguageListView.as_view(), name='language-list'),
     path('categories/<int:category_id>/block/', CategoryBlockView.as_view(), name='category-block'),
    path('categories/<int:category_id>/unblock/', CategoryUnblockView.as_view(), name='category-unblock'),
     path('language/<int:Language_id>/block/', LanguageBlockView.as_view(), name='language-block'),
    path('language/<int:Language_id>/unblock/', LanguageUnblockView.as_view(), name='language-unblock'),


]
