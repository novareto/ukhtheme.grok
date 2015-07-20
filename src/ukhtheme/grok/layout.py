# -*- coding: utf-8 -*-

import os
import grok

from . import templates_dir
from uvc.tbskin.skin import ITBSkin, Layout
from uvc.api.api import get_template
from ukhtheme.resources import tune


class ILayer(grok.IDefaultBrowserLayer):
    pass


class ISkin(ILayer, ITBSkin):
    grok.skin('ukhtheme')


class MasterLayout(Layout):
    grok.name("")
    grok.layer(ILayer)
    template = get_template(templates_dir, 'masterlayout.cpt')

    def update(self):
        tune.need()
        Layout.update(self)

    def default_namespace(self):
        namespace = Layout.default_namespace(self)
        namespace['content'] = self.view.content()
        return namespace
