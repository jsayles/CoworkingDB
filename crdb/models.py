import sys
import logging
import random
import hashlib

from datetime import datetime, time, date, timedelta

from django.conf import settings
from django.core.mail import mail_admins, send_mail
from django.contrib.auth.models import UserManager, AbstractUser
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import get_template, render_to_string
from django.urls import reverse

logger = logging.getLogger(__name__)


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
        founder_qs = Relationship.objects.filter(type=Relationship.FOUNDER)
        return Person.objects.filter(id__in=founder_qs.values("person"))

    def vendors(self):
        """Return a QuerySet of all Persons with a Relationship of VENDOR."""
        vendor_qs = Relationship.objects.filter(type=Relationship.VENDOR)
        return Person.objects.filter(id__in=vendor_qs.values("person"))

    def consultants(self):
        """Return a QuerySet of all Persons with a Relationship of CONSULT."""
        consult_qs = Relationship.objects.filter(type=Relationship.CONSULT)
        return Person.objects.filter(id__in=consult_qs.values("person"))


class Person(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U")
    pronouns = models.CharField(max_length=64, blank=True)
    websites = models.ManyToManyField(Website, blank=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=16, blank=True)

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

    def get_absolute_url(self):
        return reverse('profile_edit', kwargs={'username': self.username})

    def get_admin_url(self):
        return reverse('admin:crdb_person_change', args=[self.id])


@receiver(post_save, sender=Person)
def person_post_save(**kwargs):
    """Make sure Person.email is also an EmailAddress."""
    person = kwargs['instance']
    if person.email:
        email_address = EmailAddress.objects.filter(person=person, email=person.email).first() # there should be only one
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
    verified_ts = models.DateTimeField(default=None, blank=True, null=True)
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    remote_host = models.CharField(max_length=255, blank=True)
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

    def generate_verif_key(self):
        random.seed(datetime.now())
        salt = random.randint(0, sys.maxsize)
        salted_email = "%s%s" % (salt, self.email)
        return hashlib.sha1(salted_email.encode('utf-8')).hexdigest()

    def get_verif_key(self):
        if not self.verif_key:
            self.verif_key = self.generate_verif_key()
            self.save()
        return self.verif_key

    def get_verify_link(self):
        if hasattr(settings, 'EMAIL_VERIFICATION_URL'):
            verify_link = settings.EMAIL_VERIFICATION_URL
        else:
            verif_key = self.get_verif_key()
            uri = reverse('email_verify', kwargs={'email_pk': self.id}) + "?verif_key=" + verif_key
            verify_link = settings.BASE_URL + uri
        return verify_link

    def get_send_verif_link(self):
        return reverse('email_verify', kwargs={'email_pk': self.id}) + "?send_link=True"

    def get_set_primary_link(self):
        return reverse('email_manage', kwargs={'email_pk': self.id, 'action':'set_primary'})

    def get_delete_link(self):
        return reverse('email_manage', kwargs={'email_pk': self.id, 'action':'delete'})

    def send_verification(self):
        """Send email verification link for this EmailAddress object.
        Raises smtplib.SMTPException, and NoRouteToHost.
        """

        # Build our context for rendering
        context_dict = {
            'email': self.email,
            'user': self.person,
            'verif_key': self.get_verif_key(),
            'verif_link': self.get_verify_link(),
            'base_url': settings.BASE_URL,
        }

        subject = "Please Verify Your Email Address"
        from_email = settings.SERVER_EMAIL
        recipient_list = [self.email, ]
        text_template = get_template('email/verification_email.txt')
        text_msg = text_template.render(context=context_dict)
        html_template = get_template('email/verification_email.html')
        html_msg = html_template.render(context=context_dict)
        send_mail(subject, text_msg, from_email, recipient_list, html_message=html_msg)

    def save(self, verify=True, *args, **kwargs):
        """Save this EmailAddress object."""
        if self.pk:
            # Skip verification if this is an update
            verify = False
        if not self.verif_key:
            self.verif_key = self.generate_verif_key()
        super(EmailAddress, self).save(*args, **kwargs)
        if verify:
            self.send_verification()

    def delete(self):
        """Delete this EmailAddress object."""
        if self.is_primary:
            next_email = self.person.emails.exclude(email=self.email).first()
            if not next_email:
                raise Exception("Can not delete last email address!")
            next_email.set_primary()
        super(EmailAddress, self).delete()


class Project(models.Model):
    SPACE = "space"
    VENDOR = "vendor"
    CONSULTANT = "consultant"
    NONPROFIT = "nonprofit"
    COOP = "coop"
    COLLECTIVE = "collective"
    OTHER = "other"

    PROJECT_TYPES = (
        (SPACE, "Coworking Space"),
        (VENDOR, "Product Vendor"),
        (CONSULTANT, "Consultantancy"),
        (NONPROFIT, "Non-Profit"),
        (COOP, "Co-Operative"),
        (COLLECTIVE, "Collective"),
        (OTHER, "Other"),
    )

    # Model definitions
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32, unique=True)
    type = models.CharField(max_length=16, choices=PROJECT_TYPES, default=OTHER)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=16, blank=True)
    websites = models.ManyToManyField(Website, blank=True)
    email = models.EmailField(max_length=100, blank=True, unique=True)
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
    #     return reverse('admin:crdb_vlan_change', args=[self.id])

    class Meta:
        ordering = ['name',]


class Relationship(models.Model):

    FOUNDER = "founder"
    OWNER = "owner"
    EMPLOYEE = "employee"
    MEMBER = "member"
    VOLUNTEER = "volunteer"
    WORKTRADE = "worktrade"
    BOARD = "board"
    VENDOR = "vendor"
    CONSULT = "consultant"
    OTHER = "other"

    RELATIONSHIP_TYPES = (
        (FOUNDER, "Founder"),
        (OWNER, "Owner"),
        (EMPLOYEE, "Employee"),
        (MEMBER, "Member"),
        (VOLUNTEER, "Volunteer"),
        (WORKTRADE, "Work Trade"),
        (BOARD, "Board Member"),
        (VENDOR, "Product Vendor"),
        (CONSULT, "Consultant"),
        (OTHER, "Other"),
    )

    # Model definitions
    type = models.CharField(max_length=16, choices=RELATIONSHIP_TYPES, default=OTHER)
    person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_day = models.PositiveSmallIntegerField(null=True, blank=True)
    start_month = models.PositiveSmallIntegerField(null=True, blank=True)
    start_year = models.PositiveSmallIntegerField(null=True, blank=True)
    end_day = models.PositiveSmallIntegerField(null=True, blank=True)
    end_month = models.PositiveSmallIntegerField(null=True, blank=True)
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
