from django.contrib import admin
from models import Deployment, Category, Application


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Application, ApplicationAdmin)


class DeploymentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Deployment, DeploymentAdmin)
