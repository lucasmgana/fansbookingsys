from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse_lazy
from django .contrib.auth.models import User
from django.views import generic

from .models import *
from .forms import *

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['matchs'] = Match.objects.all()
        context['total_match'] = Match.objects.all().count()        
        return context


def register(req):
    form = RegisterForm()
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        context = {
            'teams': Club.objects.all(),
            'form': form,
        }

        if form.is_valid():
            user = form.save()
            club = req.POST.get('clubs')
            club = Club.objects.get(name=club)

            full_name = req.POST.get('fname') + " " + req.POST.get('lname')
            FanProfile.objects.create(user=user, full_name=full_name, club=club)
            return redirect('login')
        return render(req, 'registration/register.html', context)
    else:

        context = {
            'teams': Club.objects.all(),
            'form': form,
        }
        return render(req, 'registration/register.html', context)


class SuccessfullyView(generic.TemplateView):
    template_name = 'payment.html'


class TicketView(generic.TemplateView):
    template_name = 'ticket.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['match'] = Match.objects.get(id=self.kwargs['pk'])
        entrace = context['match']
        context['entrace'] = get_list_or_404(MatchEntrace, match=entrace)
        return context

class ListTicketView(generic.TemplateView):
    template_name = 'tickets.html'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            context['matchs'] = get_list_or_404(Ticket, user=self.kwargs['pk'])
        except:
            context['no_match'] ='no match'
        context['total_tickets'] = Ticket.objects.filter(user=self.kwargs['pk']).count()        
        return context
