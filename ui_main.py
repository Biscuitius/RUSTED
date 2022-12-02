import tkinter as tk
from ui_playerview import PlayerViewer
from urllib.request import urlopen
from PIL import Image, ImageTk
from ui_styles import colour, font
from examples import player_list

root_main = tk.Tk()
root_main.title("RATS.EXE")
root_main.config(bg=colour.bg_low, padx=10, pady=10)
root_main.resizable(False, False)

root_main.grid_columnconfigure(0, weight=1)
root_main.grid_columnconfigure(1, weight=2)

root_main.grid_rowconfigure(1, weight=1)
root_main.grid_rowconfigure(2, weight=1)
root_main.grid_rowconfigure(3, weight=1)
root_main.grid_rowconfigure(4, weight=1)
root_main.grid_rowconfigure(5, weight=1)
root_main.grid_rowconfigure(6, weight=1)
root_main.grid_rowconfigure(7, weight=1)
root_main.grid_rowconfigure(8, weight=1)
root_main.grid_rowconfigure(9, weight=1)
root_main.grid_rowconfigure(10, weight=1)

tk.Label(
    root_main,
    bg=colour.bg_mid,
    text="  Rust Advanced Tracking System  ",
    font=(font.medium, 20),
    fg=colour.txt_title
).grid(
    column=0,
    row=0,
    columnspan=3,
    stick="nesw"
)

# ============ Leaderboard ======================================


# ============ Player List ======================================

player_list_base = tk.Frame(
    root_main,
    bg="green"
)
player_list_canvas = tk.Canvas(
    player_list_base,
    bg=colour.bg_low,
    borderwidth=0,
    highlightthickness=0,
    width=1,
    height=1
)

player_list_scrollbar = tk.Scrollbar(
    player_list_base,
    orient="vertical",
    command=player_list_canvas.yview
)

player_list_scrollable_frame = tk.Frame(player_list_canvas)

player_list_scrollable_frame.bind(
    "<Configure>",
    lambda e: player_list_canvas.configure(
        scrollregion=player_list_canvas.bbox("all"),
        width=player_list_scrollable_frame.winfo_width()
    )
)

player_list_canvas.create_window(
    (0, 0), window=player_list_scrollable_frame, anchor="nw")

player_list_canvas.configure(yscrollcommand=player_list_scrollbar.set)

player_list_canvas.bind(
    "<Configure>",
    lambda e: player_list_scrollable_frame.configure(
        width=player_list_canvas.winfo_width()
    )
)

player_list_base.grid(column=1, row=2, rowspan=9, stick="nesw")
player_list_canvas.pack(side="left", fill="both", expand=True)
player_list_scrollbar.pack(side="right", fill="y", expand=False)

tk.Label(
    root_main,
    text="Players",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high
).grid(column=1, row=1, stick="nesw")


def add_player(player):

    try:
        img = urlopen(player.avatarsmall)
        img = ImageTk.PhotoImage(data=img.read())

    except:
        img = Image.open("./icons/blank_small.jpg")
        img = ImageTk.PhotoImage(img)

    label = tk.Button(
        player_list_scrollable_frame,
        text=" "+player.name+" ",
        font=(font.medium, 12),
        relief="flat",
        bg=colour.btn,
        activebackground=colour.btn_click,
        fg=colour.txt_title,
        image=img,
        anchor="w",
        compound="left",
        command=lambda: ViewPlayer(player)
    )
    label.pack(fill="both")
    label.imgref = img


def ViewPlayer(player):
    PlayerViewer(player)


for player in player_list:
    add_player(player)

root_main.mainloop()
