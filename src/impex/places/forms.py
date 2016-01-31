from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class CreatePlaceForm(PostForm):

    def create_form(self):
        self.add_field(
            'name',
            label='Nazwa',
            validators=[NotEmpty()],
        )

    def on_success(self):
        data = self.get_data_dict(True)
        self.drivers.places.create(
            name=data['name'],
        )
        self.database().commit()


class EditPlaceForm(CreatePlaceForm):

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.name = data['name']
        self.drivers.places.update(self.instance)
        self.database().commit()

    def read_from(self, place):
        self.set_value('name', place.name)
        self.instance = place
