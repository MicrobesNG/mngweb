from __future__ import unicode_literals

import re

from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


# FAQ

class FaqIndexPage(Page):
    subpage_types = ['faq.FaqCategoryPage']

    @property
    def categories(self):
        return FaqCategoryPage.objects.live().descendant_of(self)

    def get_context(self, request):
        context = super(FaqIndexPage, self).get_context(request)

        # Add extra variables and return the updated context
        context['categories'] = self.categories
        return context


class FaqCategoryPage(Page):
    parent_page_types = ['faq.FaqIndexPage']

    @property
    def title_id(self):
        """The title of the category formatted as an HTML ID for page anchoring"""
        lower = self.title.lower()
        no_brackets = re.sub(r'\s*\(.+\)', '', lower)
        hyphens = no_brackets.replace(' ', '-')
        return hyphens

    # exclude from sitemap
    def get_sitemap_urls(self):
        return []

    content_panels = Page.content_panels + [
        InlinePanel('questions', label="Questions"),
    ]


class FaqQuestion(Orderable):
    page = ParentalKey('faq.FaqCategoryPage', related_name='questions')
    question = models.CharField(max_length=255)
    answer = RichTextField()

    panels = [
        FieldPanel('question'),
        FieldPanel('answer', classname="full"),
    ]

    def __str__(self):
        return self.question

