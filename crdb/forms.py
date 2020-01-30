import logging
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.utils.timezone import localtime, now

from crdb.models import Month, SiteType, Person

logger = logging.getLogger(__name__)


# class LinkForm(forms.Form):
#     username = forms.CharField(required=False, widget=forms.HiddenInput)
#     url_type = forms.ModelChoiceField(widget=forms.Select(), label='Website Type', queryset=SiteType.choices, required=False)
#     url = forms.URLField(widget=forms.URLInput(), required=False)
#
#     def save(self):
#         if not self.is_valid():
#             raise Exception('The form must be valid in order to save')
#
#         if self.cleaned_data['username']:
#             person = Person.objects.get(username=self.cleaned_data['username'])
#             person.save_url(self.cleaned_data['url_type'], self.cleaned_data['url'])


class EditProfileForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.HiddenInput)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    # address1 = forms.CharField(max_length=100, required=False)
    # address2 = forms.CharField(max_length=100, required=False)
    # city = forms.CharField(max_length=100, required=False)
    # state = forms.ChoiceField(widget=forms.Select(), choices=get_state_choices, required=False)
    # zipcode = forms.CharField(max_length=16, required=False)
    phone = forms.CharField(max_length=20, required=False)
    bio = forms.CharField(widget=forms.Textarea, max_length=512, required=False)
    url_github = forms.URLField(required=False)
    url_linkedin = forms.URLField(required=False)
    url_twitter = forms.URLField(required=False)
    url_facebook = forms.URLField(required=False)
    url_instagram = forms.URLField(required=False)
    url_personal = forms.URLField(required=False)
    url_blog = forms.URLField(required=False)

    def save(self):
        if not self.is_valid():
            raise Exception('The form must be valid in order to save')

        person = Person.objects.get(username=self.cleaned_data['username'])
        person.first_name = self.cleaned_data['first_name']
        person.last_name = self.cleaned_data['last_name']
        person.phone = self.cleaned_data['phone']
        person.bio = self.cleaned_data['bio']
        person.save()

        # Location data
        # TODO - Convert to Person.location
        # person.address1 = self.cleaned_data['address1']
        # person.address2 = self.cleaned_data['address2']
        # person.city = self.cleaned_data['city']
        # person.state = self.cleaned_data['state']
        # person.zipcode = self.cleaned_data['zipcode']
        # person.save()

        # Save the URLs
        person.save_url(SiteType.GITHUB, self.cleaned_data['url_github'])
        person.save_url(SiteType.TWITTER, self.cleaned_data['url_twitter'])
        person.save_url(SiteType.LINKEDIN, self.cleaned_data['url_linkedin'])
        person.save_url(SiteType.FACEBOOK, self.cleaned_data['url_facebook'])
        person.save_url(SiteType.INSTAGRAM, self.cleaned_data['url_instagram'])
        person.save_url(SiteType.PERSONAL, self.cleaned_data['url_personal'])
        person.save_url(SiteType.BLOG, self.cleaned_data['url_blog'])

        return person


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    # start_month = forms.ChoiceField(widget=forms.Select(), choices=Month.choices, required=False)
