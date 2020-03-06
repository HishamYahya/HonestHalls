from django.urls import path
from . import views

urlpatterns = [
    path('edit/<int:review_id>', views.edit, name='review-edit'),
    path('write/<int:hall_id>', views.write, name='review-write'),
    path('delete/<int:review_id>', views.delete, name='review-delete'),
    path('edit/<int:review_id>/photos', views.review_photos, name='review-photos'),
    path('report/<int:review_id>', views.report, name='report'),
]
