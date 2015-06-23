from implugin.sqlalchemy.generator import DataGenerator

from .driver import ImpexDriverHolder


class ImpexDataGenerator(DataGenerator):

    def _get_driver_cls(self):
        return ImpexDriverHolder

    def make_all(self):
        self._create('SampleData', name='elf')
        self._create('SampleData', name='elf2')
        self._create('SampleData', name='elf3')
