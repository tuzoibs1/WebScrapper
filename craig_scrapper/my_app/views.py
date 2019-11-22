import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models 

#url with quiry thats dynamically generated
BASE_CRAIGLIST_URL = 'https://minneapolis.craigslist.org/search/bbb?query=python%20tutor&sort=rel'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    #creating search object to hold searched querys
    models.Search.objects.create(search=search)
    
    # print(quote_plus(search))
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    print(final_url)
    data = response.text
    
    #parse data to bs4 object 
    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class': 'result-title'})
    print(post_titles[0].get('href'))
    
    #print(data)
    stuff_for_frontend ={
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)

    