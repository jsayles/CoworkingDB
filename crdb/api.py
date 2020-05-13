import logging

from django.conf.urls import url, include

from rest_framework import routers, serializers, viewsets

from crdb.models import Person, Project


######################################################################
# Serializers define the API representation.
######################################################################


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = [
            'url',
            'username',
            'email',
            'is_staff'
        ]


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = [
            'url',
            'name',
            'email',
            'websites'
        ]


######################################################################
# ViewSets define the view behavior.
######################################################################


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


######################################################################
# Routers provide an easy way of automatically determining the URL conf.
######################################################################


router = routers.DefaultRouter()
router.register(r'people', PersonViewSet)
router.register(r'projects', ProjectViewSet)


######################################################################
# URL Patterns
######################################################################


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
