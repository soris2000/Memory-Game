import flet as ft
import random
from time import sleep
from counter import *

items = 0
card_1 = -1
card_2 = -1
correct_pairs = 0
dificulty = ""
panel = ft.GridView()
counter = Counter()


def main(page: ft.Page):
    page.title = "Memory Game"
    page.window_width = 800
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    
    def get_panel():
        global items
        global dificulty

        if dificulty == "easy":
            items = 6
            width_item = 200
        elif dificulty == "medium":
            items = 12
            width_item = 150
        else:
            items = 20
            width_item = 100

        gv = ft.GridView(
            width=500,
            height=500,
            expand=0,
            max_extent=width_item,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
        )
        for i in range(items):
            gv.controls.append(
                ft.Container(
                    key=i,
                    padding=5,
                    image_src="assets/card.png",
                    image_fit=ft.ImageFit.CONTAIN,
                    on_click=flip_card,
                    bgcolor=ft.colors.ON_PRIMARY,
                    border_radius=10,
                ),
            )
        return gv
  
    def on_hover(e):
        e.control.bgcolor = "teal" if e.data == "true" else "pink"
        e.control.update()

    def close_dlg(e):
        dlg_startgame.open = False
        dlg_startgame.update()
        counter.start()
        page.update()

    def check_match():
        global panel
        global correct_pairs
        global items
        global card_1
        global card_2
        if panel.controls[card_1].data != panel.controls[card_2].data:
            # Match
            panel.controls[card_1].disabled = False
            panel.controls[card_2].disabled = False
            page.update()
        else:
            # No Match
            correct_pairs += 1
            panel.controls[card_1].bgcolor = "green"
            panel.controls[card_2].bgcolor = "green"
            page.update()

        if correct_pairs == int(items / 2):
            # Game Over
            counter.stop()
            page.dialog = dlg_endgame
            mins, secs = divmod(counter.seconds, 60)
            time = "{:02d}:{:02d}".format(mins, secs)
            dlg_endgame.content.value = f"Time: {time}"
            dlg_endgame.open = True
            page.update()
            return

        for i in range(items):
            if panel.controls[i].disabled == False:
                panel.controls[i].image_src = f"assets/card.png"
                panel.controls[i].bgcolor = ft.colors.ON_PRIMARY

        card_1 = -1
        card_2 = -1
        page.update()

    def flip_card(e):
        global card_1
        global card_2
        e.control.image_src = f"assets/{e.control.data}.png"
        e.control.disabled = True
        e.control.bgcolor = ft.colors.WHITE
        e.control.update()
        sleep(0.5)
        if card_1 == -1:
            card_1 = e.control.key
        else:
            card_2 = e.control.key
            check_match()

    def new_game(e):
        global card_1
        global card_2
        global correct_pairs
        correct_pairs = 0
        card_1 = -1
        card_2 = -1
        dlg_endgame.open = False
        counter.reset()
        page.update()
        page.controls.clear()
        home()
    
    def start_game(e):
        global items
        global dificulty
        global panel

        page.controls.clear()
        dificulty = select_dificulty.value
        panel = get_panel()
        page.add(
            ft.Container(
                width=800,
                height=700,
                image_src="assets/background.png",
                image_fit=ft.ImageFit.FILL,
                content=ft.Column(
                    [
                        title,
                        ft.Container(height=20),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Time", size=30),
                                        ft.Container(
                                            border=ft.border.all(3, "white54"),
                                            border_radius=5,
                                            width=150,
                                            height=70,
                                            content=counter,
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Image(
                                            src="assets/pig.png",
                                            width=200,
                                            height=200,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                panel,
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        )

        animals = [
            "bee",
            "dolphin",
            "elephant",
            "fish",
            "monkey",
            "penguin",
            "cat",
            "cow",
            "turtle",
            "frog",
        ]
        cards = []
        for i in range(int(items / 2)):
            animal = random.choice(animals)
            animals.remove(animal)
            cards.append(animal)

        list_cards = cards * 2
        random.shuffle(list_cards)
       
        for i in range(items):
            panel.controls[i].data = list_cards[i]

        # Show tutorial
        page.dialog = dlg_startgame
        dlg_startgame.open = True
        page.update()

    def home():
        page.add(
            ft.Container(
                width=800,
                height=700,
                image_src="assets/background.png",
                image_fit=ft.ImageFit.FILL,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=300,
                    height=300,
                    border_radius=10,
                    border=ft.border.all(3, "white54"),
                    content=ft.Column(
                        [
                            ft.Text("Memory Game", size=30, weight=ft.FontWeight.BOLD),
                            ft.Text("Select dificulty:"),
                            select_dificulty,
                            ft.Container(
                                on_click=start_game,
                                on_hover=on_hover,
                                width=100,
                                height=50,
                                bgcolor=ft.colors.PINK,
                                border_radius=10,
                                content=ft.Text("Play", size=20),
                                border=ft.border.all(3, "white54"),
                                alignment=ft.alignment.center,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
            )
        )
        page.update()

 
    # UI Game
    select_dificulty = ft.RadioGroup(
        content=ft.Column(
            width=150,
            controls=[
                ft.Radio(value="easy", label="Easy"),
                ft.Radio(value="medium", label="Medium"),
                ft.Radio(value="hard", label="Hard"),
            ],
        )
    )

    title = ft.Text("Memory Game", size=50, text_align=ft.TextAlign.CENTER)
    dlg_startgame = ft.AlertDialog(
        modal=True,
        title=ft.Text(value="How to play", text_align=ft.TextAlign.CENTER),
        content=ft.Image(src="assets/Tutorial.png", width=300, height=200),
        actions=[
            ft.TextButton("Ok", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    dlg_endgame = ft.AlertDialog(
        modal=True,
        title=ft.Text(value="Game Over", text_align=ft.TextAlign.CENTER),
        content=ft.Text(value="", text_align=ft.TextAlign.CENTER),
        actions=[
            ft.TextButton("New Game", on_click=new_game),
            ft.TextButton("Exit", on_click=lambda e: page.window_destroy()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Load Home
    home()


if __name__ == "__main__":
    ft.app(target=main)
