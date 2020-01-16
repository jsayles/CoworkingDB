from django.test import TestCase

from coredb.models import Person, Company, Relationship


class RelationshipTestCase(TestCase):

    def setUp(self):
        person_one = Person.objects.create(username="person_one", email="one@example.com")
        Person.objects.create(username="person_two", email="two@example.com")
        Person.objects.create(username="person_three", email="three@example.com")
        Company.objects.create(name="Space Co", code="space", type=Company.SPACE, email="space@example.com", created_by=person_one, updated_by=person_one)
        Company.objects.create(name="Vendor Co", code="vendor", type=Company.VENDOR, email="vendor@example.com", created_by=person_one, updated_by=person_one)
        Company.objects.create(name="Consultants Co", code="consult", type=Company.CONSULT, email="consult@example.com", created_by=person_one, updated_by=person_one)

    def test_founders(self):
        person_one = Person.objects.by_email("one@example.com")
        self.assertIsNotNone(person_one)
        founders = Person.objects.founders()
        self.assertFalse(person_one in founders)
        space_co = Company.objects.get(code="space")
        Relationship.objects.create(type=Relationship.FOUNDER, person=person_one, company=space_co)
        founders = Person.objects.founders()
        self.assertTrue(person_one in founders)
