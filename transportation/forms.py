from django import forms
from django.contrib.auth.models import Group

from .models import *
from django.forms import CharField, ModelForm
from allauth.account.forms import SignupForm


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    type = (
        ('T', 'Transporter'),
        ('C', 'Customer'),
    )
    email = forms.EmailField(label='Email', required=True)
    # is_customer = forms.BooleanField(label='Customer', required=False)
    # is_transporter = forms.BooleanField(label='Transporter', required=False)
    profile_type = forms.ChoiceField(choices=type)
    phone = forms.CharField(max_length=12, label='Phone', required=True)
    address = forms.CharField(max_length=100, label='Address')
    city = forms.CharField(max_length=30, label='City')
    state = forms.CharField(max_length=30, label='State')
    pin_code = forms.CharField(max_length=6, label='Pin Code')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('Phone number can only contains digits')
        elif len(phone) != 10:
            raise forms.ValidationError('Length of phone number must be 10 digits')
        return phone

    def clean_pin_code(self):
        pin_code = self.cleaned_data['pin_code']
        if not pin_code.isdigit():
            raise forms.ValidationError('Pincode can only contains digits')
        elif len(pin_code) != 6:
            raise forms.ValidationError('Length of Pincode must be 6 digits')
        return pin_code

    def clean_city(self):
        city = self.cleaned_data['city']
        if not city.isalpha():
            raise forms.ValidationError('City can only contains alphabets')
        return city

    def clean_state(self):
        state = self.cleaned_data['state']
        if not (state.isalpha()):
            raise forms.ValidationError('State can only contains alphabets')
        return state

    def save(self, request):
        # import pdb;pdb.set_trace()
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.city = self.cleaned_data['city']
        user.state = self.cleaned_data['state']
        user.pin_code = self.cleaned_data['pin_code']
        if request.POST['profile_type'] == 'C':
            user.is_customer = True
            group = Group.objects.get(name="Customer")
            group.user_set.add(user)
            group.save()
        elif request.POST['profile_type'] == 'T':
            user.is_transporter = True
            group = Group.objects.get(name="Transporter")
            group.user_set.add(user)
            group.save()
        user.save()
        return user


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {'transporter': forms.HiddenInput()}

    def clean_man_Year(self):
        man_Year = self.cleaned_data['man_Year']
        if man_Year < 2000 or man_Year > 2020:
            raise forms.ValidationError('Between 2000 to 2020 is accepted')
        return man_Year

    def clean_color(self):
        color = self.cleaned_data['color']
        if not color.isalpha():
            raise forms.ValidationError('Color can contain alphabets')
        return color

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if not capacity > 0:
            raise forms.ValidationError('Capacity can contain only positive value')
        return capacity


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = '__all__'

    def clean(self):
        start_Date = self.cleaned_data['start_Date']
        end_date = self.cleaned_data['end_date']
        if not start_Date <= end_date:
            raise forms.ValidationError('Start Date must be smaller than or equal to end date')
        return self.cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        if not price > 0:
            raise forms.ValidationError('Price can contain only positive value')
        return price


class SearchForm(ModelForm):
    start_city = forms.CharField(required=False)
    end_city = forms.CharField(required=False)
    start_Date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    class Meta:
        model = Deal
        fields = ['start_city', 'end_city', 'start_Date', 'end_date']

    def clean(self):
        start_Date = self.cleaned_data['start_Date']
        end_date = self.cleaned_data['end_date']
        if not start_Date <= end_date:
            raise forms.ValidationError('Start Date must be smaller than or equal to End Date')
        return self.cleaned_data


class QueryRequestForm(ModelForm):
    class Meta:
        model = QueryRequest
        fields = '__all__'
        widgets = {'deal': forms.HiddenInput(), 'username': forms.HiddenInput()}


class QueryResponseForm(ModelForm):
    class Meta:
        model = QueryResponse
        fields = '__all__'
        widgets = {'request_id': forms.HiddenInput(), 'username': forms.HiddenInput()}


class RatingForm(ModelForm):
    rate = (('1', 'Worst Experience'), ('2', 'Bad Experience',),
            ('3', 'Good Experience'), ('4', 'Very Good Experience'),
            ('5', 'Excellent Experience')
            )
    rating = forms.CharField(max_length=1, widget=forms.Select(choices=rate))

    class Meta:
        model = Rating
        fields = '__all__'
