import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from tkinter import simpledialog
from PIL import Image, ImageDraw, ImageFont


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
        self.canvas.bind("<Button-1>", self.add_text)  # Добавляем обработчик для добавления текста

    def change_background(self):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            self.canvas.config(bg=new_color)
            self.image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), new_color)
            self.draw = ImageDraw.Draw(self.image)

    def ask_for_text(self):
        user_input = simpledialog.askstring("Введите текст", "Введите текст, который вы хотите добавить:")
        if user_input:
            self.text = user_input
            self.awaiting_text_input = True  # Устанавливаем флаг, ожидающий добавление текста

    def add_text(self, event):
        if self.awaiting_text_input:  # Проверяем, установлен ли флаг
            x, y = event.x, event.y
            font = ImageFont.load_default()  # Используем стандартный шрифт
            self.draw.text((x, y), self.text, fill=self.pen_color, font=font)
            self.canvas.create_text((x, y), text=self.text, fill=self.pen_color, anchor='nw')
            self.awaiting_text_input = False  # Сбрасываем флаг после добавления текста

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

        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT)

        change_bg_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background)
        change_bg_button.pack(side=tk.LEFT)

        text_button = tk.Button(control_frame, text="Текст", command=self.ask_for_text)
        text_button.pack(side=tk.LEFT)

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

    def resize_canvas(self):
        width = simpledialog.askinteger("Размер холста", "Введите новую ширину:", minvalue=1)
        height = simpledialog.askinteger("Размер холста", "Введите новую высоту:", minvalue=1)

        if width and height:  # Проверяем, получили ли валидные значения
            # Создаем новый холст и обновляем объект Image
            self.image = Image.new("RGB", (width, height), "white")
            self.draw = ImageDraw.Draw(self.image)

            # Обновляем размеры холста
            self.canvas.config(width=width, height=height)
            self.canvas.delete("all")  # Очищаем холст

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
