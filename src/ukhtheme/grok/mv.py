import grok
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IContentProvider
from uvc.layout.interfaces import IPageTop



grok.templatedir('templates')


class SpotMenuViewlet(grok.Viewlet):
    grok.viewletmanager(IPageTop)
    grok.context(Interface)
    grok.order(5)

    id = "spotmenuviewlet"

    def update(self):
        self.menus = getMultiAdapter(
                (self.view.context, self.request, self.view),
                IContentProvider, 'spotmenu').getMenuItems()
