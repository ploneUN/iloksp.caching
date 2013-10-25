from zope.event import notify
from z3c.caching.purge import Purge
from zope.globalrequest import getRequest
from zope.annotation.interfaces import IAnnotations
from plone.registry.interfaces import IRegistry
from zope.component import adapter, queryUtility

from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.interfaces import IPurger
from plone.cachepurging.utils import isCachePurgingEnabled
from plone.cachepurging.utils import getPathsToPurge
from plone.cachepurging.utils import getURLsToPurge

def syncPurge(obj):
    request = getRequest()

    paths = getPathsToPurge(obj, request)

    registry = queryUtility(IRegistry)
    if registry is None:
        return []

    if not isCachePurgingEnabled(registry=registry):
        return []

    purger = queryUtility(IPurger)
    if purger is None:
        return []

    settings = registry.forInterface(ICachePurgingSettings, check=False)
    purged_urls = []
    for path in paths:
        for url in getURLsToPurge(path, settings.cachingProxies):
            purger.purgeSync(url)
            purged_urls.append(url)

    return purged_urls


def purge(obj):
    notify(Purge(obj))
