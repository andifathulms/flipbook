import os
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings


def get_total_pages():
    # Get the template directory path
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'pages')
    # Count files matching the pattern page_*.html
    pages = [f for f in os.listdir(template_dir) if f.startswith('page_') and f.endswith('.html')]
    return len(pages)


def load_pages(start_page, end_page):
    pages_content = []
    for page_num in range(start_page, end_page + 1):
        try:
            page_content = render_to_string(f'pages/page_{page_num}.html')
            pages_content.append({
                'number': page_num,
                'content': page_content
            })
        except:
            break
    return pages_content


def index(request: HttpRequest) -> HttpResponse:
    total_pages = get_total_pages()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request for additional pages
        start_page = int(request.GET.get('start', 1))
        end_page = int(request.GET.get('end', start_page + 3))

        # Load requested pages
        pages_content = load_pages(start_page, end_page)
        return JsonResponse({'pages': pages_content})
    else:
        # Initial page load
        initial_pages = 4  # Load first 4 pages initially
        pages_content = load_pages(1, initial_pages)

        context_data = {
            'initial_pages': pages_content,
            'total_pages': total_pages
        }
        return render(request, "index.html", context_data)