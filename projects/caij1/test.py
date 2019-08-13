
from tkinter import *


def main():
    root = Tk()

    w = Canvas(
        root,
        width=200,
        height=200,
        background="white"
    )
    w.pack()

    p1 = w.create_line(0, 100, 200, 100, fill='yellow')

    p2 = w.create_line(100, 0, 100, 200, fill='red', dash=(4, 4))

    p3 = w.create_rectangle(50, 50, 150, 150, fill='blue')

    b = Button(root, text='删除全部', command=(lambda x=ALL: w.delete(x)))
    b.pack()

    mainloop()


if __name__ == '__main__':
    main()