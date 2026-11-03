import tkinter as tk
from tkinter import filedialog, scrolledtext
import math
import random
import webbrowser
from PIL import Image, ImageTk


CX, CY = 380, 340
W_WIDTH, W_HEIGHT = 1200, 800
RADIUS = 330

SELECTED_ANIME = ""

ANIME_LIST = ["Лимонные девочки", "Маг Целитель"]

def get_anime_list_from_json(filepath : str) -> list[str]:
    ...

def open_file() -> None:
    file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=(("Текстовые файлы", "*.txt"), ("JSON файлы", "*.json*"), ("Все файлы", "*.*")))
    if file_path:
        global ANIME_LIST
        animes = []
    
        if ".txt" in file_path:
            for item in (open(file_path, "r", encoding='utf8')):
                if item:
                    animes.append(item.replace("\n",""))
        
        if ".json" in file_path:
            animes = get_anime_list_from_json(file_path)
            
        for anime in animes:
            AnimeList.insert(tk.END, anime+"\n")
            


def open_anime_page() -> None:
    if SELECTED_ANIME:    
        urlPart1 = "https://ru.yummyani.me/catalog?q="
        
        urlPart2 = "+".join(SELECTED_ANIME.translate(str.maketrans({",":"%2C","!":"%21","?":'%3F'})).split(" "))

        webbrowser.open(urlPart1+urlPart2)
    else:
        return
    

def generate_colors(num_colors):
    random.seed(42)
    return [f"#{random.randint(70, 230):02x}{random.randint(70, 230):02x}{random.randint(70, 230):02x}" for _ in range(num_colors)]

COLORS = generate_colors(len(ANIME_LIST))

main = tk.Tk()
main.title("Anime Wheel")
main.geometry(f"{1200}x{800}")
main.resizable(False, False)
main.config(background="#faf5f5")

rigth_panel = tk.Frame(main, width=400, height=W_HEIGHT,background="#e6e2e2")
rigth_panel.pack_propagate(False) 
rigth_panel.pack(fill='y',side='right',ipadx=15,ipady=15)

image = Image.open("open-file-icon.png")
image.thumbnail((50, 50))
icon = ImageTk.PhotoImage(image)

Label = tk.Label(rigth_panel, height=5, text="Запишите список в поле ниже (каждое аниме на отдельной строчке) или выберите файл (.txt/.json)", wraplength=390, justify="left", font=("Arial", 12, "bold"),bg='#e6e2e2')
Label.pack(anchor="center", side='top',pady=5,padx=5)


AnimeList = scrolledtext.ScrolledText(rigth_panel, width=380,height=37, )
AnimeList.pack(anchor='center', padx=10, pady=5,)

open_file_button = tk.Button(rigth_panel, width=53, height=53, image=icon, command= lambda: open_file())
open_file_button.image = icon
open_file_button.pack(anchor='se', side='right',pady=5,padx=5)

result_label = tk.Label(main, height=1, width=40,text="Казино ебаное, но аниме", bg="#faf5f5", font=("Arial", 24, "bold"))
result_label.pack(anchor='s', side='top', padx=10, pady=10)



def wheel_generator():
    global ANIME_LIST, COLORS
    anime_list = AnimeList.get(1.0,tk.END).strip()
    if anime_list == "\n" or not anime_list or anime_list == "":
        ANIME_LIST = ["Лимонные девочки", "Маг Целитель"]
    else:
        ANIME_LIST = []
        for anime in anime_list.split("\n"):
            if anime.strip(""):
                ANIME_LIST.append(anime.strip())
    COLORS = generate_colors(len(ANIME_LIST))
    
    app.draw_scene()

generate_wheel = tk.Button(main, height=1, width=20,text="Сгенерировать колесо",command= lambda: wheel_generator(), font=("Arial", 18, "bold"))
generate_wheel.pack(anchor='center')



