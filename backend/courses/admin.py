from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CourseStatus, ContentPage, ContentBlock, UserProgress


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    ordering = ['email']


class ContentBlockInline(admin.StackedInline):
    """
    StackedInline puts every field on its own row so nothing gets hidden.
    Fields are grouped logically: order/type first, then the three content
    fields (title, body, url) each labelled clearly.
    """
    model = ContentBlock
    extra = 1
    fields = ['order', 'type', 'title', 'body', 'url']
    ordering = ['order']

    # Clearer help text so it's obvious which field to use per type
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['body'].help_text = 'Used by Text blocks — write your content here.'
        form.base_fields['url'].help_text  = (
            'Used by YouTube and Document blocks. '
            'For YouTube paste the full watch URL '
            '(e.g. https://www.youtube.com/watch?v=...). '
            'For documents paste a direct file or Google Drive link.'
        )
        form.base_fields['order'].help_text = (
            'Controls the display order within this page. '
            'Lower numbers appear first. Block 1 is the first thing students see.'
        )
        return form


@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    """
    • list_editable on 'order' lets you change page order directly from
      the list view without opening each page individually.
    • list_display_links must exclude 'order' when it is list_editable.
    • ordering + list_filter make it easy to find and reorder pages.
    """
    list_display         = ['section', 'order', 'title', 'next_page']
    list_display_links   = ['title']          # 'order' must NOT be a link when editable
    list_editable        = ['order']          # ← edit order numbers inline on list page
    list_filter          = ['section']
    ordering             = ['section', 'order']
    inlines              = [ContentBlockInline]

    # Show next_page choices filtered to same section for clarity
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'order' in form.base_fields:
            form.base_fields['order'].help_text = (
                'Page position within its section. '
                '1 = first page students land on in this section.'
            )
        return form


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    """
    Standalone view so you can also edit blocks directly if needed.
    """
    list_display  = ['page', 'order', 'type', 'title']
    list_filter   = ['type', 'page__section']
    ordering      = ['page__section', 'page__order', 'order']
    list_editable = ['order']
    list_display_links = ['title']


@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ['current_week', 'current_topic', 'updated_at']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display   = ['user', 'last_page', 'updated_at']
    readonly_fields = ['updated_at']
