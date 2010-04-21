from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from models import *


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items, context_instance=RequestContext(request))
            else:
                return items
        return rendered_func

@login_required
@rendered_with('rolf/index.html')
def index(request):
    return dict(recent_pushes=Push.objects.filter(user=request.user),
                categories=Category.objects.all())

@login_required
def add_category(request):
    if request.method == "POST":
        c = Category.objects.create(name=request.POST.get('name','unknown'))
    return HttpResponseRedirect("/")

@login_required
def add_application(request,object_id):
    category = get_object_or_404(Category,id=object_id)
    if request.method == "POST":
        a = Application.objects.create(category=category,
                                       name=request.POST.get('name','unknown'))
    return HttpResponseRedirect(category.get_absolute_url())
