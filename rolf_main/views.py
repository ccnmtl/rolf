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

@login_required
def add_deployment(request,object_id):
    application = get_object_or_404(Application,id=object_id)
    if request.method == "POST":
        a = Deployment.objects.create(application=application,
                                       name=request.POST.get('name','unknown'))
    return HttpResponseRedirect(application.get_absolute_url())

@login_required
def add_setting(request,object_id):
    deployment = get_object_or_404(Deployment,id=object_id)
    if request.method == "POST":
        s = Setting.objects.create(deployment=deployment,
                                   name=request.POST.get('name','unknown'),
                                   value=request.POST.get('value',''))
    return HttpResponseRedirect(deployment.get_absolute_url())

@login_required
def edit_settings(request,object_id):
    deployment = get_object_or_404(Deployment,id=object_id)
    if request.method == "POST":
        for k in request.POST.keys():
            if k.startswith('setting_name_'):
                setting_id = int(k[len('setting_name_'):])
                setting = get_object_or_404(Setting,id=setting_id)
                if request.POST[k] == "":
                    setting.delete
                else:
                    setting.name = request.POST[k]
                    setting.value = request.POST.get("setting_value_%d" % setting_id,"")
                    setting.save()
    return HttpResponseRedirect(deployment.get_absolute_url())

@login_required
def add_stage(request,object_id):
    deployment = get_object_or_404(Deployment,id=object_id)
    if request.method == "POST":
        recipe = None
        code = request.POST.get('code','').replace('\r\n','\n')
        recipe_id = request.POST.get('recipe_id','')
        if recipe_id:
            recipe = get_object_or_404(Recipe,id=recipe_id)
        else:
            recipe = Recipe.objects.create(name="",description="",
                                           language=request.POST.get('language','python'),
                                           code=code)
        stage = Stage.objects.create(deployment=deployment,recipe=recipe,
                                     name=request.POST.get('name','unknown stage'))
        
    return HttpResponseRedirect(deployment.get_absolute_url())

@login_required
def clone_deployment(request,object_id):
    deployment = get_object_or_404(Deployment,id=object_id)
    if request.method == "POST":
        application = get_object_or_404(Application,id=request.POST['application_id'])
        new_deployment = Deployment.objects.create(name=request.POST['name'],application=application)
        # clone settings
        for setting in deployment.setting_set.all():
            s = Setting.objects.create(deployment=new_deployment,name=setting.name,
                                       value=setting.value)
        # clone stages
        for stage in deployment.stage_set.all():
            recipe = stage.recipe
            r = recipe
            if recipe.name == "":
                # not a cookbook recipe, so we clone it
                r = Recipe.objects.create(name="",language=recipe.language,code=recipe.code)
            s = Stage.objects.create(deployment=new_deployment,name=stage.name,recipe=r)
        return HttpResponseRedirect(new_deployment.get_absolute_url())
    return HttpResponseRedirect(deployment.get_absolute_url())

@login_required
def push(request,object_id):
    deployment = get_object_or_404(Deployment,id=object_id)
    if request.method == "POST":
        push = deployment.new_push(user=request.user,comment=request.POST.get('comment',''))
        if request.POST.get('step',''):
            return HttpResponseRedirect(push.get_absolute_url() + "?step=1")
        else:
            return HttpResponseRedirect(push.get_absolute_url())
    else:
        return HttpResponse("POST requests, only, please")
