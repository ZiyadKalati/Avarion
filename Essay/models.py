from django.db import models
from django.template.defaultfilters import slugify

from copy import deepcopy

# Create your models here.
"""
class EssayManager(models.Manager):
    def copy_essay(self, old_draft):
        """"""
        Makes a deep copy of an essay and returns it
        :param old_draft: The Essay object to be copied
        :return: The copied instance of the Essay object
        """"""
        copy = deepcopy(old_draft)
        copy.is_published = False
        return copy
"""

class Essay(models.Model):
    """
    Represents an entire treatment of a topic,
    which is added upon gradually over time.
    """

    THOUGHTS = 'thoughts'
    MEDITATIONS = 'meditations'
    CATEGORY = [
        (THOUGHTS, 'Thoughts'),
        (MEDITATIONS, 'Meditations'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY, default=THOUGHTS)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    objects = models.Manager()
    #copy = EssayManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Essay, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('essay_detail', {'slug' : self.slug})

    #############################
    @property
    def h_title(self):
        """Getter of the essay title"""
        return self.title

    @h_title.setter
    def h_title(self, value):
        """Setter of the essay title"""
        self.title = value

    @h_title.deleter
    def h_title(self):
        """Deleter of the essay title"""
        del self.title

    ##############################
    @property
    def h_slug(self):
        """Getter of the essay slug"""
        return self.slug

    @h_slug.setter
    def h_slug(self, value):
        """Setter of the essay slug"""
        self.slug = value

    @h_slug.deleter
    def h_slug(self):
        """Deleter of the essay slug"""
        del self.slug

    ##############################
    @property
    def h_content(self):
        """Getter of the essay content"""
        return self.content

    @h_content.setter
    def h_content(self, value):
        """Setter of the essay content"""
        self.slug = value

    @h_content.deleter
    def h_content(self):
        """Deleter of the essay content"""
        del self.content

    ###############################
    @property
    def h_creation_time(self):
        """Getter of the date the essay created on"""
        return self.created_on

    @h_creation_time.setter
    def h_creation_time(self, value):
        """Setter of the date the essay created on"""
        self.created_on = value

    #################################
    @property
    def h_modify_time(self):
        """Getter of the date the essay was edited"""
        return self.modified_on

    #################################
    @property
    def h_is_published(self):
        """Getter of whether the essay is published"""
        return self.is_published

