import logging

logger = logging.getLogger('general')


class TankMixin:
    """
    Base tank
    """
    __status = 0

    @property
    def weight(self):
        return self.__weight

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in [0, 1]:
            return ValueError('Incorrect status value {}'.format(value))
        self.__status = value

    def supply(self):
        # assume every supply fill setting to full tank level
        logger.info('{} is refill'.format(str(self)))
        self.__weight = self.MAX_VOLUME
        if self.status == 0:
            self.status = 1

    def decrease_weight(self, weight_down):
        self.__weight -= weight_down
        if self.weight <= self.MIN_VOLUME:
            logger.info('{} is empty'.format(str(self)))
            self.status = 0
