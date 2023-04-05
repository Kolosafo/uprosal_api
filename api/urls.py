from django.urls import path
from django.views.generic import TemplateView
from . import views

from django.conf import settings
from django.conf.urls.static import static


app_name = 'api'
urlpatterns = [
    # url path to get posts
    path('get_cover_letter/<str:email>',
         views.get_cover_letter, name="get_cover_letter"),
    path('get_projects/<str:email>', views.get_projects, name="get_projects"),
    path('update_project/', views.update_project, name="update_project"),
    path('delete_project/', views.delete_projects, name="delete_project"),
    path('save_cover_letter/', views.save_cover_letter, name="save_cover_letter"),
    path('save_projects/', views.save_projects, name="save_projects"),

    path('save_skills/', views.save_skills, name="save_skills"),
    path('get_skills/<str:email>', views.get_skills, name="get_skills"),
    path('update_skills/', views.update_skills, name="update_skills"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
