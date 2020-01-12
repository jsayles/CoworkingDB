from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import UserManager, AbstractUser


GENDER_CHOICES = (
    ('U', 'Not recorded'),
    ('M', 'Man'),
    ('F', 'Woman'),
    ('O', 'Something else'),
)


class Website(models.Model):

    GITHUB = "github"
    LINKEDIN = "linkedin"
    PERSONAL = "personal"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    BLOG = "blog"
    OTHER = "other"

    SITE_TYPES = (
        (GITHUB, "github"),
        (LINKEDIN, "linkedin"),
        (PERSONAL, "personal"),
        (FACEBOOK, "facebook"),
        (INSTAGRAM, "instagram"),
        (BLOG, "blog"),
        (OTHER, "other"),
    )

    # Model definitions
    type = models.CharField(max_length=16, choices=SITE_TYPES, default=OTHER)
    url = models.URLField()

    def __str__(self):
        return self.url


class Location(models.Model):
    address1 = models.CharField(max_length=128, blank=True)
    address2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=16, blank=True)
    country = models.CharField(max_length=128, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class PersonManager(UserManager):

    def by_email(self, email):
        """Retrieve a Person based who has the given email address."""
        email_address = EmailAddress.objects.filter(email=email).first() # There should be only one
        if email_address:
            return email_address.person

    def founders(self):
        """Return a QuerySet of all Persons with a Relationship of FOUNDER."""
        pass


class Person(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U")
    pronouns = models.CharField(max_length=64, blank=True, null=True)
    websites = models.ManyToManyField(Website, blank=True)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=16, blank=True, null=True)

    objects = PersonManager()

    def add_email(self, email, primary=False):
        email_address = EmailAddress.objects.filter(person=self, email=email)
        if not email_address:
            email_address = EmailAddress.objects.create(person=self, email=email)
        if primary:
            # Update the Person model
            self.email = email
            self.save()
            # Update the EmailAddress model
            email_address.is_primary = True
            email_address.save()


@receiver(post_save, sender=Person)
def person_post_save(**kwargs):
    """Make sure Person.email is also an EmailAddress."""
    person = kwargs['instance']
    if person.email:
        email_address = person.emails.filter(email=person.email).first() # there should be only one
        if not email_address:
            # Email was not in there so it should be created
            EmailAddress.objects.create(person=person, email=person.email, is_primary=True)
        elif not email_address.is_primary:
            # Email was in there indicating this is being switched to primary
            # Make the old primary not primary anymore
            old_primary = person.emails.filter(is_primary=True).first() # There should be only one
            if old_primary:
                old_primary.is_primary = False
                old_primary.save()
            email_address.is_primary = True
            email_address.save()


class EmailAddress(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="emails", on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    verif_key = models.CharField(max_length=40)
    verified_ts = models.DateTimeField(default=None, null=True, blank=True)
    remote_addr = models.GenericIPAddressField(null=True, blank=True)
    remote_host = models.CharField(max_length=255, null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def is_verified(self):
        """Is this e-mail address verified? Verification is indicated by
        existence of a verified timestamp which is the time the person
        followed the e-mail verification link."""
        return bool(self.verified_ts)

    def set_primary(self):
        """Set this e-mail address to the primary address by setting the
        email property on the person."""
        # If we are already primary, we're done
        if self.is_primary:
            return

        # Make sure the person has the same email address
        if self.person.email != self.email:
            self.person.email = self.email
            self.person.save()

        # Now go through and unset all other email addresses
        for email in self.person.emails.all():
            if email == self:
                email.is_primary = True
                email.save(verify=False)
            else:
                if email.is_primary:
                    email.is_primary = False
                    email.save(verify=False)

    def delete(self):
        """Delete this EmailAddress object."""
        if self.is_primary:
            next_email = self.person.emails.exclude(email=self.email).first()
            if not next_email:
                raise Exception("Can not delete last email address!")
            next_email.set_primary()
        super(EmailAddress, self).delete()


class Company(models.Model):
    SPACE = "space"
    VENDOR = "vendor"
    CONSULT = "consult"
    OTHER = "other"

    COMPANY_TYPES = (
        (SPACE, "Coworking Space"),
        (VENDOR, "Product Vendor"),
        (CONSULT, "Consultantancy"),
        (OTHER, "Other"),
    )

    # Model definitions
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=16, choices=COMPANY_TYPES, default=OTHER)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    websites = models.ManyToManyField(Website, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    created_ts = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_by", on_delete=models.CASCADE)
    updated_ts = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="updated_by", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('vlan', kwargs={'vlan': self.tag})
    #
    # def get_admin_url(self):
    #     return reverse('admin:coredb_vlan_change', args=[self.id])

    class Meta:
        ordering = ['name',]


class Relationship(models.Model):

    FOUNDER = "founder"
    OWNER = "owner"
    EMPLOYEE = "employee"
    VOLUNTEER = "volunteer"
    VENDOR = "vendor"
    CONSULT = "consultant"
    OTHER = "other"

    RELATIONSHIP_TYPES = (
        (FOUNDER, "Founder"),
        (OWNER, "Owner"),
        (EMPLOYEE, "Employee"),
        (VOLUNTEER, "Volunteer"),
        (VENDOR, "Product Vendor"),
        (CONSULT, "Consultant"),
        (OTHER, "Other"),
    )

    # Model definitions
    type = models.CharField(max_length=16, choices=RELATIONSHIP_TYPES, default=OTHER)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_day = models.PositiveSmallIntegerField(blank=True, null=True)
    start_month = models.PositiveSmallIntegerField(blank=True, null=True)
    start_year = models.PositiveSmallIntegerField(blank=True, null=True)
    end_day = models.PositiveSmallIntegerField(blank=True, null=True)
    end_month = models.PositiveSmallIntegerField(blank=True, null=True)
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
