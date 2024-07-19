from django import forms
from django.core import validators

def check_start_with_j(value):
    if value[0].lower() != 'j':
        raise forms.ValidationError("Name needs to start with j")

class FormName(forms.Form):
    name = forms.CharField(validators=[check_start_with_j])
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter your email again')
    text = forms.CharField(widget=forms.Textarea)

    # botcheck
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
    
    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data.get('email')
        vmail = all_clean_data.get('verify_email')
        # email = all_clean_data['email']
        # vmail = all_clean_data['verify_email']

        if email != vmail:
            raise forms.ValidationError("Emails don't match!")
    
    # def clean_botcatcher(self) -> forms.CharField:
    #     """
    #     If bot fills in extra field acting as honeytrap it won't submit.
    #     returns: forms.botcatcher instance (hidden input)
    #     """
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("Bot found!")
    #     return botcatcher