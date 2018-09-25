from base.utility import Singleton
from config import BEANS_TANK_WEIGHT_MAX, WATER_TANK_WEIGHT_MAX
from config import BEANS_MIN_WEIGHT, WATER_MIN_WEIGHT
from base.tank import TankMixin

import logging

logger = logging.getLogger('general')


class CoffeeBeanTank(TankMixin, metaclass=Singleton):
    """
    Coffee bean container
    """
    MIN_VOLUME = BEANS_MIN_WEIGHT
    MAX_VOLUME = BEANS_TANK_WEIGHT_MAX

    def __init__(self):
        """
        Initialization, setting status and level of tank
        """
        # Initialization should check level, and set status depend on outside information.
        self.supply()
        self.status = 1  # 1 - level ok, 0 - need supply
        logger.info('Initialization coffee beans tank')

    def __str__(self):
        return 'Coffee beans tank'


class WaterTank(TankMixin, metaclass=Singleton):
    """
    Water container
    """

    MIN_VOLUME = WATER_MIN_WEIGHT
    MAX_VOLUME = WATER_TANK_WEIGHT_MAX

    def __init__(self):
        """
        Initialization, setting status and level of tank
        """
        # Initialize should check level, and sets status depend on outside information, sets max possible weight
        self.supply()
        self.status = 1  # 1 - level ok, 0 - need supply
        logger.info('Initialization coffee beans tank')

    def __str__(self):
        return 'Water tank'
