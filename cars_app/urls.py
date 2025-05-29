from django.urls import path
from .views import (
    WelcomeView,
    register,
    user_login,
    user_logout,
    profile_view,
    edit_profile,
    add_car,
    edit_car,
    delete_car,
    car_list,
    car_detail,
    rent_car,
    available_cars,
    add_car_for_sale,
    buy_car,
    sell_car,
    add_accessory,
    accessory_list,
    add_to_cart,
    view_cart,
    payment_page,
    complete_payment,
    payment_success,
    add_card,
    index,
    toggle_role,
)
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница и аутентификация
    path('', WelcomeView.as_view(), name='welcome'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('index/', index),

    # Профиль пользователя
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),

    # Управление автомобилями
    path('cars/', car_list, name='car_list'),
    path('cars/<int:car_id>/', car_detail, name='car_detail'),
    path('add_car/', add_car, name='add_car'),
    path('edit_car/<int:car_id>/', edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', delete_car, name='delete_car'),
    path('rent/<int:car_id>/', rent_car, name='rent_car'),
    path('sell_car/<int:car_id>/', sell_car, name='sell_car'),
    path('buy_car/<int:car_id>/', buy_car, name='buy_car'),
    path('available_cars/', available_cars, name='available_cars'),
    path('add_car_for_sale/', add_car_for_sale, name='add_car_for_sale'),

    # Управление аксессуарами
    path('accessories/', accessory_list, name='accessory_list'),
    path('add_accessory/', add_accessory, name='add_accessory'),
    path('add_to_cart/<int:accessory_id>/', add_to_cart, name='add_to_cart'),
    
    # Корзина
    path('cart/', view_cart, name='view_cart'),

    # Оплата
    path('payment/', payment_page, name='payment_page'),
    path('payment/complete/', complete_payment, name='complete_payment'),
    path('payment_success/', TemplateView.as_view(template_name='payment_success.html'), name='payment_success'),

    # Добавление карты
    path('add_card/', add_card, name='add_card'),

    path('toggle-role/', toggle_role, name='toggle_role'),
]

# Статические файлы в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
