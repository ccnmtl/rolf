from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from models import Category, Push, Application, Deployment, Permission
from models import Setting, Flag, Recipe, Stage, FlagValue
from simplejson import dumps
from munin.helpers import muninview
from datetime import datetime, timedelta
from django_statsd.clients import statsd
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from itsdangerous import BadSignature, SignatureExpired
from django.conf import settings
from django.contrib.auth.models import User


class rendered_with(object):
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):
        def rendered_func(request, *args, **kwargs):
            items = func(request, *args, **kwargs)
            if type(items) == type({}):
                return render_to_response(self.template_name, items,
                             context_instance=RequestContext(request))
            else:
                return items
        return rendered_func


@login_required
@rendered_with('rolf/index.html')
def index(request):
    recent_pushes = Push.objects.filter(user=request.user)
    recent_deployments = list(set([p.deployment for p in recent_pushes]))
    recent_deployments.sort(key=lambda x: x.last_push_date())
    recent_deployments.reverse()
    return dict(recent_pushes=recent_pushes,
                recent_deployments=recent_deployments,
                categories=Category.objects.all())


@login_required
def add_category(request):
    if request.method == "POST":
        Category.objects.create(name=request.POST.get('name', 'unknown'))
    return HttpResponseRedirect("/")


@login_required
def add_application(request, object_id):
    category = get_object_or_404(Category, id=object_id)
    if request.method == "POST":
        Application.objects.create(category=category,
                                   name=request.POST.get('name', 'unknown'))
    return HttpResponseRedirect(category.get_absolute_url())


@login_required
def add_deployment(request, object_id):
    application = get_object_or_404(Application, id=object_id)
    if request.method == "POST":
        a = Deployment.objects.create(application=application,
                                      name=request.POST.get('name', 'unknown'))
        # make sure the user has edit access
        for group in request.user.groups.all():
            Permission.objects.create(deployment=a,
                                      group=group,
                                      capability="edit")
    return HttpResponseRedirect(application.get_absolute_url())


