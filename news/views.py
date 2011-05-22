# Create your views here.
from django.http import HttpResponse

def index(request):
	    return HttpResponse("Hello, world. You're at the poll index.")

def list(request):
	latest_news_list = Poll.objects.all().order_by('-pub_date')
