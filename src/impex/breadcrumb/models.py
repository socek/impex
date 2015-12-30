from impex.application.requestable import Requestable


class BreadCrumbElement(Requestable):

    def __init__(self, label, url=None, parent=None):
        self._label = label
        self.url = url
        self.parent = parent

    def get_url(self):
        if self.url:
            return self.url(self.request)

    @property
    def label(self):
        return self._label


class EventElement(BreadCrumbElement):

    def __init__(self):
        super().__init__(None, parent='home')

    @property
    def label(self):
        event_id = self.matchdict['event_id']
        event = self.drivers.events.get_by_id(event_id)
        return event.name


class GameListElement(BreadCrumbElement):

    def __init__(self):
        super().__init__(
            'Mecze',
            parent='empty:event',
        )

    def get_url(self):
        event_id = self.matchdict['event_id']
        group_id = self.matchdict.get('group_id', None)
        if group_id:
            return self.route_path(
                'games:group_list',
                event_id=event_id,
                group_id=group_id
            )
        else:
            return self.route_path(
                'games:list',
                event_id=event_id,
            )

    @property
    def label(self):
        group_id = self.matchdict.get('group_id', None)
        if group_id:
            group = self.drivers.groups.get_by_id(group_id)
            return group.name
        else:
            return self._label


class BreadCrumb(Requestable):

    def feed_request(self, request):
        super().feed_request(request)
        for key, crumb in self.data.items():
            crumb.feed_request(request)

    def add(self, key, *args, **kwargs):
        self.data[key] = BreadCrumbElement(*args, **kwargs)

    def get_crumbs_for(self, key):
        if not key:
            return
        keys = []
        tmp = key
        while self.data[tmp].parent:
            keys.append(tmp)
            tmp = self.data[tmp].parent
        keys.append(tmp)
        keys.reverse()
        for key in keys:
            yield self.data[key]

    def __init__(self):
        self.data = {}

        self.add('home', 'Główna', lambda req: req.route_path('home'))

        self.add(
            'empty:admin',
            'Panel Administracyjny',
            parent='home',
        )
        self.add(
            'events:admin:list',
            'Wydarzenia',
            url=lambda req: req.route_path('events:admin:list'),
            parent='empty:admin',
        )

        self.add(
            'events:admin:create',
            'Dodawanie',
            url=lambda req: req.route_path('events:admin:create'),
            parent='events:admin:list',
        )
        self.add(
            'events:admin:edit',
            'Edycja',
            url=lambda req: req.route_path('events:admin:edit'),
            parent='events:admin:list',
        )
        self.add(
            'groups:admin:list',
            'Grupy',
            url=lambda req: req.route_path('groups:admin:list'),
            parent='empty:admin',
        )
        self.add(
            'groups:admin:create',
            'Dodawanie',
            url=lambda req: req.route_path('groups:admin:list'),
            parent='groups:admin:list',
        )
        self.add(
            'groups:admin:edit',
            'Edycja',
            url=lambda req: req.route_path('groups:admin:edit'),
            parent='groups:admin:list',
        )
        self.add(
            'games:admin:list',
            'Mecze',
            url=lambda req: req.route_path(
                'games:admin:list',
                event_id=req.matchdict['event_id'],
            ),
            parent='events:admin:list',
        )
        self.add(
            'games:admin:create',
            'Dodawanie',
            url=None,
            parent='games:admin:list',
        )
        self.add(
            'games:admin:edit',
            'Edycja',
            url=None,
            parent='games:admin:list',
        )
        self.add(
            'games:admin:edit_scores',
            'Tabela wyników',
            url=None,
            parent='games:admin:list',
        )
        self.add(
            'teams:admin:list',
            'Drużyny',
            url=lambda req: req.route_path(
                'teams:admin:list',
            ),
            parent='empty:admin',
        )
        self.add(
            'teams:admin:create',
            'Dodawanie',
            url=None,
            parent='teams:admin:list',
        )
        self.add(
            'teams:admin:edit',
            'Dodawanie',
            url=None,
            parent='teams:admin:list',

        )
        self.data['empty:event'] = EventElement()
        self.data['games:list'] = GameListElement()
