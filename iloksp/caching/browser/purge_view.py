from five import grok
from Products.CMFCore.interfaces import IContentish
from zope.event import notify
from z3c.caching.purge import Purge
from iloksp.caching.interfaces import IProductSpecific
from iloksp.caching.utils import syncPurge
from Products.statusmessages.interfaces import IStatusMessage

grok.templatedir('templates')

class PurgeView(grok.View):
    grok.name('purge_cache')
    grok.require('cmf.ManagePortal')
    grok.template('purge_view')
    grok.context(IContentish)
    grok.layer(IProductSpecific)

    def update(self):
        if (self.request.method == 'POST' and 
            'purge' in self.request.keys()):
            
            urls = syncPurge(self.context)
            for url in urls:
                IStatusMessage(self.request).add('Purged %s' % url)
