from django.contrib import admin
from .models import Manufacturer, Sculptor, Artist, Form, Painting, MilkJug, Photo


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    ordering = ['name']


@admin.register(Sculptor)
class SculptorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    readonly_fields = ['uploaded_at']


@admin.register(MilkJug)
class MilkJugAdmin(admin.ModelAdmin):
    list_display = [
        'get_name', 'manufacturer', 'form', 'painting', 
        'owner', 'visibility', 'is_published', 'created_at'
    ]
    list_filter = [
        'manufacturer', 'sculptor', 'artist', 'form', 'painting',
        'visibility', 'is_published', 'has_mark', 'condition'
    ]
    search_fields = [
        'name', 'manufacturer__name', 'sculptor__name', 'artist__name',
        'form__name', 'painting__name', 'comments', 'owner__username'
    ]
    raw_id_fields = ['owner']
    date_hierarchy = 'created_at'
    inlines = [PhotoInline]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'manufacturer', 'sculptor', 'artist', 'form', 'painting',
                'name', 'year'
            )
        }),
        ('Дополнительные параметры', {
            'fields': (
                'material', 'country', 'factory',
                'height', 'volume', 'condition'
            ),
            'classes': ('collapse',)
        }),
        ('Клеймо', {
            'fields': ('has_mark', 'mark_description'),
            'classes': ('collapse',)
        }),
        ('Владелец и публикация', {
            'fields': ('owner', 'visibility', 'is_published')
        }),
        ('Дополнительно', {
            'fields': ('source', 'comments'),
            'classes': ('collapse',)
        }),
    )
    
    def get_name(self, obj):
        return str(obj)
    get_name.short_description = 'Молочник'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['milk_jug', 'is_main', 'order', 'uploaded_at']
    list_filter = ['is_main', 'uploaded_at']
    raw_id_fields = ['milk_jug']
    ordering = ['milk_jug', 'order']
