
class Singleton(type):
    """Singleton"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def check_tanks(coffee_machine):
    """Function check if any of containers have to supplying"""
    coffee_machine.is_pending = bool(
        not coffee_machine.beans_tank.status or not coffee_machine.water_tank.status
    )
    return coffee_machine.is_pending
