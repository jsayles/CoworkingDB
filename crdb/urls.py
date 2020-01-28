from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from crdb import views

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

    path('email/add/', views.email_add, name='email_add'),
    path('email/manage/<email_pk>/<action>/', views.email_manage, name='email_manage'),
    path('email/verify/<email_pk>/', views.email_verify, name='email_verify'),

    # path('port/<int:port_id>/', views.port_view, name='port'),
    # path('locations/', views.location_list, name='locations'),
    # path('location/<str:location>/', views.location_view, name='location'),
    # path('switches/', views.switch_list, name='switches'),
    # path('switch/<str:stack>/<int:unit>/', views.switch_view, name='switch'),
    # path('vlans/', views.vlan_list, name='vlans'),
    # path('vlan/<str:vlan>/', views.vlan_view, name='vlan'),
    # path('orgs/', views.org_list, name='orgs'),
    # path('org/<int:org_id>/', views.org_view, name='org'),
    # path('print/org/<int:org_id>/', views.org_print, name='org_print'),
    path('admin/', admin.site.urls),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
