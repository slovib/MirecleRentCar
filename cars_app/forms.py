from django import forms
from django.contrib.auth.models import User
from .models import Rental, Car, Review, Profile, Accessory

# Форма аренды
class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'return_date']
        labels = {
            'start_date': 'Дата начала',
            'return_date': 'Дата возврата',
        }

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def __init__(self, *args, **kwargs):
        self.car_id = kwargs.pop('car_id', None)
        super().__init__(*args, **kwargs)
        self.fields['start_date'].error_messages = {'required': 'Пожалуйста, введите дату начала.'}
        self.fields['return_date'].error_messages = {'required': 'Пожалуйста, введите дату возврата.'}

    def save(self, commit=True):
        rental = super().save(commit=False)
        rental.car_id = self.car_id
        if commit:
            rental.save()
        return rental

# Форма автомобиля
# Форма автомобиля
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'price', 'is_rented', 'is_for_sale', 'image', 'description', 'mileage', 'fuel_type', 'transmission']
        labels = {
            'make': 'Производитель',
            'model': 'Модель',
            'year': 'Год выпуска',
            'price': 'Цена',
            'is_rented': 'Арендован',
            'is_for_sale': 'На продажу',
            'image': 'Изображение',
            'description': 'Описание',
            'mileage': 'Пробег',
            'fuel_type': 'Тип топлива',
            'transmission': 'Коробка передач',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        is_rented = cleaned_data.get('is_rented')
        is_for_sale = cleaned_data.get('is_for_sale')

        # Чтобы не было конфликта, хотя бы одно из полей должно быть True
        if not is_rented and not is_for_sale:
            raise forms.ValidationError("Автомобиль должен быть доступен либо для аренды, либо для продажи.")
        
        return cleaned_data


from django import forms
from .models import Review

from django import forms
from .models import Review

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Поля для оценки и комментария

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя из kwargs
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.instance.user = user  # Присваиваем текущего пользователя полю user




# Форма регистрации
import re
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from .models import Profile  # Импортируй свою модель профиля

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Подтверждение пароля")
    email = forms.EmailField()
    phone_number = forms.CharField(
        max_length=17,
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(attrs={
            'placeholder': '+7 700 679 5801',
            'inputmode': 'tel'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

    # Проверка совпадения паролей
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")

    # Проверка надежности пароля
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
            if not re.search(r'[^A-Za-z0-9]', password):
                raise forms.ValidationError("Пароль должен содержать хотя бы один специальный символ.")

    # Проверка номера телефона
        phone = cleaned_data.get("phone_number")
        if phone:
            phone_cleaned = re.sub(r'\s+', '', phone)
        if not re.match(r'^(\+7|8)\d{10}$', phone_cleaned):
            raise forms.ValidationError("Номер телефона должен начинаться с +7 или 8 и содержать 11 цифр.")
        cleaned_data['phone_number'] = phone_cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # хэширование пароля
        if commit:
            user.save()
            # Создаем профиль и сохраняем номер телефона
            Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user



# Форма входа
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )

# Форма профиля
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

# Форма редактирования пользователя
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }

# Форма аксессуара
class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'description', 'price', 'stock', 'image']
        labels = {
            'name': 'Название аксессуара',
            'description': 'Описание аксессуара',
            'price': 'Цена',
            'stock': 'Количество на складе',
            'image': 'Изображение аксессуара',
        }
        help_texts = {
            'name': 'Введите название аксессуара.',
            'description': 'Опишите аксессуар.',
            'price': 'Укажите цену аксессуара.',
            'stock': 'Количество доступных единиц.',
            'image': 'Загрузите изображение аксессуара.',
        }


# Форма платежа
from django import forms
from django.core.exceptions import ValidationError
import re

from django import forms
from django.core.exceptions import ValidationError
import re

from django import forms
import re

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=19, 
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 1234 5678'}),
        label="Номер карты",
        required=True,
        error_messages={'required': 'Пожалуйста, введите номер карты.'},
    )
    
    expiry_date = forms.CharField(
        max_length=7, 
        widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}),
        label="Дата окончания (MM/YYYY)",
        required=True,
        error_messages={'required': 'Пожалуйста, введите дату окончания.'},
    )

    cvv = forms.CharField(
        max_length=3, 
        widget=forms.PasswordInput(attrs={'placeholder': '***'}),
        label="CVV",
        required=True,
        error_messages={'required': 'Пожалуйста, введите код CVV.'},
    )

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        # Удаляем пробелы и проверяем длину номера
        card_number = card_number.replace(' ', '')
        if len(card_number) not in range(13, 20):
            raise forms.ValidationError('Номер карты должен содержать от 13 до 19 цифр.')
        if not card_number.isdigit():
            raise forms.ValidationError('Номер карты может содержать только цифры.')
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        # Проверяем, что дата в формате MM/YYYY
        if not re.match(r'^(0[1-9]|1[0-2])\/\d{4}$', expiry_date):
            raise forms.ValidationError('Дата должна быть в формате MM/YYYY.')
        
        month, year = expiry_date.split('/')
        if int(month) < 1 or int(month) > 12:
            raise forms.ValidationError('Месяц должен быть в пределах от 01 до 12.')
        
        # Дополнительная проверка на год, например, чтобы не был в прошлом
        current_year = 2025  # Здесь можно подставить текущий год из datetime
        current_month = 1    # Текущий месяц
        if int(year) < current_year or (int(year) == current_year and int(month) < current_month):
            raise forms.ValidationError('Дата истечения срока не может быть в прошлом.')

        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if len(cvv) != 3 or not cvv.isdigit():
            raise forms.ValidationError('CVV должен содержать только 3 цифры.')
        return cvv





# Форма карты
class CardForm(forms.Form):
    card_number = forms.CharField(max_length=16, label='Номер карты')
    cardholder_name = forms.CharField(max_length=100, label='Имя на карте')
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата истечения')
    cvv = forms.CharField(max_length=3, label='CVV')
