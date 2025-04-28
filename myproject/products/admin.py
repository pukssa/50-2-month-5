from django.contrib import admin
from .models import product, category, review

admin.site.register(product)
admin.site.register(category)
admin.site.register(review)