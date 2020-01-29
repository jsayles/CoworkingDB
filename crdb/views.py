import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import mail_admins
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import localtime, now

from crdb.models import Person, Project, Relationship, EmailAddress

logger = logging.getLogger(__name__)


#########################################################################
# Generic Views
#########################################################################


def home(request):
    context = {}
    return render(request, 'crdb/home.html', context)


@login_required
def search(request):
    context = {
    }
    return render(request, 'crdb/search.html', context)


#########################################################################
# Profile and Registration Views
#########################################################################


def request_invite(request):
    name = None
    email = None
    if request.POST and 'name' in request.POST:
        name = request.POST['name']
        email = request.POST['email']
        message = f"Invitation Request from {name}:{email}"
        mail_admins("Invitation Request", message, fail_silently=True)
    context = {
        "name": name,
        "email": email,
    }
    return render(request, 'registration/request_invite.html', context)


@login_required
def profile_redirect(request):
    person = request.user
    return HttpResponseRedirect(person.get_absolute_url())


@login_required
def profile_edit(request, username):
    person = get_object_or_404(Person, username=username)
    context = {
        "person": person
    }
    return render(request, 'crdb/profile_edit.html', context)


#########################################################################
# People Views
#########################################################################


@login_required
def people_list(request):
    people = Person.objects.all()
    context = {
        'people': people,
    }
    return render(request, 'crdb/people_list.html', context)


def person_view(request, username):
    person = get_object_or_404(Person, username=username)
    context = {
        'person': person,
    }
    return render(request, 'crdb/person_view.html', context)


#########################################################################
# Project Views
#########################################################################


def project_list(request):
    projects = Project.objects.all()
    view_flagged = 'flagged' in request.GET
    if view_flagged and request.user.is_staff:
        projects = projects.filter(is_flagged=True)
    else:
        projects = projects.filter(is_flagged=False)

    # Possibly reorder the list
    order_by = request.GET.get('order_by', '')
    if order_by:
        projects = projects.order_by(order_by)

    context = {
        'projects': projects,
    }
    return render(request, 'crdb/project_list.html', context)


@login_required
def project_view(request, code):
    project = get_object_or_404(Project, code=code)
    context = {
        'project': project,
    }
    return render(request, 'crdb/project_view.html', context)


##########################################################################
# Email Views
##########################################################################


@login_required
def email_manage(request, email_pk, action):
    """Set the requested email address as the primary. Can only be
    requested by the owner of the email address."""
    email_address = get_object_or_404(EmailAddress, pk=email_pk)
    if not email_address.person == request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to manage this email address")
    # if not email_address.is_verified():
    #     messages.error(request, "Email '%s' needs to be verified first." % email_address.email)

    if action == "set_primary":
        email_address.set_primary()
        messages.success(request, "'%s' is now marked as your primary email address." % email_address.email)
    elif action == "delete":
        email_address.delete()
        messages.success(request, "'%s' has been removed." % email_address.email)

    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(email_address.person.get_absolute_url())


@login_required
def email_add(request):
    person = get_object_or_404(Person, username=request.POST.get("username"))
    email = request.POST.get("email")
    if email:
        e = EmailAddress(person=person, email=email.lower())
        e.save(verify=True)
        messages.success(request, "Email address has been added.")
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(email_address.person.get_absolute_url())


@login_required
def email_delete(request, email_pk):
    """Delete the given email. Must be owned by current user."""
    email = get_object_or_404(EmailAddress, pk=int(email_pk))
    if not email_address.person == request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to delete this email address")
    elif len(email.person.emails.count()) == 1:
        messages.error(request, "You can not remove the last email address")
    else:
        email.delete()
        messages.success(request, "Email address has been deleted.")
    return HttpResponseRedirect(email_address.person.get_absolute_url())


@csrf_protect
def email_verify(request, email_pk):
    email_address = get_object_or_404(EmailAddress, pk=email_pk)
    if email_address.is_verified():
        messages.error(request, "Email address was already verified.")
    if not email_address.person == request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to verify this email address")

    # Send the verification link if that was requested
    if 'send_link' in request.GET:
        email_address.send_verification()

    verif_key = request.GET.get('verif_key', "").strip()
    if len(verif_key) != 0:
        if email_address.verif_key == verif_key:
            # Looks good!  Mark as verified
            email_address.remote_addr = request.META.get('REMOTE_ADDR')
            email_address.remote_host = request.META.get('REMOTE_HOST')
            email_address.verified_ts = localtime(now())
            email_address.save()
            messages.success(request, "Email address has been verified.")
            return HttpResponseRedirect(email_address.person.get_absolute_url())
        else:
            messages.error(request, "Invalid Key")

    return render(request, "registration/email_verify.html", {'email':email_address.email})
