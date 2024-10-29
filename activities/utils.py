class DataMixin:
    title_page = None
    paginate_by = 3
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['cat_selected'] = None
        context.update(kwargs)
        return context

