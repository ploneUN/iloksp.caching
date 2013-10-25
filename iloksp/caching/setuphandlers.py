from collective.grok import gs
from iloksp.caching import MessageFactory as _

@gs.importstep(
    name=u'iloksp.caching', 
    title=_('iloksp.caching import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('iloksp.caching.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
