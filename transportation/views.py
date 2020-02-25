from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Vehicle, Deal, QueryRequest, QueryResponse, Rating
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import VehicleForm, DealForm, SearchForm, QueryRequestForm, QueryResponseForm, RatingForm, \
    MyCustomSignupForm
from allauth.account.views import LoginView


def index(request):
    queryset = request.GET.get('start_city')
    queryset1 = request.GET.get('end_city')
    queryset2 = request.GET.get('start_Date')

    queryset3 = request.GET.get('end_date')
    if queryset and queryset1:
        deal_lists = Deal.objects.filter(Q(start_city__icontains=queryset), Q(end_city__icontains=queryset1))
        if queryset2 and queryset3:
            deal_lists = deal_lists.filter(Q(start_Date=queryset2), Q(end_date=queryset3))
        form = SearchForm()
        context = {'deal_lists': deal_lists, 'form': form}

        return render(request, 'transporter_index.html', context)

    else:
        form = SearchForm()
        return render(request, 'transporter_index.html', {'form': form})


# def update_profile(request,id):
#     profile = User.objects.get(id=id)
#     form = MyCustomSignupForm(instance=profile)
#     if request.method == 'POST':
#         form = MyCustomSignupForm(request.POST, instance=profile)
#         form.save()
#         return HttpResponseRedirect(reverse('home'))
#
#     return render(request, 'edit_profile.html', {'form': form})


def add_vehicle(request):
    # if request.man_Year
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
        return HttpResponseRedirect(reverse('vehicle-list'))
    form = VehicleForm(initial={'transporter': request.user.id})
    return render(request, 'add_vehicle.html', {'form': form})


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def update_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        form.save()
        return HttpResponseRedirect(reverse('vehicle-list'))
    form = VehicleForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form})


def delete_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle-list')
    return render(request, 'delete_vehicle.html', {'vehicle': vehicle})


def view_deal(request, deal_id):
    deal = Deal.objects.get(deal_id=deal_id)
    return render(request, 'view_deal.html', {'deal': deal})


def create_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        # import pdb;pdb.set_trace()
        form.save()
        return HttpResponseRedirect(reverse('deal-list'))
    form = DealForm()
    return render(request, 'create_deal.html', {'form': form})


def deal_list(request):
    deals = Deal.objects.all()
    # rating=Rating.objects.all()
    context ={'deals': deals}
    return render(request, 'deal_list.html', context)


def delete_deal(request, deal_id):
    deal = Deal.objects.get(deal_id=deal_id)
    if request.method == 'POST':
        deal.delete()
        return redirect('deal-list')
    return render(request, 'delete_vehicle.html', {'deal': deal})


def edit_deal(request, deal_id):
    deal = Deal.objects.get(deal_id=deal_id)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        form.save()
        return HttpResponseRedirect(reverse('deal-list'))
    form = DealForm(instance=deal)
    return render(request, 'edit_deal.html', {'form': form})


def view_image(request, id):
    vehicle = Vehicle.objects.get(id=id)
    return render(request, 'view_image.html', {'vehicle': vehicle})


def ask_query(request, deal_id):
    if request.method == 'POST':
        form = QueryRequestForm(request.POST)
        form.save()
        # import pdb;pdb.set_trace()
        return HttpResponseRedirect(reverse('view-query', args=[deal_id]))
    form = QueryRequestForm(initial={'username': request.user.id, 'deal': deal_id})
    return render(request, 'ask_query.html', {'form': form})


def view_query(request, deal_id):
    query = QueryRequest.objects.get(deal_id=deal_id)
    # import pdb;pdb.set_trace()
    return render(request, 'view_query.html', {'query': query})


def response_query(request, request_id):
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        form = QueryResponseForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('view-response', args=[request_id]))
    form = QueryResponseForm(initial={'username': request.user.id, 'request_id': request_id})
    context = {'form': form, 'request_id_id': request_id}
    return render(request, 'response_query.html', context)


def view_response(request, request_id):
    query = QueryResponse.objects.get(request_id=request_id)
    return render(request, 'view_response.html', {'query': query})


def give_rating(request, deal_id):
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = RatingForm(request.POST)

        form.save()
        return HttpResponseRedirect(reverse('home'))
    form = RatingForm(initial={'transporter': request.user.id, 'deal_id': deal_id})
    return render(request, 'give_rating.html', {'form': form})


def view_rating(request, deal_id):
    rating = Rating.objects.get(deal_id=deal_id)
    # import pdb;
    # pdb.set_trace()
    return render(request, 'view_rating.html', {'rating': rating})
