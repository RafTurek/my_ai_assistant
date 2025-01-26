import tkinter as tk

# Function to update the display with clicked numbers or operators
def click_button(value):
    current = display.get()
    display.delete(0, tk.END)
    display.insert(tk.END, current + value)

# Function to perform operations and evaluate results
def evaluate():
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(tk.END, str(result))
    except Exception as e:
        display.delete(0, tk.END)
        display.insert(tk.END, "Error")

# Create the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("350x200")

# Display widget for user input and output
display = tk.Entry(root, width=16, font=('Arial', 18))
display.grid(row=0, columnspan=4)

# Create buttons for numbers and operators
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row_index = 1
column_index = 0

for button in buttons:
    tk.Button(root, text=button, width=5, height=2, command=lambda b=button: click_button(b)).grid(row=row_index, column=column_index)
    column_index += 1
    if column_index == 4:
        row_index += 1
        column_index = 0

# Create button for evaluating the expression
tk.Button(root, text='=', width=5, height=2, command=lambda: evaluate()).grid(row=row_index, columnspan=4)

root.mainloop()
