from iloksp.caching.utils import purge
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

def purge_homepage(obj, event):
    # homepage should be purged on
    # - All Add/Edit events.. due to recent-changes portlet
    site = getSite()
    purge(site)
