import tkinter as tk

class Window(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.geometry(f'{width}x{height}')
        self.title("TicTacToe")
        self.canvas = tk.Canvas(self)
        self.canvas.pack(expand=1, fill=tk.BOTH)

class Cross():
    def __init__(self, grid, x_ind, y_ind):
        tag = f'cross{x_ind}{y_ind}'
        grid.canvas.create_line(
            grid.x + grid.size * x_ind, grid.y + grid.size * y_ind,
            grid.x + grid.size * (x_ind + 1), grid.y + grid.size * (y_ind + 1),
            tag=tag)
        grid.canvas.create_line(
            grid.x + grid.size * x_ind, grid.y + grid.size * (y_ind + 1),
            grid.x + grid.size * (x_ind + 1), grid.y + grid.size * y_ind,
            tag=tag)

class Zero():
    def __init__(self, grid, x_ind, y_ind):
        tag = f'oval{x_ind}{y_ind}'
        grid.canvas.create_oval(
            grid.x + grid.size * x_ind, grid.y + grid.size * y_ind,
            grid.x + grid.size * (x_ind + 1), grid.y + grid.size * (y_ind + 1),
            tag=tag)

class Grid():
    color_dict = {0: 'red', 1: 'blue'}
    def click(self, event):
        x_ind = (event.x - self.x) // self.size
        y_ind = (event.y - self.y) // self.size
        ind = 3 * x_ind + y_ind + 1
        #ind~tag = f'rect{x_ind}{y_ind}'
        #self.canvas.itemconfigure(ind, fill=Grid.color_dict[self.turn%2])
        if (x_ind >=0 and x_ind < self.dim and 
            y_ind >=0 and y_ind < self.dim and 
            ind not in self.items):
            if self.turn%2:
                item = Zero(self, x_ind, y_ind)
                item_type = 'z'
            else:
                item = Cross(self, x_ind, y_ind)
                item_type = 'c'
            self.items[ind] = item
            self.line_sum['h' + item_type + str(x_ind)] += 1
            self.line_sum['v' + item_type + str(y_ind)] += 1
            if x_ind == y_ind:
                self.line_sum['d1' + item_type] += 1
            if x_ind + y_ind + 1 == self.dim:
                self.line_sum['d2' + item_type] += 1
            for value in self.line_sum.values():
                if value == 3:
                    winner = 'Zero' if self.turn%2 else 'Cross'
                    message = tk.Toplevel()
                    #message.canvas.destroy()
                    label = tk.Label(message, text=winner + ' Win!')
                    label.pack(expand=1, fill=tk.BOTH)
                    message.grab_set()
                    self.canvas.delete('all')
                    self.__init__(self, self.x, self.y, self.size, self.dim)
                    self.turn = -1
                    break
            self.turn += 1

    def __init__(self, root, left_top_x, left_top_y, size, dim):
        self.canvas = root.canvas
        self.x = left_top_x
        self.y = left_top_y
        self.size = size
        self.dim = dim
        self.turn = 0
        self.items = {}
        self.line_sum = {}
        for i in range(dim + 1):
            self.canvas.create_line(
                left_top_x + i * size, left_top_y,
                left_top_x + i * size, left_top_y + dim * size)
            self.canvas.create_line(
                left_top_x, left_top_y + i * size,
                left_top_x + dim * size, left_top_y+ i * size)
        #rect version
        '''for i in range(dim):
            for j in range(dim):
                #tag = f'rect{i}{j}'
                self.canvas.create_rectangle(
                    left_top_x + i * size, left_top_y + j * size,
                    left_top_x + (i + 1) * size, left_top_y + (j + 1) * size,)
                    #tag=tag)'''
        for item in 'cz':
            for i in range(dim):
                self.line_sum['h' + item + str(i)] = 0
                self.line_sum['v' + item + str(i)] = 0
            self.line_sum['d1' + item] = 0
            self.line_sum['d2' + item] = 0
        self.canvas.bind('<Button-1>', self.click)

if __name__ == "__main__":            
    root = Window(800, 600)
    grid = Grid(root, 50, 50, 100, 3)
    root.mainloop()

#for item_id in mainwin.canvas.find_all():        
#    mainwin.canvas.itemconfig(item, fill='red')
#lambda event: set_red(event, item_id, self.canvas)
