from datetime import timedelta

from django.test import SimpleTestCase
from django.utils import timezone

from .models import Assignment, AssignmentSubmission


class AssignmentModelTests(SimpleTestCase):
    def test_unsaved_assignment_without_due_date_is_not_open(self):
        assignment = Assignment()

        self.assertFalse(assignment.is_open)

    def test_assignment_is_open_until_due_date(self):
        assignment = Assignment(due_date=timezone.now() + timedelta(days=1))

        self.assertTrue(assignment.is_open)

    def test_assignment_is_not_open_before_open_date(self):
        assignment = Assignment(
            opens_at=timezone.now() + timedelta(hours=1),
            due_date=timezone.now() + timedelta(days=1),
        )

        self.assertFalse(assignment.is_open)

    def test_submission_has_grade_when_marks_are_awarded(self):
        submission = AssignmentSubmission(grade_awarded=8)

        self.assertTrue(submission.has_grade)

    def test_submission_has_grade_when_feedback_is_added(self):
        submission = AssignmentSubmission(evaluator_note='Good work, but tests were missing.')

        self.assertTrue(submission.has_grade)
