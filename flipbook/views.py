from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

def index(request: HttpRequest) -> HttpResponse:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX request for additional pages
        start_page = int(request.GET.get('start', 1))
        end_page = int(request.GET.get('end', start_page + 3))
        pages_content = []
        for page_num in range(start_page, end_page + 1):
            try:
                page_content = render_to_string(f'pages/page_{page_num}.html')
                pages_content.append({
                    'number': page_num,
                    'content': page_content
                })
            except:
                # Stop if page template doesn't exist
                break
        return JsonResponse({'pages': pages_content})
    else:
        # Initial page load
        initial_pages = 4  # Load first 4 pages initially
        pages_content = []
        for page_num in range(1, initial_pages + 1):
            page_content = render_to_string(f'pages/page_{page_num}.html')
            pages_content.append({
                'number': page_num,
                'content': page_content
            })
        context_data = {
            'initial_pages': pages_content
        }
        return render(request, "index.html", context_data)
