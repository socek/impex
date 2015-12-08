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
        datetime = 'impex.application:templates/formskit/datetime.haml'
        checkbox = 'impex.application:templates/formskit/checkbox.haml'
        select = 'impex.application:templates/formskit/select.haml'
        form_error = 'impex.application:templates/formskit/form_errors.haml'

    def _base_input(self, name):
        data = super()._base_input(name)
        self.resources = Resources()
        data['need'] = self.resources.need
        return data

    def date(self, name, disabled=False, autofocus=False):
        return self._input('date', name, disabled, autofocus)

    def checkbox(self, name, disabled=False, autofocus=False):
        return self._input('checkbox', name, disabled, autofocus)

    def datetime(self, name, disabled=False, autofocus=False):
        return self._input('datetime', name, disabled, autofocus)
