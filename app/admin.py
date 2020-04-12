from django.contrib import admin
from app.models import Judoka, JudoResult, JudoEvent


class JudokaAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('first_name', 'last_name', 'country', 'birthday', 'apercu_contenu')
    list_filter = ('country',)
    ordering = ('birthday',)
    search_fields = ('first_name', 'last_name', 'country')

    # Colonnes personnalisées
    def apercu_contenu(self, judoka):
        """
        Retourne les 20 premiers caractères du contenu de l'article. S'il
        y a plus de 20 caractères, il faut rajouter des points de suspension.
        """
        text = judoka.description[0:100]
        if len(judoka.description) > 100:
            return '%s…' % text
        else:
            return text

    apercu_contenu.short_description = 'Aperçu du contenu'


class JudoResultAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('judoka', 'result', 'category', 'event', 'date')
    list_filter = ('category',)
    ordering = ('date',)
    search_fields = ('judoka', 'event', 'country')


class JudoEventAdmin(admin.ModelAdmin):
    # Configuration de la liste d'articles
    list_display = ('event_name', 'date_start', 'country', 'event_type')
    list_filter = ('country',)
    ordering = ('date_start',)
    search_fields = ('event_name', 'country', 'event_type')


admin.site.register(Judoka, JudokaAdmin)
admin.site.register(JudoResult, JudoResultAdmin)
admin.site.register(JudoEvent, JudoEventAdmin)
