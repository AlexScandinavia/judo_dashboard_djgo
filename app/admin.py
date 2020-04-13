from django.contrib import admin
from app.models import Judoka


class JudokaAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('first_name', 'last_name', 'country', 'birthyear', 'world_ranking')
    list_filter = ('country',)
    ordering = ('world_ranking',)
    search_fields = ('first_name', 'last_name', 'country')


admin.site.register(Judoka, JudokaAdmin)
