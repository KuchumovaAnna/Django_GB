from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'lesson_2/index.html'
