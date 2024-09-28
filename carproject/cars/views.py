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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


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


class ListCarsView(View):
    def get(self, request):
        cars = Car.objects.all()
        categories = {}
        for car in cars:
            if car.category not in categories:
                categories[car.category] = []
            categories[car.category].append(car)
        return render(request, 'list_cars.html', {'cars': cars})


class CarDetailView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        comments = car.comments.all()
        return render(request, 'car_detail.html', {'car': car, 'comments': comments})

    def post(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        content = request.POST.get('content')
        comment = Comment.objects.create(car=car, author=request.user, content=content)
        comment.save()
        return redirect('car_detail', car_id=car.id)


class AddCarView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_car.html')

    def post(self, request):
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        description = request.POST['description']

        Car.objects.create(
            make=make,
            model=model,
            year=year,
            description=description,
            owner=request.user
        )
        return redirect('list_cars')


class CategoryView(View):
    def get(self, request):
        categories = Car.objects.values_list('category', flat=True).distinct()
        category_cars = {category: Car.objects.filter(category=category) for category in categories}
        return render(request, 'categories.html', {'category_cars': category_cars})


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('list_cars')
        return render(request, 'register.html', {'form': form})


class EditCarView(LoginRequiredMixin, View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id, owner=request.user)
        # Логика редактирования автомобиля


class DeleteCarView(LoginRequiredMixin, View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id, owner=request.user)
        # Логика удаления автомобиля


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        content = request.POST.get('content')
        Comment.objects.create(car=car, author=request.user, content=content)
        return redirect('car_detail', car_id=car_id)


class CategorizeView(View):
    def get(self, request):
        categories = Car.objects.values_list('category', flat=True).distinct()
        return render(request, 'categories.html', {'categories': categories})
