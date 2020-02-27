from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer = models.BooleanField('customer status', default=False)
    is_transporter = models.BooleanField('transporter status', default=False)
    address = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=30, default="")
    state = models.CharField(max_length=30, default="")
    phone = models.CharField(max_length=12, default="")
    pin_code = models.CharField(max_length=6, default="")

    def __str__(self):
        return self.username


class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=15)
    man_Year = models.IntegerField()
    capacity = models.IntegerField()
    unit = models.CharField(max_length=5,default="kgs")
    picture = models.ImageField(null=True, upload_to="gallery")
    document = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    transporter = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __unicode__(self):
        return self.id


class Deal(models.Model):
    deal_id = models.IntegerField(primary_key=True)
    start_Date = models.DateField()
    end_date = models.DateField()
    start_city = models.CharField(max_length=50)
    end_city = models.CharField(max_length=50)
    price = models.IntegerField()
    unit = models.CharField(max_length=5, default="Rs")
    # transporter = models.ManyToManyField(Profile)
    transporter = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_id = models.OneToOneField(Vehicle, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.id


class Rating(models.Model):
    rate = (('1', 'Worst Experience'), ('2', 'Bad Experience',),
            ('3', 'Good Experience'), ('4', 'Very Good Experience'),
            ('5', 'Excellent Experience')
            )
    rating = models.CharField(max_length=1, choices=rate)
    transporter = models.ForeignKey(User, on_delete=models.CASCADE)
    deal_id = models.OneToOneField(Deal, on_delete=models.CASCADE)

    def __str__(self):
        return self.transporter.username


class QueryRequest(models.Model):
    c_request = models.TextField(default="")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.id


class QueryResponse(models.Model):
    t_response = models.TextField(default="")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    request_id = models.OneToOneField(QueryRequest, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.id
