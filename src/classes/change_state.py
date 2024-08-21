class MaschineState:
    def __init__(self):
        self.state_stack = []
        self.current_state = "kapali"

    def change_state(self, new_state):
        if new_state == "kapali":
            # Kapali ist ein Endzustand, alles andere wird deaktiviert
            self.state_stack.clear()
            self.current_state = new_state
        elif new_state == "start":
            # Start ist ein eigenständiger Zustand, nichts anderes kann aktiv sein
            self.state_stack.clear()
            self.current_state = new_state
        elif new_state == "stop":
            # Stop kann mit anderen Zuständen kombiniert werden
            if "kapali" not in self.state_stack and "start" not in self.state_stack:
                self.state_stack.clear()
                self.state_stack.append(new_state)
                self.current_state = new_state
        elif new_state in ["bobin", "ariza", "ayar", "cozgu"]:
            # Diese Zustände können nur in Kombination mit Stop vorkommen
            if "stop" in self.state_stack:
                if new_state not in self.state_stack:
                    self.state_stack.append(new_state)
                    self.current_state = new_state

    def deactivate_state(self, state):
        if state in self.state_stack:
            self.state_stack.remove(state)
            self.current_state = self.state_stack[-1] if self.state_stack else "stop"

    def get_state(self):
        return self.current_state
