from django.contrib import admin
from .models import author
from .models import category
from .models import article

# Register your models here.
class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__","details"]
    class Meta:
        model = author

admin.site.register(author, authorModel)

class articleModel(admin.ModelAdmin):
    list_display = ["__str__","publish_date"]
    search_fields = ["__str__","details"]
    list_per_page = 10
    list_filter = ["publish_date", "category"]

    class Meta:
        model = article

admin.site.register(article,articleModel)

class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]

    class Meta:
        model = category
admin.site.register(category, categoryModel)

