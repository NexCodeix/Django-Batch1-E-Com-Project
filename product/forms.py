from django import forms
from .models import BillingAddress


def text_inp_widget(placeholder):
    return forms.TextInput(attrs={
    'class': 'form-control',
    "placeholder": str(placeholder)})


class BillingAddressForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=text_inp_widget("john")
    )
    last_name = forms.CharField(widget=text_inp_widget("doe"))
    class Meta:
        model = BillingAddress
        fields = "__all__"

    def clean_mobile(self):
        number = self.cleaned_data.get("mobile")
        num = number[:4]
        # if (num != "+880") or (num != "018") or (num != "017") or (num != "016"):
        #     raise forms.ValidationError("pls type a bd number")

        print(num)

        return self.cleaned_data.get("mobile")
