from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'lesson_2/index.html'


class NewsPageView(TemplateView):
    template_name = 'lesson_2/news.html'

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)

        contex['news_title'] = 'First title'
        contex['news_preview'] = 'Test preview for first news'
        contex['range'] = range(5)
        contex['datetime_obj'] = datetime.now()

        return contex


class CoursesPageView(TemplateView):
    template_name = 'lesson_2/courses_list.html'


class ContactsPageView(TemplateView):
    template_name = 'lesson_2/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'lesson_2/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'lesson_2/login.html'