from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Pet, CareTask, Expense, Reminder
from .serializers import PetSerializer, CareTaskSerializer, ExpenseSerializer, ReminderSerializer
import json

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'pet_care/register.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        pets = Pet.objects.filter(owner=request.user)
        pending_tasks = CareTask.objects.filter(
            pet__owner=request.user,
            is_completed=False
        )
        
        # Bu ayki harcamaları hesapla
        start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_expenses = Expense.objects.filter(
            pet__owner=request.user,
            date__gte=start_of_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Yaklaşan hatırlatıcıları al
        upcoming_reminders = Reminder.objects.filter(
            pet__owner=request.user,
            reminder_date__gte=timezone.now(),
            reminder_date__lte=timezone.now() + timedelta(days=7)
        )
        
        context = {
            'pets': pets,
            'pending_tasks': pending_tasks,
            'monthly_expenses': monthly_expenses,
            'upcoming_reminders': upcoming_reminders,
        }
    else:
        context = {}
    
    return render(request, 'pet_care/home.html', context)

@login_required
def pet_list(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/pets/list.html', {'pets': pets})

@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    care_tasks = CareTask.objects.filter(pet=pet, is_completed=False)
    expenses = Expense.objects.filter(pet=pet).order_by('-date')[:5]
    reminders = Reminder.objects.filter(pet=pet, reminder_date__gte=timezone.now()).order_by('reminder_date')[:5]
    
    context = {
        'pet': pet,
        'care_tasks': care_tasks,
        'expenses': expenses,
        'reminders': reminders,
    }
    return render(request, 'pet_care/pets/detail.html', context)

@login_required
def pet_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        birth_date = request.POST.get('birth_date')
        
        if name and species and breed and birth_date:
            Pet.objects.create(
                owner=request.user,
                name=name,
                species=species,
                breed=breed,
                birth_date=birth_date
            )
            messages.success(request, 'Evcil hayvan başarıyla eklendi!')
            return redirect('pet-list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    return render(request, 'pet_care/pets/form.html', {
        'species_choices': Pet.SPECIES_CHOICES,
        'cat_breeds': json.dumps(Pet.CAT_BREEDS),
        'dog_breeds': json.dumps(Pet.DOG_BREEDS)
    })

@login_required
def pet_edit(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        birth_date = request.POST.get('birth_date')
        
        if name and species and breed and birth_date:
            pet.name = name
            pet.species = species
            pet.breed = breed
            pet.birth_date = birth_date
            pet.save()
            messages.success(request, 'Evcil hayvan güncellendi!')
            return redirect('pet-detail', pk=pet.pk)
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    return render(request, 'pet_care/pets/form.html', {
        'pet': pet,
        'species_choices': Pet.SPECIES_CHOICES,
        'cat_breeds': json.dumps(Pet.CAT_BREEDS),
        'dog_breeds': json.dumps(Pet.DOG_BREEDS)
    })

@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Evcil hayvan kaydı silindi.')
        return redirect('pet-list')
    
    return render(request, 'pet_care/pets/delete.html', {'pet': pet})

@login_required
def task_list(request):
    tasks = CareTask.objects.filter(pet__owner=request.user)
    return render(request, 'pet_care/tasks/list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        task_type = request.POST.get('task_type')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        if pet_id and task_type and description and due_date:
            pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
            CareTask.objects.create(
                pet=pet,
                task_type=task_type,
                description=description,
                due_date=due_date
            )
            messages.success(request, 'Bakım görevi başarıyla eklendi!')
            return redirect('task-list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    pet_id = request.GET.get('pet')
    pet = None
    if pet_id:
        pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
    
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/tasks/form.html', {
        'pets': pets,
        'selected_pet': pet,
        'task_types': CareTask.TASK_TYPES
    })

@login_required
def task_edit(request, pk):
    task = get_object_or_404(CareTask, pk=pk, pet__owner=request.user)
    
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        task_type = request.POST.get('task_type')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        if pet_id and task_type and description and due_date:
            pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
            task.pet = pet
            task.task_type = task_type
            task.description = description
            task.due_date = due_date
            task.save()
            messages.success(request, 'Bakım görevi güncellendi!')
            return redirect('task-list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/tasks/form.html', {
        'task': task,
        'pets': pets,
        'selected_pet': task.pet,
        'task_types': CareTask.TASK_TYPES
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(CareTask, pk=pk, pet__owner=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Bakım görevi silindi.')
        return redirect('task-list')
    
    return render(request, 'pet_care/tasks/delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(CareTask, pk=pk, pet__owner=request.user)
    task.is_completed = True
    task.save()
    messages.success(request, 'Bakım görevi tamamlandı olarak işaretlendi.')
    return redirect('task-list')

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(pet__owner=request.user).order_by('-date')
    return render(request, 'pet_care/expenses/list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        category = request.POST.get('category')
        
        if pet_id and description and amount and date and category:
            pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
            Expense.objects.create(
                pet=pet,
                description=description,
                amount=amount,
                date=date,
                category=category
            )
            messages.success(request, 'Harcama başarıyla eklendi!')
            return redirect('expense-list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    pet_id = request.GET.get('pet')
    pet = None
    if pet_id:
        pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
    
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/expenses/form.html', {
        'pets': pets,
        'selected_pet': pet
    })

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, pet__owner=request.user)
    
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        category = request.POST.get('category')
        
        if pet_id and description and amount and date and category:
            pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
            expense.pet = pet
            expense.description = description
            expense.amount = amount
            expense.date = date
            expense.category = category
            expense.save()
            messages.success(request, 'Harcama güncellendi!')
            return redirect('expense-list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/expenses/form.html', {
        'expense': expense,
        'pets': pets,
        'selected_pet': expense.pet
    })

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, pet__owner=request.user)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Harcama silindi.')
        return redirect('expense-list')
    
    return render(request, 'pet_care/expenses/delete.html', {'expense': expense})

@login_required
def reminder_list(request):
    reminders = Reminder.objects.filter(pet__owner=request.user).order_by('reminder_date')
    return render(request, 'pet_care/reminders/list.html', {'reminders': reminders})

@login_required
def reminder_create(request):
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        title = request.POST.get('title')
        description = request.POST.get('description')
        reminder_date = request.POST.get('reminder_date')
        
        if pet_id and title and reminder_date:
            pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
            Reminder.objects.create(
                pet=pet,
                title=title,
                description=description,
                reminder_date=reminder_date
            )
            messages.success(request, 'Hatırlatıcı başarıyla eklendi!')
            return redirect('reminder-list')
        else:
            messages.error(request, 'Lütfen tüm gerekli alanları doldurun.')
    
    pet_id = request.GET.get('pet')
    pet = None
    if pet_id:
        pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
    
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/reminders/form.html', {
        'pets': pets,
        'selected_pet': pet
    })

@login_required
def reminder_edit(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, pet__owner=request.user)
    
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        title = request.POST.get('title')
        description = request.POST.get('description')
        reminder_date = request.POST.get('reminder_date')
        
        if pet_id and title and reminder_date:
            pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)
            reminder.pet = pet
            reminder.title = title
            reminder.description = description
            reminder.reminder_date = reminder_date
            reminder.save()
            messages.success(request, 'Hatırlatıcı güncellendi!')
            return redirect('reminder-list')
        else:
            messages.error(request, 'Lütfen tüm gerekli alanları doldurun.')
    
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pet_care/reminders/form.html', {
        'reminder': reminder,
        'pets': pets,
        'selected_pet': reminder.pet
    })

@login_required
def reminder_delete(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk, pet__owner=request.user)
    
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Hatırlatıcı silindi.')
        return redirect('reminder-list')
    
    return render(request, 'pet_care/reminders/delete.html', {'reminder': reminder})

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CareTaskViewSet(viewsets.ModelViewSet):
    serializer_class = CareTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CareTask.objects.filter(pet__owner=self.request.user)

    @action(detail=True, methods=['post'])
    def complete_task(self, request, pk=None):
        task = self.get_object()
        task.is_completed = True
        task.save()
        return Response({'status': 'task completed'})

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(pet__owner=self.request.user)

class ReminderViewSet(viewsets.ModelViewSet):
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reminder.objects.filter(pet__owner=self.request.user)

    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        reminder = self.get_object()
        return Response({'status': 'reminder sent'})


    @action(detail=True, methods=['post'])
    def send_reminder(self, request, pk=None):
        reminder = self.get_object()
        return Response({'status': 'reminder sent'})
