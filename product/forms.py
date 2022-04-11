from django import forms
from .models import BillingAddress, Product


def text_inp_widget(class_name="form-control", type_div="text", placeholder="name"):
    return forms.TextInput(attrs={
    'class': class_name,
    'type': type_div,
    "placeholder": str(placeholder)})


class BillingAddressForm(forms.ModelForm):
    order = forms.CharField(required=False)
    first_name = forms.CharField(
        widget=text_inp_widget(placeholder="john")
    )
    last_name = forms.CharField(widget=text_inp_widget(placeholder="doe"))
    email = forms.CharField(widget=text_inp_widget(placeholder="yourmail@gmail.com"))
    mobile = forms.CharField(widget=text_inp_widget(placeholder="+880 **********"))
    address = forms.CharField(widget=text_inp_widget(placeholder="Gulshan, Dhaka"))
    city = forms.CharField(widget=text_inp_widget(placeholder="Dhaka"))
    zip = forms.CharField(widget=text_inp_widget(placeholder="Dhaka"))

    class Meta:
        model = BillingAddress
        # exclude = ["order", ]
        fields = "__all__"

class ProductAdminAddForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["name", "description", "price", "category"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        qs = Product.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Unique")
        return name


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        