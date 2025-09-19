from django import forms


class AddressForm(forms.Form):
    city = forms.CharField(max_length=100, label='شهر')
    province = forms.CharField(max_length=100, label='استان')
    description = forms.CharField(widget=forms.Textarea, label='توضیحات آدرس')
    postal_code = forms.CharField(max_length=10, label='کد پستی')

    # یک متد برای ترکیب فیلدها و ساخت یک آدرس کامل
    def get_combined_address(self):
        city = self.cleaned_data.get('city')
        province = self.cleaned_data.get('province')
        description = self.cleaned_data.get('description')
        postal_code = self.cleaned_data.get('postal_code')

        return f"{province}, {city}, {description}, کد پستی: {postal_code}"