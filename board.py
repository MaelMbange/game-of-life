from tkinter import *
from tkinter.ttk import *

from cell import Cell

class Board(Canvas):
    def __init__(self, master, rows=100, cols=100,cell_size=15):    
        self.CELLS_SIZE = cell_size   

        super().__init__(master,width=self.CELLS_SIZE * cols,height=self.CELLS_SIZE *rows,bg='black')
        
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.show()

        self.bind('<1>', self._on_click)

    def show(self):
        self.delete(ALL)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_alive() :
                    self.create_rectangle(col*self.CELLS_SIZE , row*self.CELLS_SIZE , 
                                    (col+1)*self.CELLS_SIZE , (row+1)*self.CELLS_SIZE ,
                                    outline='darkgreen', fill='lime',activefill='lightblue')
                else:
                    self.create_rectangle(col*self.CELLS_SIZE , row*self.CELLS_SIZE , 
                                    (col+1)*self.CELLS_SIZE , (row+1)*self.CELLS_SIZE ,
                                    outline='', fill='',activefill='lightblue',activeoutline='darkgreen')

    def _on_click(self,event:Event):
        print(f'{event.y // self.CELLS_SIZE}: {event.x // self.CELLS_SIZE}')
        col = event.x // self.CELLS_SIZE
        row = event.y // self.CELLS_SIZE

        if self.cells[row][col].is_alive(): 
            self.set_state_at_specific(row,col,Cell.State.Dead)
        else:
            self.set_state_at_specific(row,col,Cell.State.Alive)
        self.show()

    def clear(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_alive(): 
                    self.set_state_at_specific(row,col,Cell.State.Dead)
        self.show()                    

    def set_state_at_specific(self,row,col,state:Cell.State):
        self.cells[row][col].state = state

    def calculate_next_state(self):
        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbors = 0
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if (r, c) != (row, col) and 0 < r < self.rows and 0 < c < self.cols:
                            if self.cells[r][c].is_alive():
                                live_neighbors += 1             
            
                self.cells[row][col].calculate_next_state(live_neighbors)   
            
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].update_state()
                
    

