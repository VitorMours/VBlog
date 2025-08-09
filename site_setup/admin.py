from django.contrib import admin

from site_setup.models import MenuLink, SiteSetup

# Register your models here.

@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('text', 'url_or_path', 'new_tab')
    search_fields = ('text', 'url_or_path')
    list_filter = ('new_tab',)


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()