import tkinter as tk
from ui_playerview import PlayerViewer
from urllib.request import urlopen
from PIL import Image, ImageTk
from ui_styles import colour, font
from examples import ***REMOVED***, ***REMOVED***

player_list = [***REMOVED***, ***REMOVED***]

root_main = tk.Tk()
root_main.title("RATS.EXE")
root_main.config(bg=colour.bg_low, padx=10, pady=10)

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

# ============ Player List ======================================

player_list_base = tk.Frame(
    root_main,
    bg="green"
)
player_list_canvas = tk.Canvas(
    player_list_base,
    bg="red",
    borderwidth=0,
    highlightthickness=0,
    width=200,
    height=5
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
        scrollregion=player_list_canvas.bbox("all")
    )
)

player_list_canvas.create_window(
    (0, 0), window=player_list_scrollable_frame, anchor="nw")

player_list_canvas.configure(yscrollcommand=player_list_scrollbar.set)

player_list_base.grid(column=1, row=2, rowspan=9, stick="nesw")
player_list_canvas.pack(side="left", fill="both", expand=False)
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

    player_button = tk.Button(
        player_list_scrollable_frame,
        text=" "+"123456789012345678901234567890123456789012"+" ",
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
    player_button.pack(side="top", fill="both", expand=True)
    player_button.imgref = img


def ViewPlayer(player):
    PlayerViewer(player)


add_player(***REMOVED***)
add_player(***REMOVED***)

root_main.mainloop()
