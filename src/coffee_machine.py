import logging

from base.state import State
from base.state_machine import StateMachine
from base.utility import check_tanks, Singleton
from config import COFFEE_TYPES
from tanks import WaterTank, CoffeeBeanTank


logger = logging.getLogger('general')


class CoffeeMachineState(State):
    """
    Coffee Machine base state
    """

    def __init__(self):
        self.state_machine = None

    @property
    def coffee_machine(self):
        # lazy
        if not self.state_machine:
            self.state_machine = CoffeeMachine()
        return self.state_machine


class PouringCoffee(CoffeeMachineState):
    """
    State responds for pouring coffee, last state
    """

    def run(self):
        logger.info('{} is ready'.format(self.coffee_machine.chosen_coffee_name))
        # reset coffee data
        self.coffee_machine.chosen_coffee_name = None
        self.coffee_machine.chosen_coffee_data = None

    def next(self):
        return self.coffee_machine.waiting


class BrewingCoffee(CoffeeMachineState):
    """
    State responds for brewing coffee
    """

    def run(self):
        """
        Action brewing, depends on outside mechanism
        """
        pass

    def next(self):
        return self.coffee_machine.pouring_coffee


class BoilingWater(CoffeeMachineState):
    """
    State responds for boiling water
    """

    def run(self):
        """
        Action Boiling water, depends on outside mechanism. Reduce water tank level
        """
        self.coffee_machine.water_tank.decrease_weight(self.coffee_machine.chosen_coffee_data.get('water_weight'))

    def next(self):
        return self.coffee_machine.brewing_coffee


class GrindingBeans(CoffeeMachineState):
    """
    Grind Beans. The Coffee Machine state responds for grinding, reduce coffee beans level
    """

    def run(self):
        """Grinding beans action, depend on outside mechanism"""
        self.coffee_machine.beans_tank.decrease_weight(self.coffee_machine.chosen_coffee_data.get('beans_weight'))

    def next(self):
        return self.coffee_machine.boiling_water


class PendingSupply(CoffeeMachineState):
    """
    Pending state
    """

    def run(self):
        empty_tanks = []

        if not self.coffee_machine.beans_tank.status:
            empty_tanks.append(self.coffee_machine.beans_tank)
        if not self.coffee_machine.water_tank.status:
            empty_tanks.append(self.coffee_machine.water_tank)

        for tank in empty_tanks:
            while True:
                try:
                    answer = int(input('Type "1" to supply {} '.format(tank)))
                    if answer == 1:
                        tank.supply()
                        break
                except ValueError:
                    pass
        self.coffee_machine.is_pending = False
        return

    def next(self):
        return self.coffee_machine.waiting


class Waiting(CoffeeMachineState):
    """
    Idle state
    """

    def run(self):
        # checking tanks before run
        if check_tanks(self.coffee_machine):
            return
        self.chosen_coffee()

    def chosen_coffee(self):
        # choice simulation
        action = None
        coffee_kinds_list = COFFEE_TYPES.keys()
        while True:
            # Type name of coffee
            chosen_coffee = input(
                "Please choose coffee: {} | {} | {} | {}: ".format(*coffee_kinds_list))
            if chosen_coffee in coffee_kinds_list:
                try:
                    # 0 - return to coffee choice
                    # 1 - start next state
                    action = int(input("Escape: 0 | Make Coffee: 1 "))
                    self.coffee_machine.chosen_coffee_name = chosen_coffee
                    self.coffee_machine.chosen_coffee_data = COFFEE_TYPES.get(chosen_coffee, None)
                    logger.info('Starting making {}'.format(chosen_coffee))
                except ValueError:
                    # continue asking
                    pass
                if action == 1:
                    break

    def next(self):
        if not self.coffee_machine.is_pending:
            return self.coffee_machine.grinding_beans
        return self.coffee_machine.pending_supply


class Start(CoffeeMachineState):
    """
    Initializing Coffee Machine state
    """

    def run(self):
        # set tanks
        CoffeeMachine.water_tank = WaterTank()
        CoffeeMachine.beans_tank = CoffeeBeanTank()

    def next(self):
        # every start machine should check level of tanks (low level info)
        if not self.coffee_machine.is_pending:
            return self.coffee_machine.waiting
        return self.coffee_machine.pending_supply


class CoffeeMachine(StateMachine, metaclass=Singleton):
    beans_tank = None
    water_tank = None

    def __init__(self):
        """
        Initialize Coffee Machine
        """
        self.__is_pending = False
        self.chosen_coffee_data = None
        self.chosen_coffee_name = None
        super().__init__(initial_state=self.start)

    @property
    def start(self):
        # here should check that level of tanks are properly for run
        return Start()

    @property
    def brewing_coffee(self):
        return BrewingCoffee()

    @property
    def boiling_water(self):
        return BoilingWater()

    @property
    def waiting(self):
        return Waiting()

    @property
    def pending_supply(self):
        return PendingSupply()

    @property
    def grinding_beans(self):
        return GrindingBeans()

    @property
    def pouring_coffee(self):
        return PouringCoffee()

    @property
    def is_pending(self):
        return self.__is_pending

    @is_pending.setter
    def is_pending(self, value):
        if value not in [True, False]:
            return ValueError('Incorrect status')
        self.__is_pending = value
