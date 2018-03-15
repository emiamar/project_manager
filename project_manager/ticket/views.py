from django.views.generic import TemplateView
from .models import Ticket, MileStone
from forms import TaskForm
from base.mixin import  GeneralContextMixin, DeleteMixin
from django.shortcuts import HttpResponseRedirect, HttpResponse
from base.views import GenericModalCreateView
from django.contrib import messages


class DashboardView(GeneralContextMixin, TemplateView):

    template_name = 'ticket/dashboard.html'


# def testing(request):
#   return HttpRespose("hello")


class TicketListView(DeleteMixin, GeneralContextMixin, TemplateView):
    template_name = 'ticket/ticket_list.html'
    model = Ticket
    object_name = 'Ticket'

    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        ticket_list = Ticket.objects.all()
        context['ticket_list'] = ticket_list
        context['form'] = TaskForm()
        return context

    def get_success_url(self):
        return ""


# MilestoneListView
class TicketDetailView(GeneralContextMixin, TemplateView):
    template_name = 'ticket/detail_user.html'

    def get_context_data(self, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        detail_list = MileStone.objects.filter(ticket__id=ticket_id)
        ticket = Ticket.objects.get(pk=ticket_id)
        context['ticket'] = ticket
        context['detail_list'] = detail_list
        return context


class TicketCreateView (GenericModalCreateView):
    form_class = TaskForm
    success_url = '/ticket/ticket_list/'


class TicketUpdateView(GenericModalCreateView):
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



class TicketUpdateTemplateView (TemplateView):
    template_name = 'ticket/update.html'

    def get_context_data(self, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        context = super(TicketUpdateTemplateView, self).get_context_data(**kwargs)
        ticket = Ticket.objects.get(pk=ticket_id)
        context['form'] = TaskForm(instance=ticket)
        context['ticket_id'] = ticket_id
        return context


def delete_ticket(request):
    delete_ids = request.GET.getlist('for_action')
    return HttpResponse('/ticket/ticket_list')


'''
class MilestoneCreateView():
    pass
'''