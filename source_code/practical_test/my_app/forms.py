from django import forms
from django_countries.fields import CountryField


PAYMENT_CHOICES = (
    ('C', 'Cheque'),
    ('P', 'PayPal')
)


class CheckOutForm(forms.Form):
    # name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name"}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    phone_number = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "Phone_number"}), max_digits=10)
    e_mail = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "E-mail"}))
    # country = CountryField(blank_label='Select Country').formfield()
    country = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Country"}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Address_line_1"}))
    address_line_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Address_line_2"}))
    state = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "State"}))
    city = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "City"}))
    postal_code = forms.DecimalField(widget=forms.TextInput(attrs={"placeholder": "postal"}),max_digits=10, decimal_places=10)
    # notes = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "notes"}))
    payment_options = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    # terms_conditions = forms.BooleanField()
