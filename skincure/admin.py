from django.contrib import admin
from skincure.models import Profile, Result

class ProfileAdmin(admin.ModelAdmin):
    pass
class ResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Result, ResultAdmin)