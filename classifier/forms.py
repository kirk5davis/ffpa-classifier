# classifier/forms.py
from django import forms
from .models import Img


class ImgUpdateForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ['image_classification', 'updated_by_user']
        widgets = {'updated_by_user': forms.HiddenInput(), 'image_classification': forms.HiddenInput()}
    # template_name_suffix = '_update_form'
