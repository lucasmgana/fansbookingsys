from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django .contrib.auth.models import User
from django.views import generic

from .models import *
from .forms import *

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


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



def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def get_ticket(pk, tn):
    payed = False
    try:
        user = User.objects.get(id=pk)
        ticket = get_object_or_404(Ticket, user=pk, ticket_number=str(tn))
        if Payment.objects.filter(ticket=ticket):
            payed = True
        
        
        # match for class status
        m = Match.objects.filter(
            home_team=ticket.match.home_team, 
            away_team=ticket.match.away_team, 
            date=ticket.match.date, 
            stadium=ticket.match.stadium,
            ).first()

        # entrace for match class
        en = MatchEntrace.objects.get(match=m)

        # geting a class
        def get_status(self):
            if en.vip_price == ticket.amount:
                return 'VIP'
            
            elif en.mzunguko_price == ticket.amount:
                return 'MZUNGUKO'
            
            else:
                return 'PLATNUM'
            
        
        status = get_status(en)

    except:
        ticket = None

    # status=Payment.objects.get(amount=ticket)
    data = {
            'customer':user,
            'home':ticket.match.home_team,
            'away':ticket.match.away_team,
            'stadium':ticket.match.stadium,
            'date':ticket.match.date,

            'amount':ticket.amount,
            'pay_stat':payed,
            'status': status,
            'token':ticket.ticket_number,      
            
    }
    
    
    return data


#Opens up page as PDF
class ViewTicket(View):
	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('myticket.html', get_ticket(kwargs['pk'], kwargs['tn']))
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadTicket(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('myticket.html',  get_ticket(kwargs['pk'], kwargs['tn']))

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Ticket%s.pdf" %(request.user.fanprofile.full_name)
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response
