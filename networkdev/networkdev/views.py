from django.shortcuts import redirect


def redirect_editordb(request):
    return redirect('autheditor_url', permanent=True)
