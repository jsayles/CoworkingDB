from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseRedirect


from crdb import views, api

app_name = 'crdb'
urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    path('robots.txt', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),

    path('account/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('invite/', views.request_invite, name='request_invite'),

    path('', views.home, name='home'),
    path('search/', views.search, name='search'),

    path('profile/', views.profile_redirect, name='profile_redirect'),
    path('profile/<str:username>', views.profile_edit, name='profile_edit'),

    path('people/', views.people_list, name='people_list'),
    path('person/<str:username>', views.person_view, name='person_view'),

    path('projects/', views.project_list, name='project_list'),
    path('project/edit/', views.project_edit, name='project_edit'),
    path('project/edit/<str:code>', views.project_edit, name='project_edit'),
    path('project/view/<str:code>', views.project_view, name='project_view'),

    path('email/add/', views.email_add, name='email_add'),
    path('email/manage/<email_pk>/<action>/', views.email_manage, name='email_manage'),
    path('email/verify/<email_pk>/', views.email_verify, name='email_verify'),

    path('admin/', admin.site.urls),
    path('api/', include('crdb.api')),

]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
