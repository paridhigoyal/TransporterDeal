from django import forms
from django.core.exceptions import ValidationError

from .models import *
from django.forms import CharField, ModelForm
from allauth.account.forms import SignupForm

# from .. import transportation


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    # type = (
    #     ('T', 'Transporter'),
    #     ('C', 'Customer'),
    # )
    email = forms.EmailField(label='Email', required=True)
    is_customer = forms.BooleanField(label='Customer', required=False)
    is_transporter = forms.BooleanField(label='Transporter', required=False)
    # profile_type = forms.CharField(max_length=1, widget=forms.Select(choices=type))  # type: CharField
    phone = forms.CharField(max_length=12, label='Phone', required=True)
    address = forms.CharField(max_length=100, label='Address')
    city = forms.CharField(max_length=30, label='City')
    state = forms.CharField(max_length=30, label='State')
    pin_code = forms.CharField(max_length=6, label='Pin Code')

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
        user.is_customer = self.cleaned_data['is_customer']
        user.is_transporter = self.cleaned_data['is_transporter']
        if user.is_customer:
            user.is_transporter = False

        elif user.is_transporter:
            user.is_customer = False
            # user.has_perm(transportation.add_vehicle)=True
        # import pdb;pdb.set_trace()
        user.save()
        return user
    # def clean(self):


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {'transporter': forms.HiddenInput()}

    def save(self, request):
    # def clean(self):
        vehicle = super(VehicleForm, self).save(request)
        man_Year = self.cleaned_data.get('man_Year')
        # import pdb;pdb.set_trace()
        if man_Year < 2000 or man_Year > 2020:
            raise ValidationError('Invalid value')
        # return self.cleaned_data
        # vehicle.save(request)
        return vehicle


class DealForm(ModelForm):
    class Meta:
        model = Deal
        fields = '__all__'


class SearchForm(ModelForm):
    start_city = forms.CharField(required=False)
    end_city = forms.CharField(required=False)
    start_Date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    class Meta:
        model = Deal
        fields = ['start_city', 'end_city', 'start_Date', 'end_date']


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
