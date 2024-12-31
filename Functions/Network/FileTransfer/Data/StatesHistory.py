import datetime
from itertools import zip_longest

from Functions.Network.FileTransfer.Data.States import RequestStates


class StatesHistory(RequestStates):
    def __init__(self, on_update: callable = None):
        self._states: dict[float, int] = {}
        self.on_update = on_update
        self.is_finished = False

        self.updateState(self.state_initialised)

    def updateState(self, newState: int, t: float = None, call_function=False, update_state=True):
        """Setting a new state."""
        assert self.states_dict_int_to_str.get(newState) is not None, "New state is out of range."
        t = t if t is not None else datetime.datetime.now().timestamp()
        while self._states.get(t) is not None:
            t += 0.000001
        if update_state:
            self._states[t] = newState
            self.is_finished = newState in (
                self.state_error, self.state_cancelled, self.state_completed, self.state_timed_out_client_response
            )

        if self.on_update is not None and call_function:
            print('on_update:', newState)
            self.on_update(newState)

    def getState(self) -> int | None:
        """Returns current state."""
        return tuple(self._states.values())[-1] if self._states else None

    def getHistoryStates(self) -> dict[float, int]:
        """Returns original states history."""
        return self._states

    def getHistoryStates_str(self) -> dict[float, str]:
        """Converts original dictionary from integer to string states."""
        return dict(
            zip_longest(
                self._states.keys(),
                tuple(
                    map(
                        lambda x: self.states_dict_int_to_str.get(x),
                        self._states.values()
                    )
                )
            )
        )

    def __contains__(self, item):
        return item in self._states.values()
