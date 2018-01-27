from formskit.converters import ToBool
from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class CreateGroupForm(PostForm):

    def create_form(self):
        self.add_field(
            'name',
            label='Nazwa',
            validators=[NotEmpty()],
        )
        self.add_field(
            'ladder',
            label='Drabinka',
            validators=[NotEmpty()],
            convert=ToBool(),
        )

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.groups.create(
            name=data['name'],
            ladder=data['ladder'],
        )
        self.database().commit()


class EditGroupForm(CreateGroupForm):

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.name = data['name']
        self.instance.ladder = data['ladder']
        self.drivers.groups.update(self.instance)
        self.database().commit()

    def read_from(self, group):
        self.set_value('name', group.name)
        self.set_value('ladder', group.ladder)
        self.instance = group
