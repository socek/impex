from impex.application.controller import Controller

from .widgets import CreatePlaceFormWidget
from .widgets import EditPlaceFormWidget


class PlaceListController(Controller):

    renderer = 'impex.places:templates/admin/list.haml'
    permission = 'admin'
    crumbs = 'places:admin:list'

    def make(self):
        self.context['places'] = self.drivers.places.list()


class PlaceCreateController(Controller):

    renderer = 'impex.places:templates/admin/create.haml'
    permission = 'admin'
    crumbs = 'places:admin:create'

    def make(self):
        form = self.add_form_widget(CreatePlaceFormWidget)

        if form.validate():
            self.add_flashmsg('Dodano miejsce.', 'info')
            self.redirect('places:admin:list')


class PlaceEditController(Controller):

    renderer = 'impex.places:templates/admin/edit.haml'
    permission = 'admin'
    crumbs = 'places:admin:edit'

    def make(self):
        place_id = self.matchdict['place_id']
        place = self.drivers.places.get_by_id(place_id)
        form = self.add_form_widget(EditPlaceFormWidget)
        form.read_from(place)

        if form.validate():
            self.add_flashmsg('Zapisano zmiany w miejscu.', 'info')
            self.redirect('places:admin:list')
