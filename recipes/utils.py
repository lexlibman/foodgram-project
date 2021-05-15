from django.core.paginator import Paginator

from .models import Tag


def create_paginator(items_list, number_of_items, request):
    paginator = Paginator(items_list, number_of_items)
    page_number = request.GET.get('page')
    return paginator, page_number


def turn_on_tags():
    return (
        '?filter='
        f"{'&filter='.join(Tag.objects.values_list('title', flat=True))}"
    )
