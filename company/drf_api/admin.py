from django.contrib import admin
from drf_api.models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass
    
@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    pass

@admin.register(SocialNetworksRef)
class SocialNetworksRefAdmin(admin.ModelAdmin):
    pass

class SocialNetworksRefAdmin(admin.StackedInline):
	model = SocialNetworksRef
	extra = 2

class DepartmentRefAdmin(admin.StackedInline):
	model = DepartmentClientRef
	extra = 2
    
class DepartmentLegalEntityRefAdmin(admin.StackedInline):
	model = DepartmentLegalEntityRef
	extra = 2

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ('personal_id',)
    inlines = [SocialNetworksRefAdmin, DepartmentRefAdmin]

@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    readonly_fields = ('personal_id',)
    inlines = [DepartmentLegalEntityRefAdmin,]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    readonly_fields = ('personal_id',)