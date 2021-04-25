from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'error/404.html', status=404)


def server_error(request):
    return render(request, 'error/500.html', status=500)
