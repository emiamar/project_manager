from django.views.generic import TemplateView
from .models import Ticket, MileStone
from forms import TaskForm, MileStoneForm
from base.mixin import  GeneralContextMixin, DeleteMixin
from django.shortcuts import HttpResponseRedirect, HttpResponse
from base.views import GenericModalCreateView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class DashboardView(PermissionRequiredMixin, GeneralContextMixin, TemplateView):

    template_name = 'ticket/dashboard.html'
    permission_required = 'ticket.add_ticket'

    def get_context_data(self, **kwargs):
        wip_ticket_count = Ticket.objects.filter(status=3).count()
        all_time_delivery_count = Ticket.objects.filter(status=2).count()
        pending_ticket_count = Ticket.objects.filter(status=4).count()
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['wip_ticket_count'] = wip_ticket_count
        context['all_time_delivery_count'] = all_time_delivery_count
        context['pending_ticket_count'] = pending_ticket_count
        return context


class UserDashboardView(PermissionRequiredMixin, GeneralContextMixin, TemplateView):

    template_name = 'ticket/user_dashboard.html'
    permission_required = 'ticket.add_milestone'
    def get_context_data(self, **kwargs):
        user_id = self.request.user
        # user_list = Ticket.objects.filter (assigned_to=user_id)
        wip_ticket_count = Ticket.objects.filter(status=3, assigned_to = user_id).count()
        all_time_delivery_count = Ticket.objects.filter(status=2, assigned_to = user_id).count()
        pending_ticket_count = Ticket.objects.filter(status=4, assigned_to = user_id).count()
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        context['wip_ticket_count'] = wip_ticket_count
        context['all_time_delivery_count'] = all_time_delivery_count
        context['pending_ticket_count'] = pending_ticket_count
        return context


class TicketListView(PermissionRequiredMixin, DeleteMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/ticket_list.html'
    model = Ticket
    object_name = 'Ticket'
    permission_required = 'ticket.add_ticket'

    def get_context_data(self, **kwargs):
        ticket_list = Ticket.objects.all ()
        status = self.request.GET.get('status')
        if status:
            ticket_list = ticket_list.filter(status=status)
        context = super(TicketListView, self).get_context_data(**kwargs)
        context['ticket_list'] = ticket_list
        context['form'] = TaskForm()
        return context

    def get_success_url(self):
        return ""


# MilestoneListView TicketListUserView
class TicketDetailView(PermissionRequiredMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/all_user_details.html'
    permission_required = 'ticket.add_ticket'
    def get_context_data(self, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        detail_list = MileStone.objects.filter(ticket__id=ticket_id)
        ticket = Ticket.objects.get(pk=ticket_id)
        context['ticket'] = ticket
        context['detail_list'] = detail_list
        return context


class TicketDetailUserView(PermissionRequiredMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/detail_user.html'
    permission_required = 'ticket.add_milestone'
    def get_context_data(self, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketDetailUserView, self).get_context_data(**kwargs)
        detail_list = MileStone.objects.filter(ticket__id=ticket_id)
        ticket = Ticket.objects.get(pk=ticket_id)
        context['ticket'] = ticket
        context['detail_list'] = detail_list
        context['form'] = MileStoneForm()
        return context


class TicketListUserView(PermissionRequiredMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/user_ticket_list.html'
    model = Ticket
    object_name = 'Ticket'
    permission_required = 'ticket.add_milestone'
    def get_context_data(self, **kwargs):
        user_id = self.request.user
        user_list = Ticket.objects.filter (assigned_to=user_id)
        status = self.request.GET.get ('status')
        if status:
            user_list = user_list.filter (status=status, )
        context = super(TicketListUserView, self).get_context_data(**kwargs)
        context['form'] = MileStoneForm()
        context['user_list'] = user_list
        return context

    def get_success_url(self):
        return ""


class TicketCreateView (GenericModalCreateView):
    form_class = TaskForm
    success_url = '/ticket/ticket_list/'


class MilestoneCreateView (PermissionRequiredMixin, GenericModalCreateView):
    form_class = MileStoneForm
    permission_required = 'ticket.add_milestone'
    def form_init(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['user'] = request.user.id
        self.ticket_id = data.getlist('ticket')[0]
        data['ticket'] = self.ticket_id
        form = self.form_class(data)
        return self.form_check(form, *args, **kwargs)

    def get_success_url(self):
        return '/ticket/user_detail/{ticket_id}'.format(ticket_id=self.ticket_id)


class TicketUpdateView(GeneralContextMixin, GenericModalCreateView):
    form_class = TaskForm
    success_url = '/ticket/ticket_list/'
    object_name = 'TASK'
    def form_init(self, request, *args, **kwargs):
        """
        Instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        ticket_id = kwargs.get("ticket_id")
        ticket = Ticket.objects.get (pk=ticket_id)
        form = self.form_class (request.POST, instance= ticket)
        return self.form_check (form, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print "Form valid"
        form.save()
        msg = "Succesfully updated {0} {1}".format(
            self.object_name, form.instance)
        print "Form Saved"
        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())


class TicketUpdateTemplateView (PermissionRequiredMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/update.html'
    permission_required = 'ticket.add_ticket'
    def get_context_data(self, **kwargs):
        user_id = self.request.user
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketUpdateTemplateView, self).get_context_data(**kwargs)
        ticket = Ticket.objects.get(pk=ticket_id)
        context['form'] = TaskForm(instance=ticket)
        context['ticket_id'] = ticket_id
        return context


def delete_ticket(request):
    delete_ids = request.GET.getlist('for_action')
    # message
    return HttpResponse('/ticket/ticket_list')


'''
class MilestoneCreateView():
    pass
'''