from django.contrib import admin
from datetime import datetime, time, timedelta

from activities.models import Activities, Categories

class PassedActivityFilter(admin.SimpleListFilter):
    title = 'Статус мероприятия'
    parameter_name = 'status'
    def lookups(self, request, model_admin):
        return [('passed', 'Завершено'),
            ('upcoming', 'Предстоит'),
            ]
    def queryset(self, request, queryset):
        if self.value() == 'passed':
            return queryset.filter(date__lt=datetime.today())
        elif self.value() == 'upcoming':
            return queryset.filter(date__gte=datetime.today())

@admin.register(Activities)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'time', 'end_time', 'duration', 'category', 'contact', 'view_count')
    list_display_links = ('id', 'title')
    list_editable = ('date', 'time','duration', 'category', 'contact')
    list_per_page = 5
    ordering = ('-date', 'time')
    actions = ['clear_views']
    search_fields = ('title', 'category__name')
    list_filter = (PassedActivityFilter, 'date', 'category')
    readonly_fields = ['slug', 'view_count']

    @admin.display(description='Время завершения', ordering='time')
    def end_time(self, activity: Activities):
        datetime_obj = datetime.combine(datetime.today(), activity.time)
        result = datetime_obj + activity.duration
        return result.time()

    @admin.action(description="Очистить просмотры")
    def clear_views(self, request, queryset):
        count = queryset.update(view_count=0)
        self.message_user(request, f"Изменено {count} записи(ей).")

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ('name',)