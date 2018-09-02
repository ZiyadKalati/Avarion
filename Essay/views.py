from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.db.models import Count
from .models import *

# Create your views here.

class EssayCreate(CreateView):
    model = Essay
    fields = ['title', 'category', 'is_draft', 'content']
    template_name = "Essay/create_form.html"

    # The same variable exists in EssayUpdate view. Make
    # sure to keep them in sync
    draft_slug_append = '--'

    def get_initial(self):
        """
        Override. This will dynamically generate default values of the fields
        when creating a new essay. These, of course, can be changed
        by the user.
        :return: a dictionary containing all initial values to the
                fields of the form
        """
        initial = super(EssayCreate, self).get_initial()

        """
        Aggregate functions like Count are used in the "aggregate" clause
        Aggregate allows you to collect a bunch of objects and then run some
        aggregate function on this collection to derive some value from it.
        Here we are running the Count function to count the number of Essay
        objects that have slugs. All of them do, so set its 'distinct' attribute
        to True, to make sure we ignore all revisions and only count unique essays.
        The unique_slugs keyword is arbitrary; it's the key to the dictionary returned.
        """
        # First, remove drafts that have been moved from public to private view from
        # the queryset. They are duplicates of an essay that is still in public view.
        no_draft_duplicates = Essay.objects.exclude(slug__contains=self.draft_slug_append)

        essay_count = no_draft_duplicates.aggregate(unique_slugs=Count('slug', distinct=True))
        essay_count = essay_count['unique_slugs']

        # The default title will be a number. The number equals to the number of
        # unique essays plus 1
        default_title = 'Post #' + str(essay_count + 1)
        initial['title'] = default_title
        return initial

    def get_success_url(self, **kwargs):
        return reverse('essay_detail', kwargs={'slug': self.object.slug})

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
    fields = ['title', 'is_draft', 'content']
    context_object_name = "essay"
    template_name = "Essay/edit_form.html"

    # The same variable exists in EssayCreate view. Make
    # sure to keep them in sync
    draft_slug_append = '--'
    slug_append_len = len(draft_slug_append)

    def save_revision(self, form):
        """
        This function retrieves the instance of the essay that is
        about to be updated, and creates a copy of it and saves it
        to the database. This is done easily by setting pk to None
        and saving the object. This is assuming primary keys are
        auto-generated.

        If the essay is being moved from public view to private view
        (turned to draft), then the last revision in public view will
        still remain in public view, and the last edit version of the
        essay will be moved to the drafts section. However, both will
        have the same slugs this way which will prevent Django from
        displaying either in Detail View, so a special string,
        draft_slug_append, is appended to the last edit to denote
        that it is a draft.

        If the essay is being moved back to public view, any last
        revisions of this essay in public view will be un-published,
        and this current edit will take its place.
        :param form: Contains the updated fields that are to be posted.
        :return: nothing
        """

        old_draft = self.queryset.get(slug=self.kwargs['slug'])
        old_draft.pk = None

        changed_data = form.changed_data
        # If moving from public view to private (draft) view
        if ('is_draft' in changed_data) and (self.object.is_draft is True):
            self.object.slug = self.object.slug + self.draft_slug_append
        elif ('is_draft' not in changed_data) and (self.object.is_draft is True):
            # If remaining in private (draft) view
            old_draft.is_published = False
            old_draft.slug = old_draft.slug[:-self.slug_append_len]
            self.object.save()
        else:
            # Call function to check if private draft is replacing an existing
            # public essay
            self.check_final_exists()
            old_draft.is_published = False

        old_draft.save()
        return

    def check_final_exists(self):
        """
        This method checks if the essay being updated will be removed as
        a draft and moved to public view (as a final draft). If this is
        the case, then it will check if a previous revision of the essay
        currently exists as a final draft, and un-publish it if this is
        the case. The latest revision of the essay (which is currently
        being handled by this view) will take its place.
        :param form: Contains the updated fields that are to be posted.
        :return: nothing
        """

        # Check if slug of the submitted form ends in draft_slug_append
        # If so, find the earlier revision and un-publish it.
        if self.object.slug[-self.slug_append_len:] == self.draft_slug_append:
            # First remove the last letters of the slug of the draft, draft_slug_append
            self.object.slug = self.object.slug[:-self.slug_append_len]

            # Then use the slug to find the copy of the last revision that was public
            old_draft = self.queryset.filter(is_draft=False).get(slug=self.object.slug)
            old_draft.is_published = False
            old_draft.save()
        return

    def form_valid(self, form):
        """
        If the form is valid, Django executes this function on its
        own.

        This method checks which fields of the form were changed,
        and if the content or title of the essay were changed then
        save_revision is called to save a copy of the old revision
        in the database.
        If no changes were made or if the user only publishes the
        essay as a draft or as a final draft (unchecks the is_draft
        form field), then no copy of the previous revision needs to
        be made and saved to the database.
        :param form: The form that is submitted by the user
        :return: Don't know don't care.. for now
        """

        changed_data = form.changed_data
        if (len(changed_data) == 1) and ('is_draft' in changed_data):
            # If 'is_draft' is False then draft is being moved to public view
            # Call function to check if draft is replacing an existing public essay
            if (form.cleaned_data['is_draft'] == False):
                self.check_final_exists()

            self.object.save()
        elif len(changed_data) == 0:
            self.object.save()
        else:
            self.save_revision(form)
        return super(EssayUpdate, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('essay_detail', kwargs={'slug': self.object.slug})

class EssayList(ListView):
    template_name = "Essay/list.html"

    def get_context_data(self, **kwargs):
        context = super(EssayList, self).get_context_data(**kwargs)
        all_published = Essay.objects.filter(is_published=True).filter(category__iexact=self.kwargs['category'])
        context['all_final'] = all_published.filter(is_draft=False)
        context['all_drafts'] = all_published.filter(is_draft=True)
        return context

    def get_queryset(self):
        """
        This method is literally here only because Django complained that
        this view was not returning a queryset.
        """
        return Essay.objects.filter(is_published=True).filter(category__iexact=self.kwargs['category'])