class ContextMixin(object):
    """
    An easier way to deal with providing context data to templates.
    Less to type, cleaner on the eyes.

    class IndexView(ContextMixin, TemplateView):
        def get_context_data(self, **kwargs):
            today = datetime.date.today()
            books = Books.objects.all()
            return self.make_context_data(locals(), **kwargs)

    compare with the standard way:

    class IndexView(TemplateView):
        def get_context_data(self, **kwargs):
            context = super(IndexView, self).get_context_data(**kwargs)
            context['today'] = date.today()
            context['books'] = Books.objects.all()
            return context
    """
    def make_context_data(self, dictionary, **kwargs):
        context = super(ContextMixin, self).get_context_data(**kwargs)
        context.update(dictionary)
        return context
