# 8x8 Matrix Pattern Generator
# A GUI tool which generates patterns for MAX7219 8x8 LED Dot Matrix Display.
# Author - Abhishek Kumar

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageDraw

def binary_to_hex(binary):
    decimal_value = int(binary, 2)
    return f"0x{decimal_value:02X}"

def update_hex_code(event):
    x, y = event.x // box_size, event.y // box_size
    if (x, y) not in selected_boxes:
        selected_boxes.append((x, y))
        pixels[y][x] = 1
        canvas.itemconfig(rectangles[y][x], fill="#E3242B")
    else:
        selected_boxes.remove((x, y))
        pixels[y][x] = 0
        canvas.itemconfig(rectangles[y][x], fill="#03C04A")

def generate_hex_code():
    hex_values = []
    binary_values = []
    for y in range(matrix_size):
        row_binary = ''.join('1' if pixels[y][x] else '0' for x in range(matrix_size))
        binary_values.append(row_binary)
        hex_values.append(binary_to_hex(row_binary))
    binary_code.delete("1.0", tk.END)
    binary_code.insert(tk.END, "\n".join(binary_values))

    hex_code_label.delete("1.0", tk.END)
    hex_code_label.insert(tk.END, ", ".join(hex_values))

def clear_selected_pixels():
    for y in range(matrix_size):
        for x in range(matrix_size):
            pixels[y][x] = 0
            canvas.itemconfig(rectangles[y][x], fill="#03C04A")
    selected_boxes.clear()
    clear_canvas()

def create_pixels_matrix(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def draw_pixels(canvas, pixels):
    rectangles = []
    for y in range(len(pixels)):
        row = []
        for x in range(len(pixels[y])):
            rect = canvas.create_rectangle(x * box_size, y * box_size,
                                           (x + 1) * box_size, (y + 1) * box_size,
                                           fill="#03C04A", outline="black")
            row.append(rect)
        rectangles.append(row)
    return rectangles

def clear_canvas():
    binary_code.delete("1.0", tk.END)
    hex_code_label.delete("1.0", tk.END)

def fill_boxes():
    for y in range(matrix_size):
        for x in range(matrix_size):
            pixels[y][x] = 1
            canvas.itemconfig(rectangles[y][x], fill="#E3242B")
    hex_code_label.config()
    generate_hex_code()

def copy_hex_to_clipboard(root):
    hex_values = []
    for y in range(matrix_size):
        row_binary = ''.join('1' if pixels[y][x] else '0' for x in range(matrix_size))
        hex_values.append(binary_to_hex(row_binary))

    hex_string = ', '.join(hex_values)
    root.clipboard_clear()
    root.clipboard_append(hex_string)

def copy_bin_to_clipboard(root):
    binary_values = []
    for y in range(matrix_size):
        row_binary = ''.join('1' if pixels[y][x] else '0' for x in range(matrix_size))
        binary_values.append(row_binary)

    binary_string = '\n'.join(binary_values)
    root.clipboard_clear()
    root.clipboard_append(binary_string)

def save_codes_to_file():
    file_path = filedialog.asksaveasfilename(filetypes=[('Matrix Codes', '*.txt')], defaultextension='.txt')
    if not file_path:
        return
    with open(file_path, 'w') as file:
        file.write("-------------|B|I|N|A|R|Y|-------------\n")
        file.write(binary_code.get(1.0, tk.END))
        file.write("-------------|H|E|X|A|D|E|C|I|M|A|L|-------------\n")
        file.write(hex_code_label.get(1.0, tk.END))

def exit_window():
    root.destroy()

def save_image():
    file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')], defaultextension='.png')
    if not file_path:
        return

    red = (255, 0, 0)
    lime_green = (50, 205, 50)
    black = (0, 0, 0)

    image = Image.new('RGB', (box_size * matrix_size, box_size * matrix_size), color='white')
    draw = ImageDraw.Draw(image)

    for y in range(matrix_size + 1):
        draw.line([(0, y * box_size), (box_size * matrix_size, y * box_size)], fill=black, width=2)

    for x in range(matrix_size + 1):
        draw.line([(x * box_size, 0), (x * box_size, box_size * matrix_size)], fill=black, width=2)

    for y in range(matrix_size):
        for x in range(matrix_size):
            color = "#E3242B" if pixels[y][x] else "#03C04A"
            left = x * box_size + 2
            top = y * box_size + 2
            right = left + box_size - 2
            bottom = top + box_size - 2
            draw.rectangle([left, top, right, bottom], fill=color)

    image.save(file_path)

box_size = 40
matrix_size = 8

global pixels, hex_code_label, canvas, rectangles, selected_boxes

pixels = create_pixels_matrix(matrix_size)
selected_boxes = []
root = tk.Tk()
root.title("8x8 Matrix Pattern Generator")
root.geometry("820x415")
root.resizable(0,0)

frame = tk.Frame(root, width=800, height=800, bg="lightblue")
frame.place(x=10, y=13)
canvas = tk.Canvas(frame, width=box_size * matrix_size, height=box_size * matrix_size)
canvas.pack(padx=10, pady=10)
rectangles = draw_pixels(canvas, pixels)

frame1 = tk.Frame(root, width=425, height=200, bg="lightblue")
frame1.place(x=380, y=13)
binary_text = tk.Label(frame1, text="BINARY", font='arial 12', bg="lightblue")
binary_text.place(x=190, y=10)
binary_code = tk.Text(frame1, height=8, width=50)
binary_code.place(x=10, y=40)

frame2 = tk.Frame(root, width=425, height=110, bg="lightblue")
frame2.place(x=380, y=247)
hex_text = tk.Label(frame2, text="HEXADECIMAL", font='arial 12', bg="lightblue")
hex_text.place(x=165, y=10)
hex_code_label = tk.Text(frame2, height=2, width=50)
hex_code_label.place(x=10, y=50)

button_frame = ttk.Frame(root, width=800, height=50, padding=(5, 5, 5, 5))
button_frame.pack(side="bottom",fill="x")

generate_button = ttk.Button(button_frame, text="GENERATE", command=generate_hex_code)
generate_button.pack(side="left", padx=5, pady=5)

fill_button = ttk.Button(button_frame, text="FILL", command=fill_boxes)
fill_button.pack(side="left", padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="CLEAR", command=clear_selected_pixels)
clear_button.pack(side="left", padx=5, pady=5)

exit_button = ttk.Button(button_frame, text="EXIT", command=exit_window)
exit_button.pack(side="right", padx=5, pady=5)

savecode_button = ttk.Button(button_frame, text="SAVE CODE", command=save_codes_to_file)
savecode_button.pack(side="right", padx=5, pady=5)

saveimg_button = ttk.Button(button_frame, text="SAVE IMAGE", command=save_image)
saveimg_button.pack(side="right", padx=5, pady=5)

copyhex_button = ttk.Button(button_frame, text="COPY HEX", command=lambda: copy_hex_to_clipboard(root))
copyhex_button.pack(side="right", padx=5, pady=5)

copybin_button = ttk.Button(button_frame, text="COPY BIN", command=lambda: copy_bin_to_clipboard(root))
copybin_button.pack(side="right", padx=5, pady=5)

canvas.bind("<Button-1>", update_hex_code)

root.mainloop()