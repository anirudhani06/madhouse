from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    coverpic = forms.ImageField(
        widget=forms.FileInput({"id": "image_input"}), required=False
    )
    name = forms.CharField(widget=forms.TextInput({"placeholder": "Room Name"}))
    category = forms.CharField(
        widget=forms.TextInput({"placeholder": "Category", "list": "categ_list"})
    )
    is_private = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = Room
        fields = ("coverpic", "name", "category", "is_private")
