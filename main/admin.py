from django.contrib import admin
from main.models import RefBook, RefBookVersion, RefBookElement


class RefBookVersionInline(admin.TabularInline):
    model = RefBookVersion
    extra = 1
    fields = ('version', 'start_date')
    show_change_link = True


class RefBookElementInline(admin.TabularInline):
    model = RefBookElement
    extra = 1
    fields = ('code', 'value')


@admin.register(RefBook)
class RefBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'current_version', 'current_version_start_date')
    search_fields = ('code', 'name')
    inlines = [RefBookVersionInline]

    def current_version(self, obj):
        """Возвращает текущую версию справочника (по start_date)."""
        latest_version = obj.versions.order_by('-start_date').first()
        return latest_version.version if latest_version else "—"

    current_version.short_description = "Текущая версия"

    def current_version_start_date(self, obj):
        """Возвращает дату начала действия текущей версии."""
        latest_version = obj.versions.order_by('-start_date').first()
        return latest_version.start_date if latest_version else "—"

    current_version_start_date.short_description = "Дата начала действия версии"


@admin.register(RefBookVersion)
class RefBookVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'refbook_code', 'refbook_name', 'version', 'start_date')
    search_fields = ('refbook__name', 'version')
    inlines = [RefBookElementInline]

    def refbook_code(self, obj):
        """Отображает код справочника."""
        return obj.refbook.code

    refbook_code.short_description = "Код справочника"

    def refbook_name(self, obj):
        """Отображает название справочника."""
        return obj.refbook.name

    refbook_name.short_description = "Наименование справочника"


@admin.register(RefBookElement)
class RefBookElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'code', 'value')
    search_fields = ('code', 'value')
