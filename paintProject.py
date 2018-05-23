from Tkinter import *
from tkColorChooser import askcolor
from PIL import Image,ImageDraw
import ttk
def brush(event):
    x1, y1 = (event.x - int(BrushSize.get())), (event.y - int(BrushSize.get()))
    x2, y2 = (event.x + int(BrushSize.get())), (event.y + int(BrushSize.get()))
    canvas.create_oval(x1, y1, x2, y2, fill=color[1],outline=color[1])
    canvas.draw.ellipse(((x1, y1, x2, y2)), fill=color[1], outline=color[1])
def eraser(event):
    python_green = "white"
    x1, y1 = (event.x - int(EraserSize.get())), (event.y - int(EraserSize.get()))
    x2, y2 = (event.x + int(EraserSize.get())), (event.y + int(EraserSize.get()))
    canvas.create_oval(x1, y1, x2, y2, fill=python_green,outline=python_green)
    canvas.draw.ellipse(((x1, y1, x2, y2)), fill=python_green, outline=python_green)
def setColor():
    global color
    color= askcolor()
def entry_text(event):
        canvas.entry = Entry(canvas, bd=0, font=("Purisa", 10))
        canvas.entry.place(x=event.x, y=event.y)
def ontext_button():
        print(canvas.entry.get())
        outstring = canvas.entry.get()
        canvas.draw.text((20,20), outstring,fill="black")
LINE, RECTANGLE,CIRCLE,POLYGON,TEXT,BRUSH,ERASER= list(range(7))
class Paint:
    def __init__(self, canvas):
        self.canvas = canvas
        self._tool, self._obj = None, None
        self.lastx, self.lasty = None, None
        self.canvas.bind('<Button-1>', self.update_xy)
        self.canvas.bind('<ButtonRelease-1>', self.draw)
        self.canvas.image = Image.new("RGB", (500, 500), (255, 255, 255))
        self.canvas.draw = ImageDraw.Draw(self.canvas.image)
        self.value_of_combo = 'X'
        self.combo()
    def newselection(self, event):
        self.value_of_combo = self.box.get()
        if self.value_of_combo == 'JPEG':
            self.canvas.image.save('D:my_drawingh.jpg', 'JPEG')
        elif self.value_of_combo == 'PNG':
            self.canvas.image.save('D:/my_drawingh.png', 'PNG')
        elif self.value_of_combo== 'GIF':
            self.canvas.image.save('D:/my_drawingh.gif', 'GIF')
        elif self.value_of_combo== 'BMP':
            self.canvas.image.save('D:/my_drawingh.bmp', 'BMP')
    def combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.canvas, textvariable=self.box_value,width=50)
        self.box['values'] = ('JPEG', 'PNG', 'GIF','BMP')
        self.box.current(0)
        self.box.grid(column=0, row=0)
        self.box.bind("<<ComboboxSelected>>", self.newselection)
    def draw(self, event):
        if self._tool is None or self._obj is None:
            return
        x, y = self.lastx, self.lasty
        x1, y1 = event.x, event.y
        if self._tool in (LINE, RECTANGLE,CIRCLE):
            self.canvas.coords(self._obj, (x, y, x1, y1))
            if self._tool == LINE:
                self.canvas.draw.line(((x, y, x1, y1)), fill=color[1], width=3)
            elif self._tool == RECTANGLE:
                self.canvas.draw.rectangle(((x, y, x1, y1)), fill=color[1],outline=color[1])
            elif self._tool == CIRCLE:
                self.canvas.draw.ellipse(((x, y, x1, y1)), fill=color[1],outline=color[1])
        elif self._tool == POLYGON:
            self.canvas.coords(self._obj, (x, y, x1, x1, y1, y1))
            if self._tool == POLYGON:
                self.canvas.draw.polygon((x, y, x1, x1, y1, y1), fill=color[1], outline=color[1])
    def update_xy(self, event):
        if self._tool is None:
            return
        x, y = event.x, event.y
        if self._tool == LINE:
            self._obj = self.canvas.create_line((x, y, x, y),fill=color[1])
            self.canvas.unbind("<B1-Motion>")
        elif self._tool == RECTANGLE:
            self._obj = self.canvas.create_rectangle((x, y, x, y),fill=color[1],outline=color[1])
            self.canvas.unbind("<B1-Motion>")
        elif self._tool == CIRCLE:
            self._obj = self.canvas.create_oval((x, y, x, y),fill=color[1],outline=color[1])
            self.canvas.unbind("<B1-Motion>")
        elif self._tool == POLYGON:
            self._obj = self.canvas.create_polygon((x, y, x, x, y, y), fill=color[1], outline=color[1])
            self.canvas.unbind("<B1-Motion>")
        elif self._tool == TEXT:
            self._obj = self.canvas.bind("<Double-Button-1>",entry_text)
            self.canvas.unbind("<B1-Motion>")
        elif self._tool == BRUSH:
            self._obj =self.canvas.bind("<B1-Motion> ", brush)
        elif self._tool == ERASER:
            self._obj = self.canvas.bind("<B1-Motion> ", eraser)
        self.lastx, self.lasty = x, y
    def select_tool(self, tool):
        print('Tool', tool)
        self._tool = tool
class  Tool:
    def __init__(self, whiteboard, parent=None):
        self.whiteboard = whiteboard
        frame = Frame(parent)
        self._curr_tool = None
        for i, (text, t) in enumerate((('LINE', LINE), ('RECTANGLE', RECTANGLE),('CIRCLE', CIRCLE),('TRAINGLE', POLYGON),('TEXT',TEXT),('BRUSH',BRUSH),('ERASER',ERASER))):
            lbl = Label(frame,text=text, width=10, relief='raised')
            lbl._tool = t
            lbl.bind('<Button-1>', self.update_tool)
            lbl.pack(padx=6, pady=40*(i % 2))
        frame.pack(side='left', fill='y',pady=150)
    def update_tool(self, event):
        lbl = event.widget
        if self._curr_tool:
            self._curr_tool['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        self._curr_tool = lbl
        self.whiteboard.select_tool(lbl._tool)
root = Tk()
canvas = Canvas(highlightbackground='black',bg="white")
whiteboard = Paint(canvas)
tool = Tool(whiteboard)
canvas.pack(fill='both', expand=True, padx=20, pady=6)
label = Label(root, text="enter brush size ")
label.pack()
BrushSize = Entry(root)
BrushSize.pack()
label2 = Label(root, text="enter eraser size ")
label2.pack()
EraserSize = Entry(root)
EraserSize.pack()
push = Button(text='Select Color', command=setColor).pack()
button =Button(text="confirm text", command=ontext_button).pack()
mainloop()