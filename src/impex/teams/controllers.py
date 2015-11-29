from impex.application.controller import Controller

from .forms import CreateTeamForm
from .widgets import CreateTeamFormWidget
from .widgets import EditTeamFormWidget


class TeamListController(Controller):

    renderer = 'impex.teams:templates/admin/list.haml'
    # permission = 'auth'

    def make(self):
        self.context['teams'] = self.drivers.teams.list()


class TeamCreateController(Controller):

    renderer = 'impex.teams:templates/admin/create.haml'
    # permission = 'auth'

    def make(self):
        form = self.add_form(
            CreateTeamForm,
            widgetcls=CreateTeamFormWidget,
        )

        if form.validate():
            self.add_flashmsg('Dodano drużynę.', 'info')
            self.redirect('teams:admin:list')


class TeamEditController(Controller):

    renderer = 'impex.teams:templates/admin/edit.haml'
    # permission = 'auth'

    def make(self):
        team_id = self.matchdict['team_id']
        team = self.drivers.teams.get_by_id(team_id)
        form = self.add_form_widget(EditTeamFormWidget)
        form.read_from(team)

        if form.validate():
            self.add_flashmsg('Zapisano zmiany w drużunie.', 'info')
            self.redirect('teams:admin:list')
