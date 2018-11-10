import Tkinter as tk
import math

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.pack(fill="both", expand=True)

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.canvas.create_oval(x-5, y-5, x+5, y+5, 
                                outline=color, fill=color, tags="token")

    def create(self, xA, yA, xB, yB, d=10):
        self._create_token((xA, yA), "white")
        self._create_token((xB, yB), "pink")

        t = math.atan2(yB - yA, xB - xA)
        xC = (xA + xB)/2 + d * math.sin(t)
        yC = (yA + yB)/2 - d * math.cos(t)
        xD = (xA + xB)/2 - d * math.sin(t)
        yD = (yA + yB)/2 + d * math.cos(t)

        self.canvas.create_line((xA, yA), (xC, yC), (xB, yB), smooth=True)
        self.canvas.create_line((xA, yA), (xD, yD), (xB, yB), smooth=True, fill="red")

if __name__ == "__main__":
        app = SampleApp()
        app.create(100, 200, 600, 250)
        app.mainloop()