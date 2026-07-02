from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_assignment_submission_roll_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='submission_type',
            field=models.CharField(
                choices=[('github', 'GitHub repository'), ('url', 'Website URL')],
                default='github',
                max_length=10,
                help_text='Controls the submission form shown to students.',
            ),
        ),
    ]
