from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from activities.forms import AddActivitiesForm
from activities.models import Activities
from django.db.models import Q, Value

from activities.utils import DataMixin

class HomeActivityView(LoginRequiredMixin, DataMixin, ListView):
    model = Activities
    template_name = 'activities/activities_list.html'
    context_object_name = 'activities'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                               title = 'Мероприятия библиотеки',
                               selected_category = 0)

class ActivityDetail(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, DetailView):
    model = Activities
    template_name = 'activities/activity.html'
    slug_url_kwarg = 'activity_slug'
    pk_url_kwarg = 'activity_id'
    context_object_name = 'activity'
    permission_required = 'activities.view_activities'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title=context['activity'],)

class ActivityCategory(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'activities/activities_list.html'
    context_object_name = 'activities'
    allow_empty = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['activities'][0].category
        return self.get_mixin_context(context,
                                        title= 'Категория - ' + cat.name,
                                        selected_category = cat.id)
    def get_queryset(self):
        return Activities.objects.all().filter(category__slug=self.kwargs['category_slug'])

class AddActivity(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddActivitiesForm
    template_name = 'activities/add_activity.html'
    success_url = reverse_lazy('activities_index')
    title_page = 'Добавление мероприятия'
    permission_required = 'activities.add_activities'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

class UpdateActivity(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model = Activities
    fields = ['title', 'description', 'category', 'time', 'duration', 'contact']
    template_name = 'activities/add_activity.html'
    success_url = reverse_lazy('activities_index')
    title_page = 'Обновление мероприятия'
    permission_required = 'activities.change_activities'

class DeleteActivity(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, DeleteView):
    model = Activities
    success_url = reverse_lazy('activities_index')
    template_name = 'activities/delete_activity.html'
    title_page = 'Удаление мероприятия'
    permission_required = 'activities.delete_activities'

class ActivityArchive(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'activities/activities_list.html'
    context_object_name = 'activities'
    allow_empty = True
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        return self.get_mixin_context(context,
                                      title = f'Архив на {year}/{month}',
                                      year = year,
                                      month = month,
                                      selected_category = 0)
    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Activities.objects.all().filter(Q(date__year=year) & Q(date__month=month)).annotate(passed = Value(True))