from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Member

# Create your views here.
def testing(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('myfirst.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

