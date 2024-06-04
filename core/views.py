from django.shortcuts import render, redirect

# Create your views here.
def view_404(request, exception=None):
    return redirect("/admin")