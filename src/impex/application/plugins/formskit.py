from implugin.formskit.models import PostForm as BasePostForm
from implugin.formskit.widget import FormWidget as BaseFormWidget

from impex.application.requestable import Requestable
from impex.application.resources import Resources


class PostForm(BasePostForm, Requestable):
    pass


class FormWidget(BaseFormWidget):

    class Templates(BaseFormWidget.Templates):
        text = 'impex.application:templates/formskit/text.haml'
        date = 'impex.application:templates/formskit/date.haml'

    def date(self, name, disabled=False, autofocus=False):
        return self._input('date', name, disabled, autofocus)

    def _base_input(self, name):
        data = super()._base_input(name)
        self.resources = Resources()
        data['need'] = self.resources.need
        return data
