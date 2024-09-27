from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Car
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


def list_cars(request):
    cars = Car.objects.all()
    categories = {}
    for car in cars:
        if car.category not in categories:
            categories[car.category] = []
        categories[car.category].append(car)
    return render(request, 'list_cars.html', {'cars':cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment.objects.create(car=car, author=request.user, content=content)
        comment.save()
        return redirect('car_detail', car_id=car.id)  # Перенаправление на ту же страницу
    comments = car.comments.all()  # Получаем комментарии
    return render(request, 'car_detail.html', {'car': car, 'comments': comments})


@login_required  # Защита страницы для добавления автомобиля
def add_car(request):
    if request.method == 'POST':
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        description = request.POST['description']

        # Создание нового автомобиля
        Car.objects.create(
            make=make,
            model=model,
            year=year,
            description=description,
            owner=request.user
        )
        return redirect('list_cars')  # Перенаправление на список автомобилей

    return render(request, 'add_car.html')  # Показ формы добавления

def category_view(request):
    categories = Car.objects.values_list('category', flat=True).distinct() #получение уникальных категорий
    category_cars = {category: Car.objects.filter(category=category) for category in categories}
    return render(request, 'categories.html', {'category_cars':category_cars})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('list_cars')  # Перенаправляем на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)


@login_required
def add_comment(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(car=car, author=request.user, content=content)
        return redirect('car_detail', car_id=car_id)

def categorize(request):
    categories = Car.objects.values_list('category', flat=True).distinct()
    return render(request, 'categories.html', {'categories': categories})