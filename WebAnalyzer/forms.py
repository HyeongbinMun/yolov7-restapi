from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select an image')
    conf_thresh = forms.FloatField(label='Confidence Threshold', initial=0.1, min_value=0, max_value=1)