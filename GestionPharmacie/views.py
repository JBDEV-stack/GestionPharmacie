from django.shortcuts import render

def handler403(request, exception=None):
    return render(request, '403.html', status=403)
