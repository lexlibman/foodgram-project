from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def get_full_name_or_username(user):
    return user.get_full_name() or user.username


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
