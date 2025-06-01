from enum import Enum


class Cell:
    class State(Enum):
        Alive= True
        Dead= False
    
    def __init__(self,state=None):
        self.state = state if state is not None else Cell.State.Dead
        self.next_state = Cell.State.Alive

    def is_alive(self):
        return self.state is Cell.State.Alive 
    

    def calculate_next_state(self,neighbors_count:int):
        if self.is_alive():
            self.next_state = Cell.State.Alive if neighbors_count == 2 or neighbors_count == 3 else Cell.State.Dead
        else:
            self.next_state = Cell.State.Alive if neighbors_count == 3 else Cell.State.Dead
        
    def update_state(self):
        self.state = self.next_state
        
    def __str__(self):
        return f'{hex(id(self))} is {self.state.name}'
    