from django.contrib import admin
from .models import *


# Register your models here.

class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ['student', 'company', 'rating']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(IntershalaEmployee)
admin.site.register(AdminNotification)
admin.site.register(EmployeeNotification)
admin.site.register(IntershalaAdmin)
admin.site.register(IntershalaCompany)
admin.site.register(CompanyReview, CompanyReviewAdmin)
