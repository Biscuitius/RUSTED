import tkinter as tk
from ui_playerview import PlayerViewer
from urllib.request import urlopen
from PIL import Image, ImageTk
from ui_styles import colour, font
from examples import tyler, matt

player_list = [tyler, matt]

root_main = tk.Tk()
root_main.title("RATS.EXE")
root_main.config(bg=colour.bg_low, padx=10, pady=10)

root_main.grid_columnconfigure(0, weight=1)
root_main.grid_columnconfigure(1, weight=1)

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

# ============ Server Stats =====================================

tk.Label(
    root_main,
    text="Server Name",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high
).grid(column=0, row=1, stick="nesw")

server_name_label = tk.Label(
    root_main,
    text="PLACEHOLDER",
    fg=colour.txt_title,
    font=(font.medium, 12),
    bg=colour.bg_mid,
    height=1
)
server_name_label.grid(column=0, row=2, stick="nesw")

tk.Label(
    root_main,
    text="Server IP",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high,
    height=1
).grid(column=0, row=3, stick="nesw")

server_ip_label = tk.Label(
    root_main,
    text="PLACEHOLDER",
    fg=colour.txt_title,
    font=(font.medium, 12),
    bg=colour.bg_mid,
    height=1
)
server_ip_label.grid(column=0, row=4, stick="nesw")

tk.Label(
    root_main,
    text="Player Count",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high,
    height=1
).grid(column=0, row=5, stick="nesw")

player_count_label = tk.Label(
    root_main,
    text="PLACEHOLDER",
    fg=colour.txt_title,
    font=(font.medium, 12),
    bg=colour.bg_mid,
    height=1
)
player_count_label.grid(column=0, row=6, stick="nesw")

tk.Label(
    root_main,
    text="Server Uptime",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high,
    height=1
).grid(column=0, row=7, stick="nesw")

server_uptime_label = tk.Label(
    root_main,
    text="PLACEHOLDER",
    fg=colour.txt_title,
    font=(font.medium, 12),
    bg=colour.bg_mid,
    height=1
)
server_uptime_label.grid(column=0, row=8, stick="nesw")

tk.Label(
    root_main,
    text="Server Map",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high,
    height=1
).grid(column=0, row=9, stick="nesw")

server_map_label = tk.Label(
    root_main,
    text="PLACEHOLDER",
    fg=colour.txt_title,
    font=(font.medium, 12),
    bg=colour.bg_mid
)
server_map_label.grid(column=0, row=10, stick="nesw")

# ============ SCROLL List ======================================

container = tk.Frame(root_main)
canvas = tk.Canvas(container)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

for i in range(50):
    tk.Label(scrollable_frame, text="Sample scrolling label").pack()

container.grid(column=3, row=1)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ============ Player List ======================================

tk.Label(
    root_main,
    text="Players",
    fg=colour.txt_title,
    font=(font.medium, 16),
    bg=colour.bg_high
).grid(column=1, row=1, stick="nesw")

players_frame = tk.Frame(
    root_main,
    bg=colour.bg_mid
)

players_frame.grid(
    column=1,
    row=2,
    rowspan=100,
    stick="nesw"
)


def add_player(player):

    try:
        img = urlopen(player.avatarsmall)
        img = ImageTk.PhotoImage(data=img.read())

    except:
        img = Image.open("./icons/blank_small.jpg")
        img = ImageTk.PhotoImage(img)

    label = tk.Button(
        players_frame,
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


add_player(matt)
add_player(tyler)

root_main.mainloop()
