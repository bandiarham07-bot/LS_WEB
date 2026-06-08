# Generated for assignment metadata and GitHub submissions.

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('details', models.TextField(blank=True, help_text='Structured assignment details. Existing page blocks can still hold links, videos, or extra notes.')),
                ('deliverables', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('opens_at', models.DateTimeField(blank=True, help_text='Optional. If set, students can submit only after this time.', null=True)),
                ('weightage', models.CharField(blank=True, max_length=100)),
                ('page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='courses.contentpage')),
            ],
            options={
                'ordering': ['due_date'],
            },
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('github_repo_url', models.URLField()),
                ('github_repo_name', models.CharField(max_length=255)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='courses.assignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_submissions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-submitted_at'],
                'unique_together': {('assignment', 'user')},
            },
        ),
    ]
