class BreadCrumbElement(object):

    def __init__(self, label, url, is_active=False):
        self.label = label
        self.url = url
        self.is_active = is_active
