from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Img

#admin.site.register(Img)

@admin.register(Img)

# Register your models here.
class ImgAdmin(ImportExportModelAdmin):
    pass

admin.site.site_header = "Image Classifier Admin/Log-In Page"
admin.site.index_title = "Site and Model Administration"