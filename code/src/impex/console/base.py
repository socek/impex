from baelfire.dependencies import FileChanged
from baelfire.task import TemplateTask


class IniTemplate(TemplateTask):

    source_name = 'template:ini'
    output_name = 'frontendini'

    def create_dependecies(self):
        super().create_dependecies()
        self.build_if(FileChanged('package:default'))
        self.build_if(FileChanged('package:local'))

    def generate_context(self):
        context = super().generate_context()
        context['alembic'] = {
            'script_location': self.paths.get('migrations'),
            'sqlalchemy.url': self.settings['dburl'],
        }
        return context
