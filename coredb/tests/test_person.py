from django.test import TestCase

from coredb.models import Person, EmailAddress


class PersonTestCase(TestCase):

    def setUp(self):
        Person.objects.create(username="person_one", email="one@example.com")
        # Person.objects.create(username="person_two", email="two@example.com")
        # Person.objects.create(username="person_three", email="three@example.com")

    def test_by_email(self):
        person_one = Person.objects.by_email("one@example.com")
        self.assertIsNotNone(person_one)
        other_one = Person.objects.get(username='person_one')
        self.assertEqual(person_one, other_one)

    def test_add_email(self):
        new_email = "one2@example.com"
        person_one = Person.objects.get(username='person_one')
        email_count = EmailAddress.objects.filter(person=person_one).count()
        self.assertEqual(email_count, 1)

        # Can not pull user_one with new email
        new_one = Person.objects.by_email(new_email)
        self.assertIsNone(new_one)

        # Add new email
        person_one.add_email(new_email)
        email_count = EmailAddress.objects.filter(person=person_one).count()
        self.assertEqual(email_count, 2)

        # Assume we can get this user by email now
        new_one = Person.objects.by_email(new_email)
        self.assertIsNotNone(new_one)
        self.assertEqual(person_one, new_one)

    def test_add_primary_email(self):
        new_email = "one2@example.com"
        person_one = Person.objects.get(username='person_one')

        # Add new primary email
        person_one.add_email(new_email, primary=True)
        email_count = EmailAddress.objects.filter(person=person_one).count()
        self.assertEqual(email_count, 2)

        # Assume Person.email is now our new email
        new_one = Person.objects.filter(email=new_email).first()
        self.assertIsNotNone(new_one)
        self.assertEqual(person_one, new_one)

        # Assume our new model is properly set as primary
        email_address = EmailAddress.objects.get(email=new_email)
        self.assertTrue(email_address.is_primary)
