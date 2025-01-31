from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Car, Accessory, Order, Review, Rental, Profile, Cart
from .forms import (CarForm, CardForm, PaymentForm, ReviewForm,
                    RentalForm, RegistrationForm, LoginForm,
                    ProfileForm, UserEditForm, AccessoryForm)
from django.db.models import Q

# Проверка, является ли пользователь продавцом или администратором
def is_seller_or_staff(user):
    return user.is_staff or (hasattr(user, 'profile') and user.profile.is_seller)
def index(request):
    return render(request, 'index.html')
# Список автомобилей
def car_list(request):
    cars = Car.objects.filter(is_rented=True, is_for_sale=False)
    
    # Фильтрация автомобилей по запросам
    query = request.GET.get('q')
    if query:
        cars = cars.filter(Q(make__icontains=query) | Q(model__icontains=query))
    
    # Дополнительные фильтры
    filters = {
        'make': request.GET.get('make'),
        'model': request.GET.get('model'),
        'min_price': request.GET.get('min_price'),
        'max_price': request.GET.get('max_price'),
    }
    
    for key, value in filters.items():
        if value:
            if key in ['min_price', 'max_price']:
                filter_lookup = f'price__{"gte" if key == "min_price" else "lte"}'
                cars = cars.filter(**{filter_lookup: value})
            else:
                cars = cars.filter(**{f'{key}__iexact': value})
    
    return render(request, 'car_list.html', {'cars': cars})

# Список аксессуаров
def accessory_list(request):
    accessories = Accessory.objects.all()
    cart_item_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'accessories/accessory_list.html', {'accessories': accessories, 'cart_item_count': cart_item_count})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Car, Review
from .forms import ReviewForm

# Детали автомобиля
from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Review
from .forms import ReviewForm
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Review
from .forms import ReviewForm
from django.contrib import messages

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()

    if request.method == 'POST':
        # Передаем текущего пользователя в форму
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car  # Привязываем отзыв к автомобилю
            review.save()
            messages.success(request, 'Ваш отзыв был добавлен!')
            return redirect('car_detail', car_id=car.id)
    else:
        form = ReviewForm()

    return render(request, 'car_detail.html', {'car': car, 'reviews': reviews, 'form': form})




# Добавление автомобиля (только для продавцов и администраторов)
# Добавление автомобиля (только для продавцов и администраторов)
@user_passes_test(is_seller_or_staff)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            # Проверим, для чего добавлен автомобиль
            if car.is_for_sale:
                messages.success(request, 'Автомобиль успешно добавлен на продажу!')
            elif car.is_rented:
                messages.success(request, 'Автомобиль успешно добавлен для аренды!')
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


# Редактирование автомобиля
@user_passes_test(is_seller_or_staff)
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные автомобиля успешно обновлены!')
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'edit_car.html', {'form': form, 'car': car})

# Удаление автомобиля
@user_passes_test(is_seller_or_staff)
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Автомобиль успешно удален!')
        return redirect('car_list')
    return render(request, 'delete_car.html', {'car': car})

# Аренда автомобиля
@login_required
def rent_car(request, car_id):
    selected_car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = RentalForm(request.POST, car_id=selected_car.id)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.user = request.user
            
            # Рассчет стоимости аренды
            rental_days = (rental.return_date - rental.start_date).days
            rental.total_price = rental.car.price * rental_days
            
            # Имитируем успешную аренду
            rental.car.is_rented = True
            rental.save()
            rental.car.save()
            
            messages.success(request, 'Автомобиль успешно арендован!')
            return redirect('profile')
    else:
        form = RentalForm(car_id=selected_car.id)

    return render(request, 'rent_car.html', {'form': form, 'selected_car': selected_car})

# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect('login')

# Профиль пользователя
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    rentals = Rental.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'form': form,
        'profile': profile,
        'rentals': rentals,
        'orders': orders,
    })

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('profile')
    else:
        form = RegistrationForm()

    return render(request, 'login_register.html', {'form': form})

