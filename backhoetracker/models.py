from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE = (
        ('admin', 'Admin'),
        ('operator', 'Operator'),
    )
    first_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=ROLE)
    password = models.CharField(max_length=255)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='backhoetracker_users',
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='backhoetracker_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='backhoetracker_users',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='backhoetracker_user',
    )


class Payment(models.Model):
    payment_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=255)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)


class Job(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()

class Task(models.Model):

    TASK_STATE_CHOICES = (
        ('crawling', 'Crawling'),
        ('working', 'Working'),
        ('completed', 'Completed'),
    )

    task_state = models.CharField(max_length=255, choices=TASK_STATE_CHOICES)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    odometer_reading = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
