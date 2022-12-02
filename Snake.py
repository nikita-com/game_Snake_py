from tkinter import *
import random

window = Tk()
window.title('snake')
in_game = True
width = 800
height = 600
seg_size = 20
c = Canvas(width=width, height=height, bg="#003300")
c.grid()
c.focus_set()


class Segment(object):
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x+seg_size, y+seg_size, fill='white')


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0)}
        self.vector = self.mapping["Right"]

    def move(self):
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0]*seg_size,
                 y1 + self.vector[1]*seg_size,
                 x2 + self.vector[0]*seg_size,
                 y2 + self.vector[1]*seg_size)

    def check_vector(self, button):
        if self.vector == (0, 1) and button != "Up":
            return True
        elif self.vector == (0, -1) and button != "Down":
            return True
        elif self.vector == (-1, 0) and button != "Right":
            return True
        elif self.vector == (1, 0) and button != "Left":
            return True
        return False

    def change_direction(self, event):
        if event.keysym in self.mapping and s.check_vector(event.keysym):
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2]-seg_size
        y = last_seg[3]-seg_size
        self.segments.insert(0, Segment(x, y))


segments = [Segment(seg_size, seg_size),
            Segment(seg_size*2, seg_size),
            Segment(seg_size*3, seg_size)]
s = Snake(segments)


def create_block():
    global BLOCK
    posx = seg_size*(random.randint(1, (width-seg_size)/seg_size))
    posy = seg_size*(random.randint(1, (height-seg_size)/seg_size))
    BLOCK = c.create_oval(posx, posy,
                          posx + seg_size,
                          posy + seg_size,
                          fill="red")


def main():
    global in_game
    if in_game:
        s.move()
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        if x1 < 0 or x2 > width or y1 < 0 or y2 > height:
            in_game = False
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        else:
            for index in range(len(s.segments)-1):
                if c.coords(s.segments[index].instance) == head_coords:
                    in_game = False
        window.after(100, main)
    else:
        c.create_text(width/2, height/2,
                      test="GAME OVER!",
                      font="Arial 20",
                      fill="#ff0000")


c.bind("<KeyPress>", s.change_direction)
create_block()
main()
window.mainloop()
