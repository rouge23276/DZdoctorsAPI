from django.contrib import admin
from .models import Doctor, Review, Organization, Service, Education, MediaItem, WorkingHours

admin.site.register(Doctor)
admin.site.register(Review)
admin.site.register(Organization)
admin.site.register(Service)
admin.site.register(Education)
admin.site.register(MediaItem)
admin.site.register(WorkingHours)