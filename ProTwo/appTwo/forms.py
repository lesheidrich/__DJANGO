from django import forms
from appTwo.models import User

class NewUserForm(forms.ModelForm):
    # validation here

    class Meta():
        model = User
        fields = "__all__"

