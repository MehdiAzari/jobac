from django.contrib import admin
from .models import User, Freelancer, Employer,Skills,Document
# Register your models here.

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Freelancer)
admin.site.register(Skills)
admin.site.register(Document)