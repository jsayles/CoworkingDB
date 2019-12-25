from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Count


GENDER_CHOICES = (
    ('U', 'Not recorded'),
    ('M', 'Man'),
    ('F', 'Woman'),
    ('O', 'Something else'),
)


class RelationshipType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self): return self.name


class Relationship(models.Model):
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO - Add start and end dates


class URLType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self): return self.name

    class Meta:
        ordering = ['name']


class Website(models.Model):
    url_type = models.ForeignKey(URLType, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url


class Space(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address1 = models.CharField(max_length=128, blank=True)
    address2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=16, blank=True)
    country = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    relationships = models.ManyToManyField(Relationship, blank=True)
    websites = models.ManyToManyField(Website, blank=True)
    email = models.EmailField(max_length=100, unique=True)
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
    #     return reverse('admin:codb_vlan_change', args=[self.id])

    class Meta:
        ordering = ['name',]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, related_name="profile", on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address1 = models.CharField(max_length=128, blank=True)
    address2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=16, blank=True)
    country = models.CharField(max_length=128, blank=True)
    bio = models.TextField(blank=True, null=True)
    websites = models.ManyToManyField(Website, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="U")
    pronouns = models.CharField(max_length=64, blank=True, null=True)


class EmailAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        existence of a verified timestamp which is the time the user
        followed the e-mail verification link."""
        return bool(self.verified_ts)

    def set_primary(self):
        """Set this e-mail address to the primary address by setting the
        email property on the user."""
        # If we are already primary, we're done
        if self.is_primary:
            return

        # Make sure the user has the same email address
        if self.user.email != self.email:
            self.user.email = self.email
            self.user.save()

        # Now go through and unset all other email addresses
        for email in self.user.emailaddress_set.all():
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
            next_email = self.user.emailaddress_set.exclude(email=self.email).first()
            if not next_email:
                raise Exception("Can not delete last email address!")
            next_email.set_primary()
        super(EmailAddress, self).delete()
