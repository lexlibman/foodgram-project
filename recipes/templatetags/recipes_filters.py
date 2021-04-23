from django import template
from django.utils.encoding import iri_to_uri

register = template.Library()


@register.filter
def paginator_manager(request, number):
    new_request = request.GET.copy()
    new_request['page'] = number
    return new_request.urlencode()


@register.filter
def decode_path(path):
    return iri_to_uri(path)


@register.filter
def declenize(number, args):
    args = [arg.strip() for arg in args.split(',')]
    last_digit = int(number) % 10
    if 10 < int(number) < 15:
        return f'{number} {args[2]}'
    if last_digit == 1:
        return f'{number} {args[0]}'
    if 1 < last_digit < 5:
        return f'{number} {args[1]}'
    return f'{number} {args[2]}'
