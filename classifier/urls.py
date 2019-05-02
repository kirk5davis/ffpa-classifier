from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('classify_imgs/', views.classify_home, name='classify_home'),
    path('classify_imgs/<str:model_type>/<int:img_id>', views.classify_iter, name='classify_iter'),
    path('summary', views.summary, name='summary'),
    path('profile', views.profile, name='profile'),
    path('review', views.review, name='review'),
    path('success', views.success, name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
