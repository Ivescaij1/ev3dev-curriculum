import tkinter
from tkinter import ttk
import sys


def main():

    root = tkinter.Tk()
    root.title("Game Control")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()  # only grid call that does NOT need a row and column

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: print("Forward button")
    root.bind('<Up>', lambda event: print("Forward key"))
    button1 = ttk.Button(root, text='output', command=lambda: print('printing to GUI'))
    button1.grid()

    textbox = tkinter.Text(root)
    textbox.grid(row=4, column=0, sticky='nsew')

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    def text_director(inputs):
        textbox.insert('insert', inputs)

    sys.stdout.write = text_director  # whenever sys.stdout.write is called, redirector is called.

    root.mainloop()


main()