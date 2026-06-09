import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


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


class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.OneToOneField(
        ContentPage, on_delete=models.CASCADE, related_name='assignment'
    )
    details = models.TextField(
        blank=True,
        help_text='Structured assignment details. Existing page blocks can still hold links, videos, or extra notes.',
    )
    deliverables = models.TextField()
    due_date = models.DateTimeField()
    opens_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Optional. If set, students can submit only after this time.',
    )
    weightage = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['due_date']

    @property
    def is_open(self):
        if not self.due_date:
            return False

        now = timezone.now()
        if self.opens_at and now < self.opens_at:
            return False
        return now <= self.due_date

    def __str__(self):
        return self.page.title


class AssignmentSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='submissions'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assignment_submissions'
    )
    roll_number = models.CharField(max_length=50)
    github_repo_url = models.URLField()
    github_repo_name = models.CharField(max_length=255)
    grade_awarded = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Marks awarded to the student. Leave blank until evaluated.',
    )
    grade_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Maximum marks for this assignment.',
    )
    evaluator_note = models.TextField(
        blank=True,
        help_text='Feedback explaining the grade, including why marks were cut.',
    )
    graded_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['assignment', 'user']
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['assignment', 'user'], name='courses_ass_assignm_9290bc_idx'),
            models.Index(fields=['user', '-submitted_at'], name='courses_ass_user_id_184dfb_idx'),
        ]

    @property
    def has_grade(self):
        return self.grade_awarded is not None or bool(self.evaluator_note)

    def __str__(self):
        return f'{self.user.email} - {self.assignment}: {self.github_repo_name}'


class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    last_page = models.ForeignKey(
        ContentPage, null=True, blank=True, on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} → {self.last_page}'
