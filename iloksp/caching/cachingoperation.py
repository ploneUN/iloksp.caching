import random
import time

from plone.app.caching.operations.default import ModerateCaching
from plone.caching.utils import lookupOptions

from plone.app.caching.operations.utils import setCacheHeaders
from plone.app.caching.operations.utils import doNotCache
from plone.app.caching.operations.utils import cacheInRAM
from plone.app.caching.operations.utils import cacheStop

from plone.app.caching.operations.utils import cachedResponse
from plone.app.caching.operations.utils import notModified

from plone.app.caching.operations.utils import getETagAnnotation
from plone.app.caching.operations.utils import getContext
from plone.app.caching.operations.utils import getLastModifiedAnnotation

from plone.app.caching.operations.utils import fetchFromRAMCache
from plone.app.caching.operations.utils import isModified
from plone.app.caching.operations.utils import visibleToRole

from zope.interface import classProvides
from plone.caching.interfaces import ICachingOperationType
from plone.app.caching.interfaces import IETagValue

from zope.component import getMultiAdapter


class IntranetModerateCaching(ModerateCaching):
    """
    Caching similar to moderate caching, but caches private contents
    """

    classProvides(ICachingOperationType)

    title = u"Moderate caching for intranet"
    prefix = 'iloksp.caching.intranetModerateCaching'

    options = ('smaxage','etags','lastModified','anonOnly')

    def interceptResponse(self, rulename, response, class_=None):

        # Check for cache stop request variables
        if cacheStop(self.request, rulename):
            return None

        return None


    def modifyResponse(self, rulename, response, class_=None):
        options = lookupOptions(class_ or self.__class__, rulename)

        maxage   = options.get('maxage') or self.maxage
        smaxage  = options.get('smaxage') or self.smaxage
        etags    = options.get('etags') or self.etags

        anonOnly = options.get('anonOnly', self.anonOnly)
        vary     = u'Cookie,Accept-Encoding'

        # Add the ``anonymousOrRandom`` etag if we are anonymous only
        if anonOnly:
            if etags is None:
                etags = ['anonymousOrRandom']
            elif 'anonymousOrRandom' not in etags:
                etags = tuple(etags) + ('anonymousOrRandom',)

        etag = getETagAnnotation(self.published, self.request, etags)
        lastModified = getLastModifiedAnnotation(self.published, self.request, options['lastModified'])

        # Check for cache stop request variables
        if cacheStop(self.request, rulename):
            # only stop with etags if configured
            if etags:
                etag = "%s%d" % (time.time(), random.randint(0, 1000))
                return setCacheHeaders(self.published, self.request, response, etag=etag)
            # XXX: should there be an else here? Last modified works without extra headers.
            #      Are there other config options?

        # Do the maxage/smaxage settings allow for proxy caching?
        proxyCache = smaxage or (maxage and smaxage is None)

        setCacheHeaders(self.published, self.request, response, maxage=maxage, smaxage=smaxage,
            etag=etag, lastModified=lastModified, vary=vary)
