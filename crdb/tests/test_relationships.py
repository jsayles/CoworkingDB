from django.test import TestCase

from crdb.models import Person, Project, PersonalRelationship
from crdb.models import ProjectType, RelationshipType


class RelationshipTestCase(TestCase):

    def setUp(self):
        person_one = Person.objects.create(username="person_one", email="one@example.com")
        Person.objects.create(username="person_two", email="two@example.com")
        Person.objects.create(username="person_three", email="three@example.com")
        Project.objects.create(name="Coworking Space", code="space", type=ProjectType.SPACE, email="space@example.com", created_by=person_one, updated_by=person_one)
        Project.objects.create(name="Vendor Inc.", code="vendor", type=ProjectType.VENDOR, email="vendor@example.com", created_by=person_one, updated_by=person_one)
        Project.objects.create(name="Consultants & Co", code="consult", type=ProjectType.CONSULTANT, email="consult@example.com", created_by=person_one, updated_by=person_one)

    def test_project_people(self):
        """Make sure Relationship is reflected in Project.people and Person.projects QuerySets."""
        person_one = Person.objects.by_email("one@example.com")
        project = Project.objects.get(code="space")
        self.assertFalse(person_one in project.people())
        self.assertFalse(project in person_one.projects())
        PersonalRelationship.objects.create(type=RelationshipType.FOUNDER, person=person_one, project=project)
        self.assertTrue(person_one in project.people())
        self.assertTrue(project in person_one.projects())

    def test_founders(self):
        """Make Person One a Founder of Coworking Space."""
        person_one = Person.objects.by_email("one@example.com")
        self.assertIsNotNone(person_one)
        founders = Person.objects.founders()
        self.assertFalse(person_one in founders)
        project = Project.objects.get(code="space")
        PersonalRelationship.objects.create(type=RelationshipType.FOUNDER, person=person_one, project=project)
        founders = Person.objects.founders()
        self.assertTrue(person_one in founders)

    def test_vendors(self):
        """Make Person Two a Vendor."""
        person_two = Person.objects.by_email("two@example.com")
        self.assertFalse(person_two in Person.objects.vendors())
        project = Project.objects.get(code="vendor")
        PersonalRelationship.objects.create(type=RelationshipType.VENDOR, person=person_two, project=project)
        self.assertTrue(person_two in Person.objects.vendors())

    def test_consultants(self):
        """Make Person Three a Consultant."""
        person_three = Person.objects.by_email("three@example.com")
        self.assertFalse(person_three in Person.objects.consultants())
        project = Project.objects.get(code="consult")
        PersonalRelationship.objects.create(type=RelationshipType.CONSULT, person=person_three, project=project)
        self.assertTrue(person_three in Person.objects.consultants())
