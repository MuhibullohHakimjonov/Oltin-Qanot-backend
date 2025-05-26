from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Volunteer)
admin.site.register(Investor)

admin.site.register(PhoneVerification)
