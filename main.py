import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.pen_color = 'black'  # Инициализация цвета кисти
        self.setup_ui()  # Настройка интерфейса

        self.last_x, self.last_y = None, None

        # Обработка событий
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind("<Button-3>", self.pipette)
        self.root.bind("<Control-s>", self.save_image)
        self.root.bind("<Control-c>", self.choose_color)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        eraser = tk.Button(control_frame, text="Ластик", command=self.choose_eraser)
        eraser.pack(side=tk.LEFT)

        # Виджет для "предварительного просмотра" цвета кисти
        self.color_preview = tk.Label(control_frame, width=5, height=1, bg=self.pen_color)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        self.brush_size_var = tk.IntVar(value=1)
        sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.brush_size_scale_list = tk.OptionMenu(control_frame, self.brush_size_var, *sizes,
                                                   command=self.update_brush_size)
        self.brush_size_scale_list.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
            brush_size = self.brush_size_var.get()
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=brush_size)
        self.last_x = event.x
        self.last_y = event.y

    def update_brush_size(self, value):
        self.brush_size = int(value)  # Обновляет текущий размер кисти

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        color = colorchooser.askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.color_preview.config(bg=self.pen_color)  # Обновляем цвет предварительного просмотра

    def choose_eraser(self):
        self.pen_color = 'white'  # Цвет ластика
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет предварительного просмотра

    def pipette(self, event):
        x, y = event.x, event.y
        color = self.image.getpixel((x, y))  # Получаем цвет пикселя
        self.pen_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет предварительного просмотра

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

