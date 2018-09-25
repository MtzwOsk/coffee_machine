import random
import unittest
from unittest.mock import patch

from src.coffee_machine import CoffeeMachine, Start, Waiting, PendingSupply, GrindingBeans, PouringCoffee, \
    BoilingWater, BrewingCoffee
from src.tanks import CoffeeBeanTank, WaterTank
from src.config import WATER_TANK_WEIGHT_MAX, BEANS_TANK_WEIGHT_MAX, COFFEE_TYPES, WATER_MIN_WEIGHT, BEANS_MIN_WEIGHT


class TestCoffeeMachine(unittest.TestCase):
    """
    Tests for coffee machine
    """

    def setUp(self):
        self.coffee_machine = CoffeeMachine()
        self.coffee_type = list(COFFEE_TYPES)

    def test_initialize(self):
        """
        Test initializing
        """
        self.assertTrue(isinstance(self.coffee_machine.current_state, Start))

    def test_start_state(self):
        """
        Test start state
        """
        self.coffee_machine.start.run()
        # sets tanks
        self.assertTrue(self.coffee_machine.water_tank.weight, WATER_TANK_WEIGHT_MAX)
        self.assertTrue(self.coffee_machine.beans_tank.weight, BEANS_TANK_WEIGHT_MAX)
        self.assertTrue(self.coffee_machine.water_tank.status, 1)
        self.assertTrue(self.coffee_machine.beans_tank.status, 1)

    def test_waiting_state(self):
        """
        Test waiting
        """

        coffee_type = self.coffee_type[0]
        user_input = [coffee_type, 1]
        self.coffee_machine.start.run()
        self.coffee_machine.start.next()
        with patch('builtins.input', side_effect=user_input):
            self.coffee_machine.waiting.run()
        self.assertEqual(self.coffee_machine.chosen_coffee_name, coffee_type)

    def test_grinding_coffee_beans_state(self):
        """
        Test grinding coffee beans state
        """

        coffee_type = self.coffee_type[1]
        self.coffee_machine.beans_tank = beans_tank = CoffeeBeanTank()
        self.coffee_machine.chosen_coffee_name = coffee_type
        self.coffee_machine.chosen_coffee_data = coffee_data = COFFEE_TYPES.get(coffee_type)
        self.coffee_machine.grinding_beans.run()
        self.assertEqual(beans_tank.weight, (BEANS_TANK_WEIGHT_MAX - coffee_data.get('beans_weight')))

    def test_boiling_water_state(self):
        """
        Test boiling water
        """

        coffee_type = self.coffee_type[2]
        self.coffee_machine.water_tank = water_tank = WaterTank()
        self.coffee_machine.chosen_coffee_name = coffee_type
        self.coffee_machine.chosen_coffee_data = coffee_data = COFFEE_TYPES.get(coffee_type)
        self.coffee_machine.boiling_water.run()
        self.assertEqual(water_tank.weight, (WATER_TANK_WEIGHT_MAX - coffee_data.get('water_weight')))

    def test_pouring_coffee_state(self):
        """
        Test pouring state
        """

        coffee_type = self.coffee_type[3]
        self.coffee_machine.chosen_coffee_name = coffee_type
        self.coffee_machine.chosen_coffee_data = COFFEE_TYPES.get(coffee_type)
        self.coffee_machine.pouring_coffee.run()
        # finish state circle - reset coffee data for instance
        self.assertEqual(self.coffee_machine.chosen_coffee_data, None)
        self.assertEqual(self.coffee_machine.chosen_coffee_name, None)

    def test_pending_state(self):
        """
        Test pending supply state
        """

        # tanks low level
        user_input = [1, 1]
        water_weight = WATER_TANK_WEIGHT_MAX - random.randint(0, WATER_MIN_WEIGHT - 1)  # lowest than minimal value
        beans_weight = BEANS_TANK_WEIGHT_MAX - random.randint(0, BEANS_MIN_WEIGHT - 1)
        self.coffee_machine.water_tank = water_tank = WaterTank()
        self.coffee_machine.bean_tank = beans_tank = CoffeeBeanTank()
        water_tank.decrease_weight(water_weight)
        beans_tank.decrease_weight(beans_weight)
        self.assertEqual(beans_tank.status, 0)
        self.assertEqual(water_tank.status, 0)
        self.coffee_machine.waiting.run()
        self.assertTrue(isinstance(self.coffee_machine.waiting.next(), PendingSupply))
        self.assertEqual(self.coffee_machine.is_pending, True)
        # refill tanks
        with patch('builtins.input', side_effect=user_input):
            self.coffee_machine.pending_supply.run()
        # supply
        self.assertEqual(self.coffee_machine.beans_tank.status, 1)
        self.assertEqual(self.coffee_machine.water_tank.status, 1)
        self.assertFalse(self.coffee_machine.is_pending)
        self.assertTrue(isinstance(self.coffee_machine.pending_supply.next(), Waiting))

    def test_state_circle(self):
        user_input = [self.coffee_type[2], 1]
        self.coffee_machine.current_state.run()
        waiting_state = self.coffee_machine.current_state.next()
        with patch('builtins.input', side_effect=user_input):
            waiting_state.run()
        grinding_beans_state = waiting_state.next()
        grinding_beans_state.run()
        boiling_water_state = grinding_beans_state.next()
        boiling_water_state.run()
        brewing_coffee_state = boiling_water_state.next()
        pouring_coffee_state = brewing_coffee_state.next()
        pouring_coffee_state.run()
        self.assertTrue(isinstance(waiting_state, Waiting))
        self.assertTrue(isinstance(grinding_beans_state, GrindingBeans))
        self.assertTrue(isinstance(boiling_water_state, BoilingWater))
        self.assertTrue(isinstance(brewing_coffee_state, BrewingCoffee))
        self.assertTrue(isinstance(pouring_coffee_state, PouringCoffee))
        self.assertTrue(isinstance(pouring_coffee_state.next(), Waiting))


if __name__ == '__main__':
    unittest.main()
