from rest_framework import serializers
from .models import (
    Assignment,
    AssignmentSubmission,
    CourseStatus,
    ContentPage,
    ContentBlock,
)


class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStatus
        fields = ['current_week', 'current_topic', 'updated_at']


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ['id', 'type', 'title', 'body', 'url', 'order']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    has_grade = serializers.BooleanField(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id',
            'roll_number',
            'github_repo_url',
            'github_repo_name',
            'grade_awarded',
            'grade_total',
            'evaluator_note',
            'graded_at',
            'has_grade',
            'submitted_at',
            'updated_at',
        ]
        read_only_fields = fields


class AssignmentSerializer(serializers.ModelSerializer):
    is_open = serializers.BooleanField(read_only=True)
    submission = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = [
            'id',
            'submission_type',
            'details',
            'deliverables',
            'due_date',
            'opens_at',
            'weightage',
            'is_open',
            'submission',
        ]

    def get_submission(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        prefetched_submissions = getattr(obj, 'current_user_submissions', None)
        if prefetched_submissions is not None:
            submission = prefetched_submissions[0] if prefetched_submissions else None
        else:
            submission = obj.submissions.filter(user=request.user).first()
        if not submission:
            return None
        return AssignmentSubmissionSerializer(submission).data


class ContentPageSerializer(serializers.ModelSerializer):
    blocks = ContentBlockSerializer(many=True, read_only=True)
    next_page_id = serializers.UUIDField(
        source='next_page.id', read_only=True, allow_null=True
    )
    assignment = serializers.SerializerMethodField()

    def get_assignment(self, obj):
        assignment = getattr(obj, 'assignment', None)
        if not assignment:
            return None
        return AssignmentSerializer(assignment, context=self.context).data

    class Meta:
        model = ContentPage
        fields = [
            'id',
            'section',
            'title',
            'order',
            'next_page_id',
            'blocks',
            'assignment',
        ]
