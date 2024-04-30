from __future__ import annotations

# State base class
class State:
    def __init__(self):
        self.active = False

    @classmethod
    def evaluate(cls, context: StateMachine):
        #print(f"evaluate state")
        return False
    
    def on_enter(self, context: StateMachine):
        print(f"\n-> Enter state ({self.get_name()})")
        pass

    def on_update(self, context: StateMachine):
        #print("Update state ({self.get_name()})")
        pass

    def get_name(self):
        return "BaseState"


# this is the context
class StateMachine():
    def __init__(self):
        self.previous_state: State = None
        self.current_state: State = None

        self.on_change_state_callback = None

        # you can ordered by priority (first evaluated is setted)
        # only put instances here, dont put type values
        self.state_list: list[State] = []

    def set_state(self, new_state: State):
        # cannot set null state
        if new_state == None:
            return
        
        # already in that state
        if type(self.current_state) == type(new_state):
            return

        # change states
        if self.current_state != None:
            self.previous_state = self.current_state
            self.previous_state.active = False

        self.current_state = new_state
        self.current_state.active = True

        # initialize new state
        self.current_state.on_enter(context=self)

        # callback
        if self.on_change_state_callback is not None:
            self.on_change_state_callback()
    
    def evaluate_all(self):
        # first state evaluated is setted
        for state in self.state_list:
            # skip current
            if type(state) == type(self.current_state):
                continue

            if state.evaluate(context=self):
                self.set_state(state)
                return True
        return False
    
    def update_state(self):
        # no current state
        if self.current_state == None:
            return
        
        self.current_state.on_update(context=self)