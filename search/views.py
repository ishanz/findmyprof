from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):
    return render(request, 'main.html')

# Currently: grabs query string from /search/?term=query, makes request to UVA People, renders search result locally
# r.text is the money: that's what we can parse to grab data
# and that data is what we should eventually return through HttpResponse
def search(request):
    if request.method == 'GET' and 'term' in request.GET:
        prof = request.GET['term']
        r = requests.post("http://www.virginia.edu/cgi-local/ldapweb/", data={'whitepages': prof})
        return HttpResponse(r.text)
    else:
        return HttpResponse("Improper request.")
