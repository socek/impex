from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class CreateTeamForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])
        self.add_field('hometown', label='Miasto')

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.teams.create(
            name=data['name'],
            hometown=data['hometown']
        )
        self.database().commit()


class EditTeamForm(CreateTeamForm):

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.name = data['name']
        self.instance.hometown = data['hometown']
        self.drivers.teams.update(self.instance)

    def read_from(self, team):
        self.set_value('name', team.name)
        self.set_value('hometown', team.hometown)
        self.instance = team
