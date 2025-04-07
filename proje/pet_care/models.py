from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Pet(models.Model):
    SPECIES_CHOICES = [
        ('Kedi', 'Kedi'),
        ('Köpek', 'Köpek'),
    ]
    
    CAT_BREEDS = [
        ('Tekir', 'Tekir'),
        ('Sarman', 'Sarman'),
        ('Van Kedisi', 'Van Kedisi'),
        ('British Shorthair', 'British Shorthair'),
        ('Scottish Fold', 'Scottish Fold'),
        ('Persian', 'Persian'),
        ('Siamese', 'Siamese'),
        ('Maine Coon', 'Maine Coon'),
        ('Russian Blue', 'Russian Blue'),
        ('Bengal', 'Bengal'),
    ]
    
    DOG_BREEDS = [
        ('Golden Retriever', 'Golden Retriever'),
        ('Labrador Retriever', 'Labrador Retriever'),
        ('German Shepherd', 'German Shepherd'),
        ('French Bulldog', 'French Bulldog'),
        ('Bulldog', 'Bulldog'),
        ('Poodle', 'Poodle'),
        ('Beagle', 'Beagle'),
        ('Rottweiler', 'Rottweiler'),
        ('Doberman', 'Doberman'),
        ('Husky', 'Husky'),
        ('Pitbull', 'Pitbull'),
        ('Chihuahua', 'Chihuahua'),
        ('Corgi', 'Corgi'),
        ('Shih Tzu', 'Shih Tzu'),
        ('Boxer', 'Boxer'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    birth_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.species})"

class CareTask(models.Model):
    TASK_TYPES = [
        ('feeding', 'Besleme'),
        ('grooming', 'Tüy Bakımı'),
        ('vaccination', 'Aşılama'),
        ('medication', 'İlaç'),
        ('checkup', 'Kontrol'),
        ('other', 'Diğer'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    description = models.TextField()
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_task_type_display()} - {self.pet.name}"

class Expense(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} - {self.amount} TL"

class Reminder(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    reminder_date = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.pet.name}"