GoToAnime = tk.Button(rigth_panel,text="Перейти на страницу аниме",width=330,height=2,command=lambda: open_anime_page(), font=("Arial", 14, "bold"),state="disabled")
GoToAnime.pack(anchor='sw',side='left',fill='x',padx=5,pady=5)


class FortuneWheelApp:
    global ANIME_LIST
    def __init__(self, root):
        self.root = root
        self.root.title("Anime Wheel")
        self.root.geometry(f"{W_WIDTH}x{W_HEIGHT}")
        self.root.configure(bg="#faf5f5")
        self.root.resizable(False, False)

        self.angle = 0.0
        self.speed = 0.0
        self.is_spinning = False

        self.canvas = tk.Canvas(root, width=800, height=720, bg="#faf5f5", highlightthickness=0)
        self.canvas.pack()

        self.draw_scene()

        self.canvas.bind("<Button-1>", self.check_button_click)

    def draw_scene(self):
        self.canvas.delete("all")
        num_items = len(ANIME_LIST)
        sector_angle = 360.0 / num_items

        for i in range(num_items):
            start_a = self.angle + (i * sector_angle)
            end_a = start_a + sector_angle

            self.canvas.create_arc(
                CX - RADIUS, CY - RADIUS, CX + RADIUS, CY + RADIUS,
                start=start_a, extent=sector_angle,
                fill=COLORS[i], outline="#1e1e1e", width=1
            )

            mid_a_rad = math.radians(start_a + sector_angle / 2.0)
            dist = RADIUS * 0.65
            tx = CX + dist * math.cos(mid_a_rad)
            ty = CY - dist * math.sin(mid_a_rad)

            display_angle = (start_a + sector_angle / 2.0) % 360
            if 90 < display_angle <= 270:
                text_rotation = int(display_angle + 180)
            else:
                text_rotation = int(display_angle)

            self.canvas.create_text(
                tx, ty, text=ANIME_LIST[i], fill="#000000",
                font=("Arial", 10, "bold"), angle=text_rotation, justify=tk.CENTER
            )

        arrow_x = CX + RADIUS
        self.canvas.create_polygon(
            arrow_x - 5, CY,
            arrow_x + 30, CY - 15,
            arrow_x + 30, CY + 15,
            fill="#e62828", outline="#000000", width=2
        )

        btn_radius = 60
        btn_fill = "#787878" if self.is_spinning else "#32965a"
        self.canvas.create_circle = lambda x, y, r, **kwargs: self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        
        self.canvas.create_circle(CX, CY, btn_radius, fill=btn_fill, outline="#141414", width=3, tags="spin_btn")
        self.canvas.create_text(CX, CY - 10, text="нажмите,", fill="#ffffff", font=("Arial", 12, "bold"), tags="spin_btn")
        self.canvas.create_text(CX, CY + 10, text="чтобы крутить", fill="#ffffff", font=("Arial", 12, "bold"), tags="spin_btn")

    def check_button_click(self, event):
        if self.is_spinning:
            return
        
        distance = math.hypot(event.x - CX, event.y - CY)
        if distance <= 60:
            self.is_spinning = True
            result_label.configure(text="Колесо крутится...", fg="#282828", bg="#faf5f5")
            self.speed = random.uniform(25.0, 40.0)
            self.animate()

    def animate(self):
        global SELECTED_ANIME
        if self.speed > 0:
            self.angle = (self.angle + self.speed) % 360
            self.speed -= 0.15
            self.draw_scene()
            self.root.after(4, self.animate)
        else:
            self.speed = 0.0
            self.is_spinning = False
            
            num_items = len(ANIME_LIST)
            sector_angle = 360.0 / num_items
            
            winning_index = int((360.0 - self.angle) / sector_angle) % num_items
            SELECTED_ANIME = ANIME_LIST[winning_index]
            
            GoToAnime.config(state="normal")
            
            result_label.configure(
                text=SELECTED_ANIME,
                fg="#32965a"
            )
            self.draw_scene()
            
app = FortuneWheelApp(main)

main.mainloop()
