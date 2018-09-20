from django.contrib import admin
from .models import Genre, Publicacion, Documentacion

# Register the Admin classes for Book using the decorator
@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genre', 'status', 'createDate', 'summary')
    list_filter = ('status', 'postDate')
    #fields = ['title', ('summary', 'status'), 'text', 'genre', ('createDate', 'postDate')]

    fieldsets = (
        ('General', {
            'fields': (('title', 'status'),('createDate', 'postDate'))
        }),
        ('Detalle', {
            'fields': (('summary', 'genre'),'text')
        }),
    )

@admin.register(Documentacion)
class DocumentacionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'createDate', 'summary')
    list_filter = ('status', 'createDate')

    fieldsets = (
        ('General', {
            'fields': (('title', 'status'),'createDate')
        }),
        ('Detalle', {
            'fields': ('summary','text')
        }),
    )


admin.site.register(Genre)