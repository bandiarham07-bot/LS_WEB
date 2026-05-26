import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class CourseStatus(models.Model):
    current_week = models.IntegerField(default=1)
    current_topic = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Course status'

    def __str__(self):
        return f'Week {self.current_week}: {self.current_topic}'


class ContentPage(models.Model):
    SECTION_CHOICES = [
        ('home', 'Home'),
        ('resources', 'Resources'),
        ('setups', 'Setups'),
        ('assignments', 'Assignments'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    title = models.CharField(max_length=255)
    order = models.IntegerField()
    next_page = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='previous_pages',
    )

    class Meta:
        ordering = ['section', 'order']

    def __str__(self):
        return f'{self.get_section_display()} — {self.title}'


class ContentBlock(models.Model):
    BLOCK_TYPES = [
        ('text', 'Text'),
        ('document', 'Document'),
        ('youtube', 'YouTube'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(ContentPage, on_delete=models.CASCADE, related_name='blocks')
    type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    url = models.URLField(blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.page.title} — {self.type} #{self.order}'


class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    last_page = models.ForeignKey(
        ContentPage, null=True, blank=True, on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} → {self.last_page}'
