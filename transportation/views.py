from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Vehicle, Deal, QueryRequest, QueryResponse, Rating
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import VehicleForm, DealForm, SearchForm, QueryRequestForm, QueryResponseForm, RatingForm, UpdateProfileForm


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

@login_required
def update_profile(request,id):
    User = get_user_model()
    user = User.objects.get(id=id)
    form = UpdateProfileForm(instance=user)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        form.save()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'edit_profile.html', {'form': form})

@login_required
@permission_required('transportation.add_vehicle', raise_exception=True)
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vehicle-list'))
        else:
            return render(request, 'add_vehicle.html', {'form': form})
    form = VehicleForm(initial={'transporter': request.user.id})
    return render(request, 'add_vehicle.html', {'form': form})


@login_required
@permission_required('transportation.view_vehicle', raise_exception=True)
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(transporter_id=request.user.id)
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


@login_required
@permission_required('transportation.change_vehicle', raise_exception=True)
def update_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        form.save()
        return HttpResponseRedirect(reverse('vehicle-list'))
    form = VehicleForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form})


@login_required
@permission_required('transportation.delete_vehicle', raise_exception=True)
def delete_vehicle(request, id):
    vehicle = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle-list')
    return render(request, 'delete_vehicle.html', {'vehicle': vehicle})


@login_required
@permission_required('transportation.view_deal', raise_exception=True)
def view_deal(request, deal_id):
    deal = Deal.objects.get(deal_id=deal_id)
    return render(request, 'view_deal.html', {'deal': deal})


@login_required
@permission_required('transportation.add_deal', raise_exception=True)
def create_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'create_deal.html', {'form': form})
        return HttpResponseRedirect(reverse('deal-list'))
    form = DealForm(initial={'transporter': request.user.id})
    form.fields['vehicle_id'].queryset=Vehicle.objects.filter(transporter=request.user)
    return render(request, 'create_deal.html', {'form': form})


@login_required
@permission_required('transportation.view_deal', raise_exception=True)
def deal_list(request):
    deals = Deal.objects.all()
    context = {'deals': deals}
    return render(request, 'deal_list.html', context)


@login_required
@permission_required('transportation.delete_deal', raise_exception=True)
def delete_deal(request, deal_id):
    deal = Deal.objects.get(deal_id=deal_id, transporter=request.user)
    deal.delete()
    if request.method == 'POST':
        deal.delete()
        return redirect('deal-list')
    return render(request, 'delete_vehicle.html', {'deal': deal})


@login_required
@permission_required('transportation.change_deal', raise_exception=True)
def edit_deal(request, deal_id):
    deal = Deal.objects.get(deal_id=deal_id, transporter=request.user)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        form.save()
        return HttpResponseRedirect(reverse('deal-list'))
    form = DealForm(instance=deal)
    return render(request, 'edit_deal.html', {'form': form})


@login_required
def view_image(request, id):
    vehicle = Vehicle.objects.get(id=id)
    return render(request, 'view_image.html', {'vehicle': vehicle})


@login_required
@permission_required('transportation.add_queryrequest', raise_exception=True)
def ask_query(request, deal_id):
    if request.method == 'POST':
        form = QueryRequestForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('view-query', args=[deal_id]))
    form = QueryRequestForm(initial={'username': request.user.id, 'deal': deal_id})
    return render(request, 'ask_query.html', {'form': form})


@login_required
@permission_required('transportation.view_queryrequest', raise_exception=True)
def view_query(request, deal_id):
    query = QueryRequest.objects.get(deal_id=deal_id)
    return render(request, 'view_query.html', {'query': query})


@login_required
@permission_required('transportation.add_queryresponse', raise_exception=True)
def response_query(request, request_id):
    if request.method == 'POST':
        form = QueryResponseForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('view-response', args=[request_id]))
    form = QueryResponseForm(initial={'username': request.user.id, 'request_id': request_id})
    context = {'form': form, 'request_id_id': request_id}
    return render(request, 'response_query.html', context)


@login_required
@permission_required('transportation.view_queryresponse', raise_exception=True)
def view_response(request, request_id):
    query = QueryResponse.objects.get(request_id=request_id)
    return render(request, 'view_response.html', {'query': query})


@login_required
@permission_required('transportation.add_rating', raise_exception=True)
def give_rating(request, deal_id):
    if request.method == 'POST':
        form = RatingForm(request.POST)

        form.save()
        return HttpResponseRedirect(reverse('home'))
    form = RatingForm(initial={'transporter': request.user.id, 'deal_id': deal_id})
    return render(request, 'give_rating.html', {'form': form})


@login_required
@permission_required('transportation.view_rating', raise_exception=True)
def view_rating(request, deal_id):
    rating = Rating.objects.get(deal_id=deal_id)
    return render(request, 'view_rating.html', {'rating': rating})
