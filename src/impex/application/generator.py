from implugin.sqlalchemy.generator import DataGenerator

from .driver import ImpexDriverHolder


class ImpexDataGenerator(DataGenerator):

    def _get_driver_cls(self):
        return ImpexDriverHolder

    def make_all(self):
        self.create_users()

    def create_users(self):
        self._create(
            'Auth',
            name='admin',
            email='admin@admin.com',
            password='admin',
        )
