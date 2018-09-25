import logging

from coffee_machine import CoffeeMachine


logger = logging.getLogger('general')


if __name__ == '__main__':
    coffee_machine = CoffeeMachine()
    coffee_machine.run()
    logging.info('Start coffee machine')
