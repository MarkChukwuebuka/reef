from django.shortcuts import render
from .utils import * 

# Create your views here.
def home(request):
    html_table = cache.get('html_table')
    if html_table == None:
        html_table = formulate_table()
    context = {
        'html_table' : html_table
    }
    return render(request, 'index.html', context)