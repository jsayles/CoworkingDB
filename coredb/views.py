import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect

from coredb.models import Person, Project, Relationship, EmailAddress

logger = logging.getLogger(__name__)


#########################################################################
# Generic Views
#########################################################################


def home(request):
    context = {}
    return render(request, 'coredb/home.html', context)


@login_required
def search(request):
    context = {
    }
    return render(request, 'coredb/search.html', context)


#########################################################################
# Profile and Registration Views
#########################################################################


def request_invite(request):
    name = None
    email = None
    if request.POST and 'name' in request.POST:
        name = request.POST['name']
        email = request.POST['email']
        # TODO - Email admins that this person wants an account
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
    return render(request, 'coredb/profile_edit.html', context)


# @staff_member_required
# def search(request):
#     closets = Location.objects.data_closets()
#     ports = None
#     closet_number = None
#     port_label = None
#     if request.POST:
#         try:
#             if 'closet_number' in request.POST:
#                 closet_number = request.POST['closet_number']
#                 closet = Location.objects.filter(number=closet_number).first()
#                 ports = Port.objects.filter(closet=closet)
#             else:
#                 ports = Port.objects.all()
#
#             if 'port_label' in request.POST:
#                 port_label = request.POST['port_label']
#                 alphas, digits = split_label(port_label)
#                 if alphas:
#                     ports = ports.filter(label__istartswith=alphas)
#                 if digits:
#                     ports = ports.filter(label__contains=digits)
#         except Exception as e:
#             messages.add_message(request, messages.ERROR, f"Error performing search: {e} ")
#     order_by = request.GET.get('order_by', 'p')
#     ports = sort_ports(ports, order_by)
#     context = {
#         'closets': closets,
#         'ports': ports,
#         'order_by': order_by,
#         'q_closet': closet_number,
#         'q_label': port_label,
#     }
#     return render(request, 'coredb/search.html', context)
#
# @staff_member_required
# def port_view(request, port_id):
#     port = get_object_or_404(Port, id=port_id)
#     context = {
#         'port': port,
#     }
#     return render(request, 'coredb/port_view.html', context)
#
# #########################################################################
# # Location Views
# #########################################################################
#
# @staff_member_required
# def location_list(request):
#     locations = (
#         (0, Location.objects.filter(floor=0)),
#         (1, Location.objects.filter(floor=1)),
#         (2, Location.objects.filter(floor=2)),
#     )
#     context = {
#         'locations': locations,
#     }
#     return render(request, 'coredb/location_list.html', context)
#
# @staff_member_required
# def location_view(request, location):
#     location = get_object_or_404(Location, number=location)
#     order_by = request.GET.get('order_by', 's')
#     ports = sort_ports(location.port_set.all(), order_by)
#     context = {
#         'location': location,
#         'order_by': order_by,
#         'ports': ports,
#     }
#     return render(request, 'coredb/location_view.html', context)
#
# #########################################################################
# # Switch Views
# #########################################################################
#
# @staff_member_required
# def switch_list(request):
#     # A data closet is a location with switches in it
#     closets = Location.objects.data_closets()
#     context = {
#         'closets': closets
#     }
#     return render(request, 'coredb/switch_list.html', context)
#
# @staff_member_required
# def switch_view(request, stack, unit):
#     switch = get_object_or_404(Switch, stack__name=stack, unit=unit)
#     order_by = request.GET.get('order_by', 's')
#     ports = sort_ports(switch.port_set.all(), order_by)
#     context = {
#         'switch': switch,
#         'order_by': order_by,
#         'ports': ports,
#     }
#     return render(request, 'coredb/switch_view.html', context)
#
# #########################################################################
# # VLAN Views
# #########################################################################
#
# @staff_member_required
# def vlan_list(request):
#     vlans = VLAN.objects.all().order_by('tag')
#     context = {
#         'vlans': vlans,
#     }
#     return render(request, 'coredb/vlan_list.html', context)
#
# @staff_member_required
# def vlan_view(request, vlan):
#     vlan = get_object_or_404(VLAN, tag=vlan)
#     order_by = request.GET.get('order_by', 's')
#     ports = sort_ports(vlan.port_set.all(), order_by)
#     context = {
#         'vlan': vlan,
#         'order_by': order_by,
#         'ports': ports,
#     }
#     return render(request, 'coredb/vlan_view.html', context)


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
        email.send_verification(email_address)

    verif_key = request.GET.get('verif_key', "").strip()
    if len(verif_key) != 0:
        if email_address.verif_key == verif_key:
            # Looks good!  Mark as verified
            email_address.remote_addr = request.META.get('REMOTE_ADDR')
            email_address.remote_host = request.META.get('REMOTE_HOST')
            email_address.verified_ts = timezone.now()
            email_address.save()
            messages.success(request, "Email address has been verified.")
            return HttpResponseRedirect(email_address.person.get_absolute_url())
        else:
            messages.error(request, "Invalid Key")

    return render(request, "email_verify.html", {'email':email_address.email})
