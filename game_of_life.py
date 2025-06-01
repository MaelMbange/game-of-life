from threading import Thread, Timer
from tkinter import *
from tkinter.ttk import *
from random import choice

from board import Board
from cell import Cell

class GameOfLife(Frame):    
    PADX = 5

    def __init__(self, master=None,rows=100,cols=100):
        if master is None:
            master = Tk()
            master.title("Game of life")
            master.resizable(False,False)       
        super().__init__(master)

        self.isRunning: bool = False        
        
        self._create_control_frame()
        self._create_board(rows,cols)

        self.pack()

    def _create_control_frame(self):
        control_frame = Frame(self, padding=(GameOfLife.PADX,0))

        self.start_stop_text_variable = StringVar(value='start')
        self.button_start_stop = Button(control_frame,textvariable=self.start_stop_text_variable, command=self.start_stop)
        self.button_start_stop.pack(side=LEFT, padx=GameOfLife.PADX)
        
        self.button_next_step = Button(control_frame,text='next step', command=self.next_step)
        self.button_next_step.pack(side=LEFT, padx=GameOfLife.PADX)

        self.button_clear = Button(control_frame, text='clear',command=self._clear)
        self.button_clear.pack(side=LEFT, padx=GameOfLife.PADX)

        self.button_random = Button(control_frame,text='random',command=self._random)
        self.button_random.pack(side=LEFT, padx=GameOfLife.PADX)

        self.speed_values = ['slow','normal','fast']
        self.speed_box = Combobox(control_frame,values=self.speed_values,state='readonly')
        self.speed_box.current(1)
        self.speed_box.pack(side=LEFT,padx=5)

        control_frame.pack()

    def _create_board(self,rows,cols):
        self.board = Board(self, rows=rows,cols=cols)
        self.board.pack()

    def start_stop(self):
        if self.isRunning:
            print('stop clicked')
            self.isRunning = False
            self.start_stop_text_variable.set('start')
            
            self.button_random.config(state=ACTIVE)
            self.button_clear.config(state=ACTIVE)

            if self.timer is not None:
                self.timer.cancel()
        else:
            print('start clicked')
            self.isRunning = True
            self.start_stop_text_variable.set('stop')

            self.button_random.config(state=DISABLED)
            self.button_clear.config(state=DISABLED)
            self.next_step()

    def next_step(self):
        print('next clicked')
        self.board.calculate_next_state()
        self.board.show()
        if self.isRunning:
            delay = int(self.get_speed())
            self.after(delay, self.next_step)

    def get_speed(self):
        current_speed = self.speed_box.get()
        match current_speed:
            case 'slow':
                return 1000 * 1.5
            case 'fast':
                return 1000 * 0.5
            case _:
                return 1000
            

    def _clear(self):
        print('clear clicked')
        self.board.clear()

    def _random(self):
        print('random clicked')
        rows = self.board.rows
        cols = self.board.cols

        self.board.clear()

        for row in range(rows):
            for col in range(cols):
                if choice(range(4))%4 == 0:
                    self.board.set_state_at_specific(row,col,Cell.State.Alive)
        self.board.show()   

GameOfLife(rows=50,cols=50).mainloop()
