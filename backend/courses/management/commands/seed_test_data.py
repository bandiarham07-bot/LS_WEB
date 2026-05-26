"""
Management command to seed test content for all three block types.
Run once after migrations:  python manage.py seed_test_data
"""
from django.core.management.base import BaseCommand
from courses.models import CourseStatus, ContentPage, ContentBlock


PAGES = [
    # ── HOME ────────────────────────────────────────────────────────────────
    {
        "section": "home",
        "title": "Welcome to the Course",
        "order": 1,
        "blocks": [
            {
                "type": "text",
                "title": "About this course",
                "order": 1,
                "body": (
                    "Welcome to the Student Learning Hub!\n\n"
                    "This course is structured across four sections:\n\n"
                    "• Resources – reading material, links, and videos for each week\n"
                    "• Setups – step-by-step environment and tooling guides\n"
                    "• Assignments – what you need to submit and when\n\n"
                    "Use the Continue button on the home screen to pick up exactly "
                    "where you left off. Your progress is saved automatically every "
                    "time you navigate to a new page."
                ),
            },
        ],
    },

    # ── RESOURCES ────────────────────────────────────────────────────────────
    {
        "section": "resources",
        "title": "Week 1 – Introduction to the Web",
        "order": 1,
        "blocks": [
            {
                "type": "text",
                "title": "What you will learn this week",
                "order": 1,
                "body": (
                    "This week covers the foundations of how the web works.\n\n"
                    "Topics:\n"
                    "1. How browsers request and render pages (HTTP basics)\n"
                    "2. The role of HTML, CSS, and JavaScript\n"
                    "3. What a web server does\n"
                    "4. The difference between frontend and backend\n\n"
                    "By the end of the week you should be able to explain, in plain "
                    "English, what happens between typing a URL and seeing a webpage."
                ),
            },
            {
                "type": "youtube",
                "title": "How the Internet Works (in 5 minutes)",
                "order": 2,
                "body": "A clear, non-technical overview — good starting point before the reading.",
                "url": "https://www.youtube.com/watch?v=7_LPdttKXPc",
            },
            {
                "type": "document",
                "title": "MDN – How the Web Works",
                "order": 3,
                "body": "Official Mozilla developer documentation. Read sections 1–3.",
                "url": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works",
            },
        ],
    },
    {
        "section": "resources",
        "title": "Week 2 – HTML & CSS Fundamentals",
        "order": 2,
        "blocks": [
            {
                "type": "text",
                "title": "Reading guide",
                "order": 1,
                "body": (
                    "This week focuses on the building blocks of every webpage.\n\n"
                    "HTML gives a page its structure — headings, paragraphs, lists, "
                    "links, images. CSS controls how that structure looks — colours, "
                    "fonts, spacing, layout.\n\n"
                    "Key concepts:\n"
                    "• The DOM (Document Object Model)\n"
                    "• Box model (margin, border, padding, content)\n"
                    "• Flexbox for one-dimensional layouts\n"
                    "• CSS Grid for two-dimensional layouts\n\n"
                    "Work through the video first, then tackle the linked exercise."
                ),
            },
            {
                "type": "youtube",
                "title": "HTML & CSS Full Course for Beginners",
                "order": 2,
                "body": "Watch the first 45 minutes (up to the Flexbox section).",
                "url": "https://www.youtube.com/watch?v=mU6anWqZJcc",
            },
            {
                "type": "document",
                "title": "CSS Tricks – Complete Guide to Flexbox",
                "order": 3,
                "body": "The best reference for Flexbox properties — bookmark this.",
                "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/",
            },
        ],
    },
    {
        "section": "resources",
        "title": "Week 3 – JavaScript Basics",
        "order": 3,
        "blocks": [
            {
                "type": "text",
                "title": "This week's focus",
                "order": 1,
                "body": (
                    "JavaScript makes pages interactive. This week you will cover:\n\n"
                    "• Variables (let, const) and data types\n"
                    "• Functions and arrow functions\n"
                    "• DOM manipulation (querySelector, addEventListener)\n"
                    "• Fetch API for making HTTP requests\n"
                    "• Promises and async/await\n\n"
                    "Tip: open your browser's DevTools console (F12) and run the "
                    "examples live as you watch. Typing the code yourself is far more "
                    "effective than reading it."
                ),
            },
            {
                "type": "youtube",
                "title": "JavaScript in 100 Seconds",
                "order": 2,
                "body": "Quick conceptual overview before diving into the full tutorial.",
                "url": "https://www.youtube.com/watch?v=DHjqpvDnNGE",
            },
        ],
    },

    # ── SETUPS ───────────────────────────────────────────────────────────────
    {
        "section": "setups",
        "title": "Installing VS Code",
        "order": 1,
        "blocks": [
            {
                "type": "text",
                "title": "Why VS Code?",
                "order": 1,
                "body": (
                    "VS Code (Visual Studio Code) is the editor we use throughout "
                    "this course. It is free, cross-platform, and has excellent "
                    "support for every language we touch.\n\n"
                    "Steps:\n"
                    "1. Go to https://code.visualstudio.com\n"
                    "2. Download the installer for your OS (Windows / macOS / Linux)\n"
                    "3. Run the installer with default settings\n"
                    "4. Open VS Code and press Ctrl+Shift+X (Cmd+Shift+X on Mac) "
                    "to open the Extensions panel\n"
                    "5. Install: Prettier, ESLint, Python, GitLens\n\n"
                    "If you already have VS Code, make sure it is version 1.85 or later "
                    "(Help → About to check)."
                ),
            },
            {
                "type": "document",
                "title": "VS Code setup guide (PDF)",
                "order": 2,
                "body": "Printable step-by-step guide with screenshots for all three operating systems.",
                "url": "https://code.visualstudio.com/docs/setup/setup-overview",
            },
        ],
    },
    {
        "section": "setups",
        "title": "Setting Up Node.js and npm",
        "order": 2,
        "blocks": [
            {
                "type": "text",
                "title": "Installation steps",
                "order": 1,
                "body": (
                    "Node.js lets you run JavaScript outside the browser. "
                    "npm (Node Package Manager) comes bundled with it and is how we "
                    "install project dependencies.\n\n"
                    "Recommended: install via nvm (Node Version Manager) so you can "
                    "switch Node versions easily.\n\n"
                    "macOS / Linux:\n"
                    "  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash\n"
                    "  nvm install 20\n"
                    "  nvm use 20\n\n"
                    "Windows:\n"
                    "  Download nvm-windows from the link below, install it, then:\n"
                    "  nvm install 20\n"
                    "  nvm use 20\n\n"
                    "Verify: open a terminal and run:\n"
                    "  node --version   # should print v20.x.x\n"
                    "  npm --version    # should print 10.x.x"
                ),
            },
            {
                "type": "youtube",
                "title": "Node.js installation walkthrough",
                "order": 2,
                "body": "Covers macOS and Windows. Skip to 3:20 for Windows-specific steps.",
                "url": "https://www.youtube.com/watch?v=ENrzD9HAZK4",
            },
            {
                "type": "document",
                "title": "nvm-windows releases (GitHub)",
                "order": 3,
                "body": "Download the latest nvm-setup.exe from this page.",
                "url": "https://github.com/coreybutler/nvm-windows/releases",
            },
        ],
    },
    {
        "section": "setups",
        "title": "Python & pip Setup",
        "order": 3,
        "blocks": [
            {
                "type": "text",
                "title": "Getting Python ready",
                "order": 1,
                "body": (
                    "The backend of this project uses Python 3.12+. "
                    "Check your version first:\n\n"
                    "  python3 --version\n\n"
                    "If it prints 3.12 or higher, you are set. Otherwise:\n\n"
                    "macOS:   brew install python@3.12\n"
                    "Ubuntu:  sudo apt install python3.12 python3.12-venv\n"
                    "Windows: download the installer from python.org\n\n"
                    "Always use a virtual environment per project:\n"
                    "  python3 -m venv venv\n"
                    "  source venv/bin/activate\n"
                    "  pip install -r requirements.txt\n\n"
                    "Never install project packages globally — "
                    "it causes version conflicts across projects."
                ),
            },
        ],
    },

    # ── ASSIGNMENTS ──────────────────────────────────────────────────────────
    {
        "section": "assignments",
        "title": "Assignment 1 – Personal Webpage",
        "order": 1,
        "blocks": [
            {
                "type": "text",
                "title": "Brief",
                "order": 1,
                "body": (
                    "Build a personal webpage using only HTML and CSS (no JavaScript).\n\n"
                    "Requirements:\n"
                    "• A header with your name and a short bio\n"
                    "• A section listing 3 things you want to learn this term\n"
                    "• At least one image (can be a placeholder)\n"
                    "• Responsive layout that works on both desktop and mobile\n"
                    "• Valid HTML — run your file through https://validator.w3.org\n\n"
                    "Submission:\n"
                    "Upload a single .zip containing your index.html and any assets "
                    "to the submission link below. File name: firstname_lastname_a1.zip\n\n"
                    "Due: end of Week 2 (Friday, 11:59 PM)"
                ),
            },
            {
                "type": "document",
                "title": "Submission portal",
                "order": 2,
                "body": "Click Open to go to the submission form. Log in with your student email.",
                "url": "https://forms.google.com",
            },
        ],
    },
    {
        "section": "assignments",
        "title": "Assignment 2 – JavaScript To-Do List",
        "order": 2,
        "blocks": [
            {
                "type": "text",
                "title": "Brief",
                "order": 1,
                "body": (
                    "Build a functional to-do list app using HTML, CSS, and JavaScript.\n\n"
                    "Required features:\n"
                    "• Add a task (text input + button or Enter key)\n"
                    "• Mark a task as complete (clicking toggles a strikethrough style)\n"
                    "• Delete a task\n"
                    "• Persist tasks in localStorage so they survive a page refresh\n\n"
                    "Optional stretch goal:\n"
                    "• Filter tasks by All / Active / Completed\n\n"
                    "Grading:\n"
                    "Functionality 60% · Code quality 25% · UI/UX 15%\n\n"
                    "Due: end of Week 4 (Friday, 11:59 PM)\n\n"
                    "Submission: same portal as Assignment 1 — select 'Assignment 2' "
                    "from the dropdown."
                ),
            },
            {
                "type": "youtube",
                "title": "localStorage in JavaScript – quick explainer",
                "order": 2,
                "body": "Covers getItem, setItem, and JSON serialisation — exactly what you need.",
                "url": "https://www.youtube.com/watch?v=AUOzvFzdIk4",
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds test content: CourseStatus + pages with text, YouTube, and document blocks'

    def handle(self, *args, **options):
        self.stdout.write('Seeding test data...\n')

        # ── 1. CourseStatus ───────────────────────────────────────────────────
        CourseStatus.objects.all().delete()
        CourseStatus.objects.create(
            current_week=3,
            current_topic='Week 3: JavaScript Basics',
        )
        self.stdout.write('  ✓ CourseStatus created (Week 3)')

        # ── 2. Clear existing pages ───────────────────────────────────────────
        ContentPage.objects.all().delete()
        self.stdout.write('  ✓ Existing pages cleared')

        # ── 3. Create pages + blocks ──────────────────────────────────────────
        created_pages = {}
        for page_data in PAGES:
            blocks = page_data.pop('blocks', [])
            page = ContentPage.objects.create(**page_data)
            created_pages[f"{page.section}-{page.order}"] = page

            for block_data in blocks:
                ContentBlock.objects.create(page=page, **block_data)

            block_count = len(blocks)
            self.stdout.write(
                f'  ✓ [{page.section:12s}] "{page.title}" — '
                f'{block_count} block{"s" if block_count != 1 else ""}'
            )
            # Restore blocks list for idempotency if re-run
            page_data['blocks'] = blocks

        # ── 4. Wire next_page sequence ────────────────────────────────────────
        # Resources: 1 → 2 → 3
        r1 = created_pages.get('resources-1')
        r2 = created_pages.get('resources-2')
        r3 = created_pages.get('resources-3')
        if r1 and r2: r1.next_page = r2; r1.save()
        if r2 and r3: r2.next_page = r3; r2.save()

        # Setups: 1 → 2 → 3
        s1 = created_pages.get('setups-1')
        s2 = created_pages.get('setups-2')
        s3 = created_pages.get('setups-3')
        if s1 and s2: s1.next_page = s2; s1.save()
        if s2 and s3: s2.next_page = s3; s2.save()

        # Assignments: 1 → 2
        a1 = created_pages.get('assignments-1')
        a2 = created_pages.get('assignments-2')
        if a1 and a2: a1.next_page = a2; a1.save()

        # Cross-section: Resources end → Setups start
        if r3 and s1: r3.next_page = s1; r3.save()
        # Cross-section: Setups end → Assignments start
        if s3 and a1: s3.next_page = a1; s3.save()

        self.stdout.write('\n  ✓ Page sequences wired\n')
        self.stdout.write(self.style.SUCCESS('Done. Test data seeded successfully.\n'))
        self.stdout.write(
            '\nContent summary:\n'
            '  Home        → 1 page  (1 text block)\n'
            '  Resources   → 3 pages (text + YouTube + document per page)\n'
            '  Setups      → 3 pages (text + YouTube + document per page)\n'
            '  Assignments → 2 pages (text + document / text + YouTube)\n'
            '\nSequence: Resources 1→2→3 → Setups 1→2→3 → Assignments 1→2\n'
        )
