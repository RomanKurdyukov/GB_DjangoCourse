import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.shortcuts import get_object_or_404
from django.template import RequestContext

from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductCategory, Product, VendorCode


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вам нет 18 лет!")
        return data

    def save(self):

        user = super(ShopUserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            if field_name == 'is_active' or field_name == 'is_staff' or field_name == 'is_superuser':
                field.widget.attrs['class'] = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вам нет 18 лет!")
        return data


class ProductCategoryAddForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(ProductCategoryEditForm, self).__init__(*args, **kwargs)



class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ('category', 'vendor_code',)


class VcAddForm(forms.ModelForm):
    class Meta:
        model = VendorCode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VcAddForm, self).__init__(*args, **kwargs)


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('vendor_code',)

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'about_me', 'gender')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        # for field_name, field in self.fields.items():
        #     field.widget.attrs['class'] = 'form-control'