# Вход пользователя
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('profile')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()

    return render(request, 'login_register.html', {'form': form})

# Приветственная страница
class WelcomeView(TemplateView):
    template_name = 'welcome.html'

# Редактирование профиля
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

# Добавление аксессуара
@user_passes_test(is_seller_or_staff)
def add_accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аксессуар успешно добавлен!')
            return redirect('accessory_list')
    else:
        form = AccessoryForm()
    return render(request, 'accessories/add_accessory.html', {'form': form})

# Просмотр корзины
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.accessory.price * item.quantity for item in cart_items)
    return render(request, 'accessories/cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Добавление в корзину
@login_required
def add_to_cart(request, accessory_id):
    accessory = get_object_or_404(Accessory, id=accessory_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, accessory=accessory)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    
    messages.success(request, f"{accessory.name} добавлен в корзину!")
    return redirect('accessory_list')

# Страница платежа
@login_required
def payment_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.accessory.price * item.quantity for item in cart_items)
    return render(request, 'payment/payment_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

# Завершение платежа
# Завершение платежа
@login_required
def complete_payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.accessory.price * item.quantity for item in cart_items)

    # Обработка платежа
    payment_success = process_payment_method(total_price)

    if payment_success:
        for item in cart_items:
            # Создание заказа
            Order.objects.create(
                user=request.user,
                accessory=item.accessory,
                quantity=item.quantity,
                total_price=item.accessory.price * item.quantity,
            )

            # Уменьшение stock аксессуара
            if item.accessory.stock >= item.quantity:
                item.accessory.stock -= item.quantity
                item.accessory.save()
            else:
                # Если на складе недостаточно товара, выводим ошибку
                messages.error(request, f"Недостаточно товара '{item.accessory.name}' на складе.")
                return redirect('view_cart')

        # Очистка корзины
        cart_items.delete()

        return render(request, 'payment/payment_success.html')
    else:
        return render(request, 'payment/payment_failed.html')


def process_payment_method(amount):
    # Имитация обработки платежа
    return amount > 0

# Продажа автомобиля
@login_required
def sell_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            Order.objects.create(user=request.user, car=car, total_price=car.price)
            messages.success(request, 'Автомобиль успешно куплен!')
            return redirect('car_list')
    else:
        form = PaymentForm()

    return render(request, 'sell_car.html', {'car': car, 'form': form})

# Добавление карты
@login_required
def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Карта успешно добавлена!')
            return redirect('profile')
    else:
        form = CardForm()

    return render(request, 'add_card.html', {'form': form})

# Доступные автомобили
def available_cars(request):
    cars = Car.objects.filter(is_for_sale=True)
    return render(request, 'available_cars.html', {'cars': cars})

# Добавление автомобиля на продажу
@user_passes_test(is_seller_or_staff)
def add_car_for_sale(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль успешно добавлен на продажу!')
            return redirect('available_cars')
    else:
        form = CarForm()
    return render(request, 'add_car_for_sale.html', {'form': form})

# Покупка автомобиля
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Order
from .forms import PaymentForm

@login_required
def buy_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_success = process_payment_method(car.price)

            if payment_success:
                # Создание заказа
                Order.objects.create(user=request.user, car=car, total_price=car.price)

                # Обновляем статус автомобиля, чтобы он больше не был доступен для продажи
                car.is_for_sale = False  # Убираем автомобиль из продажи
                car.save()  # Сохраняем изменения в базе данных

                messages.success(request, 'Оплата прошла успешно! Автомобиль куплен.')
                return redirect('payment_success')  # Перенаправление на страницу успешной покупки
            else:
                messages.error(request, 'Ошибка при обработке платежа. Проверьте данные карты.')
    else:
        form = PaymentForm()

    return render(request, 'buy_car.html', {'car': car, 'form': form})



from django.shortcuts import render

def payment_success(request):
    return render(request, 'payment/payment_success.html')
