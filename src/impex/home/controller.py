from impex.application.controller import Controller


class HomeController(Controller):

    renderer = 'impex.home:me.haml'

    def make(self):
        data = self.SampleData.upsert(name='elf')
        self.database().commit()
        self.context['data'] = data
