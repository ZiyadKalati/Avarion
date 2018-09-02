from django.db import models
#from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

from copy import deepcopy
from random import choice
import string

# Create your models here.

class EssayManager(models.Manager):
    def copy_essay(self, old_draft):
        """
        Makes a deep copy of an essay and returns it
        :param old_draft: The Essay object to be copied
        :return: The copied instance of the Essay object
        """
        copy = deepcopy(old_draft)
        copy.is_published = False
        return copy

    def gen_slug(self, size=11, chars=string.ascii_letters + string.digits + "_"):
        """
        You still need to do this doc.
        :param size: The length of the slug
        :param chars: The characters that will constitute the makeup of the slug
        :return: The newly generated slug
        """
        acceptable_collisions = 10

        for collisioni in range(acceptable_collisions):
            new_slug = "".join(choice(chars) for _ in range(size))
            try:
                Essay.objects.get(slug=new_slug)
            except ObjectDoesNotExist:
                return new_slug
            else:
                if collisioni == (acceptable_collisions - 1):
                    # Recursive
                    return self.gen_slug(size=(size + 1))

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
    is_draft = models.BooleanField(default=False)
    objects = models.Manager()
    essay_manager = EssayManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override the save method to check if a slug exists for this essay,
        if not then create a random 11 character string and assign it to 'slug'.
        The reason a random string of characters is created is because an
        option to change the title of the essay will be given to the user. If
        the title of the essay is slugified instead, and the title is later
        changed when the essay is edited, the slug and essay title will not
        match. That would look horrendous.

        Note: There is no way to check for collisions yet.
        """

        if not self.slug:
            self.slug = Essay.essay_manager.gen_slug()
        return super(Essay, self).save(*args, **kwargs)


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

