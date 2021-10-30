from loginapp import tickect
from django.conf import settings
from django.shortcuts import (
    render, redirect, get_object_or_404, get_list_or_404
)

from django.contrib import messages
from django.utils.crypto import get_random_string
from pypesa.vodacom import MPESA
from .models import *

from .forms import PaymentForm



def repay(request, pk):
    ticket = Ticket.objects.get(id=pk)

    user = ticket.user
    token = ticket.ticket_number
    amount = ticket.amount

    api_key = 'pass-auth-key'
    public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ=='

    try:
        # Instatiate API context
        m_pesa = MPESA(api_key, public_key)

        if m_pesa:    
            desc = str("form ticket " + str(token))

            # Constructing parameters 
            parameters = {
                'input_Amount': amount,
                'input_Country': 'TZN',
                'input_Currency': 'TZS',
                'input_CustomerMSISDN': '000000000001',
                'input_ServiceProviderCode': '000000',
                'input_ThirdPartyConversationID': get_random_string(18),
                'input_TransactionReference': token,
                'input_PurchasedItemsDesc': desc,
            }
            
            # make an API call
            results = m_pesa.customer2business(parameters)

            # processing results from API call
            if results.body['output_ResponseCode'] == 'INS-0':
                Payment.objects.create(user=user, ticket = ticket, amount=amount)
                ticket.payed = True
                ticket.save()
                Ticket.save()
                

                messages.success(
                    request, 'Your Payment was Successfully sent!')
                return redirect('loginapp:tickets', pk=user.id)

            else:
                messages.error(request, results.body['output_ResponseDesc'])

    except:
        messages.error(
                request, 'Whuuh!!!!! Connection error..!!! Payments unsuccessfully'
                )
    return redirect('loginapp:tickets', pk=user.id )


def payment(request, pk):
    template_name = 'ticket.html'
    match = Match.objects.get(id=pk)
    context={'match':match}
    
    api_key = 'pass-auth-key'
    public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ=='

    if request.method == 'POST':
        raw_amount = request.POST.get('price')
        amount = int(raw_amount)
        token = get_random_string(6)
        user = request.user

        old_ticket = Ticket.objects.filter(user=user, match=match).first()

        # checks if tickets exists and payed
        if old_ticket:
            if old_ticket.payed == True:
                messages.error(
                        request, 'Can\'t book twice, either print your ticket! one ticket per match'
                        )
                return render(request, template_name, context)  

            else:
                
                messages.error(
                        request, 'You have to pay for it since you are ready booked this ticket!!'
                        )
                return redirect('loginapp:tickets', pk=user.id)

        # ticket does not exists
        else:
            # create new ticket
            ticket = Ticket.objects.create(
                user = user,
                ticket_number = token,
                match = match,
                amount = amount,
            )

            ticket.save()


        if ticket:
            try:
                # Instatiate API context
                m_pesa = MPESA(api_key, public_key)

                if m_pesa:    
                    desc = str("form ticket " + str(token))

                    # Constructing parameters 
                    parameters = {
                        'input_Amount': amount,
                        'input_Country': 'TZN',
                        'input_Currency': 'TZS',
                        'input_CustomerMSISDN': '000000000001',
                        'input_ServiceProviderCode': '000000',
                        'input_ThirdPartyConversationID': get_random_string(18),
                        'input_TransactionReference': token,
                        'input_PurchasedItemsDesc': desc,
                    }
                    

                    
                    # make an API call
                    results = m_pesa.customer2business(parameters)

                    # processing results from API call
                    if results.body['output_ResponseCode'] == 'INS-0':
                        ticket.payed = True
                        ticket.save()
                        Payment.objects.create(user=user, ticket = ticket, amount=amount)
                        
                        

                        messages.success(
                            request, 'Your Payment was Successfully sent!')
                        return redirect('loginapp:tickets', pk=user.id)

                    else:
                        messages.error(request, results.body['output_ResponseDesc'])

            except:
                messages.error(
                        request, 'Whuuh!!!!! Connection error..!!! Payments unsuccessfully'
                        )


            return render(request, template_name, context)

        else:
            messages.error(
                                request, 'Invalid Ticket, book again!!')

            return render(request, template_name, context)

    
    return render(request, template_name, context)


