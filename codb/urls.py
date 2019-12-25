from django.contrib import admin
from django.urls import path

from codb import views

app_name = 'codb'
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
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