@login_required
def add_setting(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            Setting.objects.create(deployment=deployment,
                                   name=request.POST.get('name',
                                                         'unknown'),
                                   value=request.POST.get('value', ''))
    return HttpResponseRedirect("%s#tab-settings" %
                                deployment.get_absolute_url())


@login_required
def remove_permission(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            permission = get_object_or_404(Permission,
                             id=request.POST.get('permission_id', -1))
            permission.delete()
    return HttpResponseRedirect(deployment.get_absolute_url())


@login_required
def add_permission(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            form = deployment.add_permission_form(request_vars=request.POST)
            permission = form.save(commit=False)
            permission.deployment = deployment
            permission.save()
    return HttpResponseRedirect(deployment.get_absolute_url())


@login_required
def remove_flag(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            flag = get_object_or_404(Flag, id=request.POST.get('flag_id', -1))
            flag.delete()
    return HttpResponseRedirect(deployment.get_absolute_url())


@login_required
def add_flag(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            form = deployment.add_flag_form(request_vars=request.POST)
            flag = form.save(commit=False)
            flag.deployment = deployment
            flag.save()
    return HttpResponseRedirect(deployment.get_absolute_url())


@login_required
def edit_settings(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            for k in request.POST.keys():
                if k.startswith('setting_name_'):
                    setting_id = int(k[len('setting_name_'):])
                    setting = get_object_or_404(Setting, id=setting_id)
                    if request.POST[k] == "":
                        setting.delete
                    else:
                        setting.name = request.POST[k]
                        setting.value = request.POST.get("setting_value_%d" %
                                                         setting_id, "")
                        setting.save()
    return HttpResponseRedirect("%s#tab-settings" %
                                deployment.get_absolute_url())


@login_required
def add_stage(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            recipe = None
            code = request.POST.get('code', '').replace('\r\n', '\n')
            recipe_id = request.POST.get('recipe_id', '')
            if recipe_id:
                recipe = get_object_or_404(Recipe, id=recipe_id)
            else:
                recipe = Recipe.objects.create(name="", description="",
                                 language=request.POST.get('language',
                                                           'python'),
                                               code=code)
            Stage.objects.create(deployment=deployment, recipe=recipe,
                                 name=request.POST.get('name',
                                                       'unknown stage'))

    return HttpResponseRedirect("%s#tab-stages" %
                                deployment.get_absolute_url())


@login_required
def clone_deployment(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_edit(request.user):
            application = get_object_or_404(Application,
                                            id=request.POST['application_id'])
            new_deployment = Deployment.objects.create(
                name=request.POST['name'],
                application=application)
            # clone settings
            for setting in deployment.setting_set.all():
                Setting.objects.create(deployment=new_deployment,
                                       name=setting.name,
                                       value=setting.value)
            # clone stages
            for stage in deployment.stage_set.all():
                recipe = stage.recipe
                r = recipe
                if recipe.name == "":
                    # not a cookbook recipe, so we clone it
                    r = Recipe.objects.create(name="",
                                              language=recipe.language,
                                              code=recipe.code)
                Stage.objects.create(deployment=new_deployment,
                                     name=stage.name, recipe=r)
            # clone permissions
            for perm in deployment.permission_set.all():
                Permission.objects.create(deployment=new_deployment,
                                          group=perm.group,
                                          capability=perm.capability)

            # clone flags
            for flag in deployment.flag_set.all():
                Flag.objects.create(deployment=new_deployment,
                                    name=flag.name,
                                    varname=flag.varname,
                                    boolean=flag.boolean,
                                    default=flag.default,
                                    description=flag.description)

            return HttpResponseRedirect(new_deployment.get_absolute_url())
    return HttpResponseRedirect(deployment.get_absolute_url())


@login_required
def push(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_push(request.user):
            statsd.incr('event.push')
            push = deployment.new_push(user=request.user,
                                       comment=request.POST.get('comment', ''))
            for k in request.POST.keys():
                if k.startswith("flag_"):
                    flag_id = k[len("flag_"):]
                    flag = Flag.objects.get(id=flag_id)
                    value = request.POST[k]
                    FlagValue.objects.create(flag=flag, push=push,
                                             value=value)
            if request.POST.get('step', ''):
                return HttpResponseRedirect(push.get_absolute_url() +
                                            "?step=1")
            else:
                return HttpResponseRedirect(push.get_absolute_url())
    else:
        return HttpResponse("POST requests, only, please")


@login_required
def rollback(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if request.method == "POST":
        if deployment.can_push(request.user):
            statsd.incr('event.rollback')
            push_id = request.POST.get('push_id', '')
            push = deployment.new_push(user=request.user,
                                       comment=request.POST.get('comment', ''))
            for k in request.POST.keys():
                if k.startswith("flag_"):
                    flag_id = k[len("flag_"):]
                    flag = Flag.objects.get(id=flag_id)
                    value = request.POST[k]
                    FlagValue.objects.create(flag=flag, push=push,
                                             value=value)
            if request.POST.get('step', ''):
                return HttpResponseRedirect("/push/%d/?step=1;rollback=%s" %
                                            (push.id, push_id))
            else:
                return HttpResponseRedirect("/push/%d/?rollback=%s" %
                                            (push.id, push_id))
    else:
        return HttpResponse("requires POST")


@login_required
def stage(request, object_id):
    push = get_object_or_404(Push, id=object_id)
    if push.deployment.can_push(request.user):
        statsd.incr('event.run_stage')
        pushstage = push.run_stage(request.GET.get('stage_id', None),
                                   request.GET.get('rollback_id', None))
        logs = [dict(command=l.command, stdout=l.stdout,
                     stderr=l.stderr) for l in pushstage.log_set.all()]
        return HttpResponse(dumps(dict(status=pushstage.status,
                                       logs=logs,
                                       end_time=str(pushstage.end_time),
                                       stage_id=pushstage.stage.id)),
                            mimetype='application/json')
    else:
        return HttpResponse("permission denied")


@login_required
@rendered_with('rolf/cookbook.html')
def cookbook(request):
    return dict(all_recipes=Recipe.objects.all().exclude(name=""))


@login_required
def add_cookbook_recipe(request):
    code = request.POST.get('code', '').replace('\r\n', '\n')
    name = request.POST.get('name', '')
    language = request.POST.get('language', '')
    description = request.POST.get('description', '')
    Recipe.objects.create(name=name, description=description,
                          language=language, code=code)
    return HttpResponseRedirect("/cookbook/")


@login_required
def edit_recipe(request, object_id):
    recipe = get_object_or_404(Recipe, id=object_id)
    recipe.name = request.POST.get('name', '')
    recipe.description = request.POST.get('description', '')
    recipe.language = request.POST.get('language', '')
    code = request.POST.get('code', '').replace('\r\n', '\n')
    recipe.code = code
    recipe.save()
    return HttpResponseRedirect(recipe.get_absolute_url())


@login_required
def edit_stage(request, object_id):
    stage = get_object_or_404(Stage, id=object_id)
    stage.name = request.POST.get('name', '')
    code = request.POST.get('code', '').replace('\r\n', '\n')
    recipe_id = request.POST.get('recipe_id', '')
    if recipe_id != "":
        r = Recipe.objects.get(id=recipe_id)
        stage.recipe = r
    else:
        if stage.recipe.name != "":
            stage.recipe = Recipe.objects.create(
                language=request.POST.get('language', 'shell'), code="")
        else:
            stage.recipe.language = request.POST.get('language', 'shell')
            stage.recipe.code = code
            stage.recipe.save()
    stage.save()
    return HttpResponseRedirect(stage.get_absolute_url())


@login_required
def reorder_stages(request, object_id):
    deployment = get_object_or_404(Deployment, id=object_id)
    if deployment.can_edit(request.user):
        ids = [(int(k[len('stage_'):]), int(v)) for k, v in
               request.GET.items() if k.startswith('stage_')]
        ids.sort(key=lambda x: x[0])
        deployment.set_stage_order([x[1] for x in ids])
        deployment.save()
    return HttpResponse("ok")


@login_required
def generic_detail(request, object_id, model, template_name):
    return render_to_response(template_name,
                              dict(object=get_object_or_404(model,
                                                            id=object_id)),
                              context_instance=RequestContext(request))


@login_required
@rendered_with('rolf/get_api_key.html')
def get_api_key(request):
    s1 = URLSafeSerializer(settings.API_SECRET, salt="rolf-ipaddress-key")
    k1 = s1.dumps(dict(username=request.user.username,
                       remote_addr=request.META['REMOTE_ADDR']))
    s2 = URLSafeTimedSerializer(settings.API_SECRET, salt="rolf-timed-key")
    k2 = s2.dumps(dict(username=request.user.username))
    return dict(k1=k1, k2=k2, remote_addr=request.META['REMOTE_ADDR'])


def verify_key(request):
    # TODO: convert to a decorator
    key = request.META.get('HTTP_ROLF_API_KEY', '')
    s1 = URLSafeSerializer(settings.API_SECRET,
                           salt="rolf-ipaddress-key")
    try:
        d = s1.loads(key)
        # check their IP
        if d['remote_addr'] != request.META['REMOTE_ADDR']:
            return None
        return get_object_or_404(User, username=d['username'])
    except BadSignature:
        # try timed key
        s2 = URLSafeTimedSerializer(settings.API_SECRET,
                                    salt="rolf-timed-key")
        try:
            d = s2.loads(key, max_age=60 * 60 * 24 * 7)
            return get_object_or_404(User, username=d['username'])
        except BadSignature:
            # invalid
            return None
        except SignatureExpired:
            return None
    return None


def api_push(request, deployment_id):
    user = verify_key(request)
    if not user:
        return HttpResponseForbidden()
    if request.method != "POST":
        return HttpResponseNotAllowed()
    deployment = get_object_or_404(Deployment,
                                   id=deployment_id)
    if not deployment.can_push(user):
        return HttpResponseForbidden()
    statsd.incr('event.push')
    push = deployment.new_push(
        user=user, comment="")
    stages = [dict(
            name=stage.name,
            url="/api/1.0/push/%d/stage/%d/" % (push.id, stage.id))
              for stage in deployment.stage_set.all()]
    return HttpResponse(dumps(dict(stages=stages)),
                        mimetype="application/json")


def api_run_stage(request, push_id, stage_id):
    user = verify_key(request)
    if not user:
        return HttpResponseForbidden()
    if request.method != "POST":
        return HttpResponseNotAllowed()
    push = get_object_or_404(Push, id=push_id)
    if not push.deployment.can_push(user):
        return HttpResponseForbidden()
    stage = get_object_or_404(Stage, id=stage_id)

    statsd.incr('event.run_stage')
    pushstage = push.run_stage(stage.id,
                               # no support for rollback yet
                               None)
    logs = [dict(command=l.command, stdout=l.stdout,
                 stderr=l.stderr) for l in pushstage.log_set.all()]
    return HttpResponse(
        dumps(dict(status=pushstage.status,
                   logs=logs,
                   end_time=str(pushstage.end_time),
                   stage_id=pushstage.stage.id)),
        mimetype='application/json')


@muninview(config="""graph_title Total Pushes
graph_vlabel pushes
graph_category rolf""")
def total_pushes(request):
    return [("pushes", Push.objects.all().count())]


@muninview(config="""graph_title Pushes
graph_vlabel pushes
graph_category rolf""")
def current_pushes(request):
    return [("pushes",
             Push.objects.filter(start_time__gt=datetime.now() -
                                 timedelta(minutes=6)).count())]
