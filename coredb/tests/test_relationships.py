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
        """Make Person One a Founder of Space Co."""
        person_one = Person.objects.by_email("one@example.com")
        self.assertIsNotNone(person_one)
        founders = Person.objects.founders()
        self.assertFalse(person_one in founders)
        space_co = Company.objects.get(code="space")
        Relationship.objects.create(type=Relationship.FOUNDER, person=person_one, company=space_co)
        founders = Person.objects.founders()
        self.assertTrue(person_one in founders)

    def test_vendors(self):
        """Make Person Two a Vendor."""
        person_two = Person.objects.by_email("two@example.com")
        self.assertFalse(person_two in Person.objects.vendors())
        vend_co = Company.objects.get(code="vendor")
        Relationship.objects.create(type=Relationship.VENDOR, person=person_two, company=vend_co)
        self.assertTrue(person_two in Person.objects.vendors())

    def test_consultants(self):
        """Make Person Three a Consultant."""
        person_three = Person.objects.by_email("three@example.com")
        self.assertFalse(person_three in Person.objects.consultants())
        company = Company.objects.get(code="consult")
        Relationship.objects.create(type=Relationship.CONSULT, person=person_three, company=company)
        self.assertTrue(person_three in Person.objects.consultants())
