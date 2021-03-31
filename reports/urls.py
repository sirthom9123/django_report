from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('save/', views.create_report_view, name='create_report'),
    path('list/', views.ReportListView.as_view(), name='report_list'),
    path('upload_file/', views.UploadTemplateView.as_view(), name='upload'),
    path('upload/', views.csv_upload_view, name='csv_upload_view'),
    
    
    path('<pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('pdf/<int:pk>/', views.render_pdf_view, name='generate_pdf'),
]
