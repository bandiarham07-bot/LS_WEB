from rest_framework import serializers
from .models import CourseStatus, ContentPage, ContentBlock


class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStatus
        fields = ['current_week', 'current_topic', 'updated_at']


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ['id', 'type', 'title', 'body', 'url', 'order']


class ContentPageSerializer(serializers.ModelSerializer):
    blocks = ContentBlockSerializer(many=True, read_only=True)
    next_page_id = serializers.UUIDField(
        source='next_page.id', read_only=True, allow_null=True
    )

    class Meta:
        model = ContentPage
        fields = ['id', 'section', 'title', 'order', 'next_page_id', 'blocks']
