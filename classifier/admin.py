from django.contrib import admin
from django.dispatch import receiver
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import Img
from django.core import files
from django.core.files.uploadedfile import SimpleUploadedFile
from import_export.signals import post_import



class ImgResource(resources.ModelResource):

    class Meta:
        model = Img
    # hook into the import export here somehow...????

# Register your models here.
@admin.register(Img)
class data_import(ImportExportModelAdmin):
    resource_class = ImgResource

admin.site.site_header = "Image Classifier Admin/Log-In Page"
admin.site.index_title = "Site and Model Administration"