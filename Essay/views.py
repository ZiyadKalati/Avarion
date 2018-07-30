from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from .models import *

# Create your views here.

class EssayCreate(CreateView):
    model = Essay
    fields = ['title', 'slug', 'category', 'content']
    template_name = "Essay/create_form.html"

class EssayDetail(DetailView):
    """
    This presents the most recent revision of a
    particular essay.
    """

    """
    queryset is the default set of objects that get_object()
    will search through using the argument passed to this
    view class, namely <slug>.
    
    Another thing to note is that there is no need for
    'model = Essay' here since this is equivalent to
    'queryset = Essay.objects.all()'.
    """
    queryset = Essay.objects.filter(is_published=True)
    context_object_name = "essay"
    template_name = "Essay/essay_detail.html"


class EssayUpdate(UpdateView):

    queryset = Essay.objects.filter(is_published=True)
    fields = ['content']
    context_object_name = "essay"
    template_name = "Essay/edit_form.html"

    def save_draft(self):
        """
        This function retrieves the instance of the essay that is
        about to be updated, and creates a copy of it and saves it
        to the database. This is done easily by setting pk to None
        and saving the object. This is assuming primary keys are
        auto-generated.
        :return: nothing
        """
        old_draft = self.queryset.get(slug=self.kwargs['slug'])
        old_draft.pk = None
        old_draft.is_published = False
        old_draft.save()
        return

    def form_valid(self, form):
        self.save_draft()
        return super(EssayUpdate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('essay_detail', kwargs={'slug': self.kwargs['slug']})

class EssayList(ListView):
    queryset = Essay.objects.filter(is_published=True)
    context_object_name = "all_essays"
    template_name = "Essay/list.html"

    def get_queryset(self):
        return Essay.objects.filter(is_published=True).filter(category__iexact=self.kwargs['category'])