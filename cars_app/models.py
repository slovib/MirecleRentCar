from django.db import models
from django.contrib.auth.models import User

# Модель автомобиля
class Car(models.Model):
    make = models.CharField(max_length=100)  # Производитель
    model = models.CharField(max_length=100)  # Модель
    year = models.IntegerField()  # Год выпуска
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за аренду
    is_rented = models.BooleanField(default=False)  # Статус аренды
    is_for_sale = models.BooleanField(default=False)  # Статус продажи
    image = models.ImageField(upload_to='car_images/')  # Изображение автомобиля
    description = models.TextField()  # Описание автомобиля
    mileage = models.IntegerField(null=True, blank=True)  # Пробег (опционально)
    fuel_type = models.CharField(max_length=50, choices=[  # Тип топлива
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('electric', 'Электрический'),
        ('hybrid', 'Гибрид'),
    ], default='petrol')
    transmission = models.CharField(max_length=50, choices=[  # Коробка передач
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
    ], default='manual')

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# Модель отзыва


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')  # Связь с автомобилем
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Оценка от 1 до 5
    comment = models.TextField()  # Комментарий
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания отзыва

    def __str__(self):
        return f"Отзыв о {self.car} от {self.user.username}"


# Модель аренды
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, арендующий автомобиль
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Арендуемый автомобиль
    start_date = models.DateField()  # Дата начала аренды
    return_date = models.DateField()  # Дата возврата
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Общая цена аренды

    @property
    def rental_days(self):
        return (self.return_date - self.start_date).days  # Расчет количества дней аренды

    def __str__(self):
        return f"{self.car} арендован до {self.return_date}"

# Модель аксессуара
class Accessory(models.Model):
    name = models.CharField(max_length=100)  # Название аксессуара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена аксессуара
    image = models.ImageField(upload_to='accessory_images/')  # Изображение аксессуара
    description = models.TextField()  # Описание аксессуара
    stock = models.PositiveIntegerField(default=0)  # Количество доступных единиц

    def __str__(self):
        return self.name

# Модель корзины
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, добавивший аксессуар в корзину
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)  # Добавленный аксессуар
    quantity = models.PositiveIntegerField(default=1)  # Количество аксессуаров

# Модель заказа
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, сделавший заказ
    car = models.ForeignKey(Car, null=True, blank=True, on_delete=models.CASCADE)  # Заказанный автомобиль (если есть)
    accessory = models.ForeignKey(Accessory, null=True, blank=True, on_delete=models.CASCADE)  # Заказанный аксессуар (если есть)
    quantity = models.PositiveIntegerField(default=1)  # Количество
    order_date = models.DateTimeField(auto_now_add=True)  # Дата заказа
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая цена заказа
    

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username} на {self.car or self.accessory}"

# Модель профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Пользовательский аккаунт
    phone_number = models.CharField(max_length=15, blank=True)  # Номер телефона
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png')  # Аватар пользователя
    is_seller = models.BooleanField(default=False)  # Роль продавца

    def __str__(self):
        return self.user.username
