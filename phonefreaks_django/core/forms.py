from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Phone

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}))

class PhoneForm(forms.ModelForm):
    # Explicit fields for Prices
    price_amazon = forms.IntegerField(label="Price (Amazon)", required=True, widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))
    price_flipkart = forms.IntegerField(label="Price (Flipkart)", required=True, widget=forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))

    # Explicit fields for Specs
    spec_display = forms.CharField(label="Display", required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))
    spec_processor = forms.CharField(label="Processor", required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))
    spec_camera = forms.CharField(label="Camera", required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))
    spec_battery = forms.CharField(label="Battery", required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))
    spec_os = forms.CharField(label="OS", required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}))

    class Meta:
        model = Phone
        fields = ['id', 'brand', 'model', 'description', 'image']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'placeholder': 'e.g., iphone-15-pro'}),
            'brand': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'model': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg', 'rows': 4, 'required': False}),
            'image': forms.URLInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        
        if instance:
            # Populate initial data from JSON fields
            if instance.prices:
                initial['price_amazon'] = instance.prices.get('amazon')
                initial['price_flipkart'] = instance.prices.get('flipkart')
            
            if instance.specs:
                initial['spec_display'] = instance.specs.get('display')
                initial['spec_processor'] = instance.specs.get('processor')
                initial['spec_camera'] = instance.specs.get('camera')
                initial['spec_battery'] = instance.specs.get('battery')
                initial['spec_os'] = instance.specs.get('os')
        
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        
        # Make ID field read-only when editing an existing phone
        if instance:
            self.fields['id'].widget.attrs['readonly'] = True
            self.fields['id'].help_text = 'ID cannot be changed after creation'

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Construct JSON fields
        instance.prices = {
            'amazon': self.cleaned_data['price_amazon'],
            'flipkart': self.cleaned_data['price_flipkart']
        }
        
        instance.specs = {
            'display': self.cleaned_data['spec_display'],
            'processor': self.cleaned_data['spec_processor'],
            'camera': self.cleaned_data['spec_camera'],
            'battery': self.cleaned_data['spec_battery'],
            'os': self.cleaned_data['spec_os']
        }
        
        if commit:
            instance.save()
        return instance
