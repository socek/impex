from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class CreateGroupForm(PostForm):

    def create_form(self):
        self.add_field('name', label='Nazwa', validators=[NotEmpty()])

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.groups.create(
            name=data['name'],
        )
        self.database().commit()


class EditGroupForm(CreateGroupForm):

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.name = data['name']
        self.drivers.groups.update(self.instance)

    def read_from(self, group):
        self.set_value('name', group.name)
        self.instance = group
