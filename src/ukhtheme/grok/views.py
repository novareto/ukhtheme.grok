# -*- coding: utf-8 -*-

import grok
import megrok.pagetemplate as pt

from . import templates_dir
from .layout import ILayer
from dolmen.forms.base import ApplicationForm
from uvc.api import Page, Form
from uvc.api.api import get_template
from uvc.layout.forms.components import Wizard
from uvcsite.homefolder import views
from uvcsite import IUVCSite
from megrok import pagetemplate as pt


class FormTemplate(pt.PageTemplate):
    pt.view(Form)
    grok.layer(ILayer)
    template = get_template(templates_dir, 'formtemplate.cpt')


#class UVCHome(Page):
#    grok.name('index')
#    grok.context(IUVCSite)
#    template = get_template(templates_dir, 'home.cpt')


class HomeFolderIndex(views.Index):
    grok.layer(ILayer)

    cssClasses = {'table': 'table table-hover table-striped'}


class WizardTemplate(pt.PageTemplate):
    grok.layer(ILayer)
    pt.view(Wizard)
    template = get_template(templates_dir, 'wizardtemplate.cpt')
