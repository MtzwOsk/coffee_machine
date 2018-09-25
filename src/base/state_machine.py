import logging

logger = logging.getLogger('general')


class StateMachine:
    """
    Machine state
    """
    def __init__(self, initial_state=None):
        """
        Initialize state machine
        """
        self.current_state = initial_state

    def run(self):
        self.current_state.run()
        while True:
            self.current_state = self.current_state.next()
            self.current_state.run()
