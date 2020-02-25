from django.contrib import admin
#from .models import Deal
#from .models import Vehicle
from .models import *

# admin.site.register(User)
admin.site.register(Deal)
admin.site.register(Vehicle)
admin.site.register(Rating)
admin.site.register(QueryRequest)
admin.site.register(QueryResponse)
admin.site.register(User)
# Register your models here.
#admin.site.register(Transporter)
#admin.site.register(Customer)