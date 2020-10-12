class Event(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    """
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

class pluginManager:
    def __init__(self, plugins):
        self.onDownloadRaw         = Event()
        self.onLoadObservationSite = Event()

        for plugin in plugins:
            if hasattr(plugin, '__onDownloadRaw__'):
                self.onDownloadRaw.append(plugin.__onDownloadRaw__)

            if hasattr(plugin, '__onLoadObservationSite__'):
                self.onLoadObservationSite.append(plugin.__onLoadObservationSite__)