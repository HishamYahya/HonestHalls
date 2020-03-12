from django.urls import path, include
from . import views
import reviews.views as review_views
urlpatterns = [
    path('', views.index, name='index'),
    path('hall/<int:id>', views.hallpage, name='hallpage'),
    path('hall/<int:hall_id>/<int:review_id>/up', review_views.up_vote, name='hallpage-upvote'),
    path('hall/<int:hall_id>/<int:review_id>/down', review_views.down_vote, name='hallpage-downvote'),
]
