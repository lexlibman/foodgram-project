from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Tag


def create_paginator(items_list, number_of_items, request):
    paginator = Paginator(items_list, number_of_items)
    page_number = request.GET.get('page')
    return paginator, page_number


def paginator_manager(request, template, content, context):
    paginator, page_number = create_paginator(
        content,
        settings.PAGINATION_PAGE_SIZE,
        request
    )
    if page_number and int(page_number) > paginator.num_pages + 1:
        context['page'] = paginator.get_page(paginator.num_pages + 1)
    else:
        context['page'] = paginator.get_page(page_number)
    return render(request, template, context)


def turn_on_tags():
    return (
        '?filter='
        f"{'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    )
