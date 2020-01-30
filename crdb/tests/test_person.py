from django.test import TestCase

from crdb.models import Person, EmailAddress, SiteType


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

    def test_save_url(self):
        person_one = Person.objects.get(username='person_one')
        website_one = "https://github.com/person_one"
        website_two = "https://github.com/p1"
        self.assertEqual(0, person_one.websites.count())

        # Save a Github URL and test it was saved
        person_one.save_url(SiteType.GITHUB, website_one)
        self.assertEqual(1, person_one.websites.count())
        self.assertEqual(website_one, person_one.websites.first().url)
        
        # Save another Github URL and assume it overwrites the first one
        person_one.save_url(SiteType.GITHUB, website_two)
        self.assertEqual(1, person_one.websites.count())
        self.assertEqual(website_two, person_one.websites.first().url)
