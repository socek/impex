from impex.application.controller import Controller

# from .forms import CreateForm


class OrdersListController(Controller):

    renderer = 'impex.teams:templates/admin/list.haml'
    # permission = 'auth'

    def make(self):
        pass


# class OrderCreateController(Controller):

#     renderer = 'impex.orders:templates/create.haml'
#     permission = 'auth'

#     def make(self):
#         form = self.add_form(CreateForm)
#         if form.validate():
#             self.database().commit()
#             self.add_flashmsg('Dodano zamówienie.', 'info')
#             self.redirect('orders:list')


# class OrderReadController(Controller):

#     renderer = 'impex.orders:templates/read.haml'
#     permission = 'auth'

#     def make(self):
#         order_id = self.matchdict['order_id']
#         order = self.drivers.Orders.get_by_id(order_id)
#         self.context['order'] = order
