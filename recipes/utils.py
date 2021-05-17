from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .models import Tag


def create_paginator(request, template, context, items_list):
    paginator = Paginator(items_list, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    if page_number and int(page_number) > paginator.num_pages:
        url = request.build_absolute_uri(
            '?'
        ) + "?page=" + str(paginator.num_pages)
        return redirect(url)
    context['page'] = paginator.get_page(page_number)
    return render(request, template, context)


def turn_on_tags():
    return (
        '?filter='
        f"{'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    )
