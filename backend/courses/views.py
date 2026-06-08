from urllib.parse import urlparse

from django.utils import timezone
from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Assignment, AssignmentSubmission, CourseStatus, ContentPage, UserProgress
from .serializers import (
    AssignmentSubmissionSerializer,
    CourseStatusSerializer,
    ContentPageSerializer,
)

# Sections that are navigable as content pages (excludes 'home' which is
# its own tab and has no route in the frontend)
NAVIGABLE_SECTIONS = ['resources', 'setups', 'assignments']


def get_root_page():
    """
    Returns the navigable page (resources/setups/assignments) that no other
    page points to via next_page — i.e. the absolute start of the sequence.
    """
    qs = ContentPage.objects.filter(section__in=NAVIGABLE_SECTIONS)
    all_ids = qs.values_list('id', flat=True)
    if not all_ids:
        return None
    pointed_to = ContentPage.objects.exclude(
        next_page=None
    ).values_list('next_page_id', flat=True)
    root_ids = set(all_ids) - set(pointed_to)
    if root_ids:
        return qs.filter(id__in=root_ids).order_by('order').first()
    # Fallback: no links set yet — return first resources page
    return qs.order_by('order').first()


class HomeView(APIView):
    def get(self, request):
        course_status = CourseStatus.objects.first()
        progress, _ = UserProgress.objects.get_or_create(user=request.user)

        # Use saved progress if it's a navigable page, else fall back to root
        last_page = progress.last_page
        if last_page and last_page.section not in NAVIGABLE_SECTIONS:
            last_page = None
        last_page = last_page or get_root_page()

        return Response({
            'course_status': (
                CourseStatusSerializer(course_status).data if course_status else None
            ),
            'last_page': (
                ContentPageSerializer(last_page).data if last_page else None
            ),
        })


class UpdateProgressView(APIView):
    def patch(self, request):
        page_id = request.data.get('page_id')
        if not page_id:
            return Response(
                {'error': 'page_id is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            page = ContentPage.objects.get(id=page_id)
        except ContentPage.DoesNotExist:
            return Response(
                {'error': 'Page not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Only save progress for navigable sections
        if page.section not in NAVIGABLE_SECTIONS:
            return Response({'status': 'skipped'})

        progress, _ = UserProgress.objects.get_or_create(user=request.user)
        progress.last_page = page
        progress.save()

        return Response({'status': 'updated'})


class SectionPagesView(generics.ListAPIView):
    serializer_class = ContentPageSerializer

    def get_queryset(self):
        section = self.kwargs['section']
        user_submission_prefetch = Prefetch(
            'assignment__submissions',
            queryset=AssignmentSubmission.objects.filter(user=self.request.user),
            to_attr='current_user_submissions',
        )
        return (
            ContentPage.objects
            .filter(section=section)
            .select_related('assignment')
            .prefetch_related('blocks', user_submission_prefetch)
        )


class PageDetailView(generics.RetrieveAPIView):
    serializer_class = ContentPageSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_submission_prefetch = Prefetch(
            'assignment__submissions',
            queryset=AssignmentSubmission.objects.filter(user=self.request.user),
            to_attr='current_user_submissions',
        )
        return (
            ContentPage.objects
            .select_related('assignment')
            .prefetch_related('blocks', user_submission_prefetch)
            .all()
        )


def get_github_repo_name(repo_url):
    parsed = urlparse(repo_url.strip())
    if parsed.scheme not in ['http', 'https']:
        return None
    host = parsed.netloc.lower()
    if host.startswith('www.'):
        host = host[4:]
    parts = [part for part in parsed.path.strip('/').split('/') if part]

    if host != 'github.com' or len(parts) < 2:
        return None

    repo = parts[1]
    if repo.endswith('.git'):
        repo = repo[:-4]
    if not repo:
        return None
    return f'{parts[0]}/{repo}'


class AssignmentSubmitView(APIView):
    def post(self, request, assignment_id):
        roll_number = request.data.get('roll_number', '').strip()
        if not roll_number:
            return Response(
                {'roll_number': 'Roll number is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        repo_url = request.data.get('github_repo_url', '').strip()
        if not repo_url:
            return Response(
                {'github_repo_url': 'GitHub repository URL is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        repo_name = get_github_repo_name(repo_url)
        if not repo_name:
            return Response(
                {'github_repo_url': 'Enter a valid GitHub repository URL like https://github.com/user/repo.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return Response(
                {'error': 'Assignment not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        now = timezone.now()
        if assignment.opens_at and now < assignment.opens_at:
            return Response(
                {'error': 'This assignment is not open for submissions yet.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if now > assignment.due_date:
            return Response(
                {'error': 'The due date has passed. Submissions are closed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission, _ = AssignmentSubmission.objects.update_or_create(
            assignment=assignment,
            user=request.user,
            defaults={
                'roll_number': roll_number,
                'github_repo_url': repo_url,
                'github_repo_name': repo_name,
            },
        )

        return Response(AssignmentSubmissionSerializer(submission).data)
