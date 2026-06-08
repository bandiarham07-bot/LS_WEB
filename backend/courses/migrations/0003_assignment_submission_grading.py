# Generated for assignment submission grading.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_assignment_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='evaluator_note',
            field=models.TextField(blank=True, help_text='Feedback explaining the grade, including why marks were cut.'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='grade_awarded',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Marks awarded to the student. Leave blank until evaluated.', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='grade_total',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Maximum marks for this assignment.', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='graded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name='assignmentsubmission',
            index=models.Index(fields=['assignment', 'user'], name='courses_ass_assignm_9290bc_idx'),
        ),
        migrations.AddIndex(
            model_name='assignmentsubmission',
            index=models.Index(fields=['user', '-submitted_at'], name='courses_ass_user_id_184dfb_idx'),
        ),
    ]
