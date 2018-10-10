import tkinter as tk


class Gui():
    def __init__(self, title, size):
        self.win = tk.Tk()
        self.win.title(title)
        self.win.geometry(str(size[0])+'x'+str(size[1]))
        self.height = size[1]
        self.width = size[0]
        self.color = "black"
        self.canvas = []
        self.img = {}


    def start(self):
        self.win.mainloop()


    def make_canvas(self, size):
        self.canvas.append(tk.Canvas(self.win, bg="gray", width=size[0], height=size[1]))
        self.canvas[-1].pack(side="left")
        return len(self.canvas)-1


    # direction: 0 => horizontal
    #            1 => vertical
    def draw_straightLine(self, pos, id, direction=0):
        cur_canvas = self.canvas[id]
        if(direction == 0):
            cur_canvas.create_line(0, pos, self.width, pos, fill=self.color)
        elif(direction == 1):
            cur_canvas.create_line(pos, 0, pos, self.height, fill=self.color)


    def draw_img(self, coord, img_path, id):
        if(img_path not in self.img):
            cur_img = tk.PhotoImage(file=img_path)
            self.img.update({img_path: cur_img})
        else:
            cur_img = self.img[img_path]

        self.canvas[id].create_image(coord[0], coord[1], image=cur_img, anchor=tk.NW)



class Chessboard():
    def __init__(self, size, count):
        self.size = size
        self.unit = 32
        self.win = Gui("8Queens Genetic Algorithm",
                       (self.unit*size[0]*count, self.unit*size[1]))
        for _ in range(count):
            self.win.make_canvas((self.unit*size[0], self.unit*size[1]))

        for id in range(len(self.win.canvas)):
            for row in range(size[1]):
                self.win.draw_straightLine(row * self.unit, id, 0)

            for col in range(size[0]):
                self.win.draw_straightLine(col * self.unit, id, 1)


    def draw_queens(self, coords, id):
        for coord in coords:
            self.win.draw_img((coord[0]*self.unit, coord[1]*self.unit),
                              "./img/queen_half.png", id)


    def start(self):
        self.win.start()