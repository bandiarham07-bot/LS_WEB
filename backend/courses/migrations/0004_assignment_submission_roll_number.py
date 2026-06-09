# Generated for assignment submission roll numbers.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_assignment_submission_grading'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='roll_number',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
