# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import ukhtheme.grok
from os import path
from grok import util

from .layout import ILayer
from . import templates_dir
from megrok.pagetemplate import PageTemplate
from uvc.layout import viewlets
from uvc.layout.interfaces import IAboveContent
from uvc.layout.slots import managers, menuviewlets
from uvc.layout.slots.menuviewlets import DocumentActionsMenuViewlet
from uvc.layout.slots.menuviewlets import PersonalPreferencesViewlet
from uvc.layout.slots.menuviewlets import FooterTemplate
from uvc.tbskin.viewlets import Breadcrumbs
from uvcsite.viewlets import steps
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface import Interface
from zope.viewlet.interfaces import IContentProvider
from uvc.api.api import get_template


template_dir = path.join(
    path.dirname(ukhtheme.grok.__file__), 'templates')


class Navigation(grok.ViewletManager):
    grok.name('navigation')
    grok.context(Interface)


class FooterTemplate(FooterTemplate):
    grok.layer(ILayer)

    template = get_template(template_dir, 'footer.cpt')


class PersonalPreferencesViewlet(PersonalPreferencesViewlet):
    grok.layer(ILayer)
    grok.require('zope.View')

    def getFooter(self):
        return self.getFooterViewlet()

    def getPersonal(self):
        return self.menus

    @property
    def name(self):
        return self.request.principal.id

    def getFooterViewlet(self):
        viewlets = getMultiAdapter(
            (self.view.context, self.request, self.view),
            IContentProvider,
            'footermenu').getMenuItems()
        return viewlets


class PersonalPreferencesTemplate(PageTemplate):
    grok.view(PersonalPreferencesViewlet)
    grok.layer(ILayer)
    template = get_template(templates_dir, 'personalpreferencestemplate.cpt')


class FavIcon(grok.Viewlet):
    grok.layer(ILayer)
    grok.viewletmanager(managers.Headers)
    grok.context(Interface)
    template = get_template(templates_dir, 'favicon.cpt')


class GlobalMenuViewlet(menuviewlets.GlobalMenuViewlet):
    grok.layer(ILayer)
    grok.viewletmanager(Navigation)
    grok.order(1)

    def getUser(self):
        return self.usermenu

    def getNavigation(self):
        return self.menus

    def getRenderableItems(self):
        return self.renderableitems

    def getQuicklinks(self):
        return self.quicklinks()

    def application_url(self):
        return util.application_url(self.request, self.context)

    def quicklinks(self):
        menu = queryMultiAdapter((self.view.context, self.request, self.view),
                                 IContentProvider, 'quicklinks')
        if menu is not None:
            return menu.getMenuItems()
        return None

    @property
    def usermenu(self):
        menu = queryMultiAdapter((self.view.context, self.request, self.view),
                                 IContentProvider, 'personalpreferences')
        if menu is not None:
            return menu.getMenuItems()
        return None


class GlobalMenuTemplate(PageTemplate):
    grok.layer(ILayer)
    grok.view(menuviewlets.GlobalMenuViewlet)
    template = get_template(templates_dir, 'globalmenutemplate.cpt')


class NavigationTemplate(PageTemplate):
    grok.layer(ILayer)
    grok.view(GlobalMenuViewlet)
    template = get_template(templates_dir, 'navigationtemplate.cpt')


class BGHeader(viewlets.header.BGHeader):
    grok.layer(ILayer)
    grok.order(30)
    template = get_template(templates_dir, 'bgheader.cpt')

    def application_url(self):
        return util.application_url(self.request, self.context)


class DocumentActionsTemplate(PageTemplate):
    grok.view(DocumentActionsMenuViewlet)
    grok.layer(ILayer)
    template = get_template(templates_dir, 'documentactionstemplate.cpt')


class Breadcrumbs(Breadcrumbs):
    grok.layer(ILayer)
    template = None

    def available(self):
        return False

    def render(self):
        return None


class StepsProgressBar(steps.StepsProgressBar):
    grok.layer(ILayer)

    def available(self):
        return False


class DocumentTabs(grok.Viewlet):
    grok.viewletmanager(IAboveContent)
    grok.context(Interface)
    template = get_template(templates_dir, 'documenttabs.cpt')

    def tabs(self):
        menu = queryMultiAdapter((self.view.context, self.request, self.view),
                                 IContentProvider, 'extraviews')
        if menu is not None:
            return menu.getMenuItems()
        return None

    def update(self):
        self.actions = self.tabs()
