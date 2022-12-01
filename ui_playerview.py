import tkinter as tk
import webbrowser
from urllib.request import urlopen
from ui_styles import colour, font
from PIL import ImageTk, Image


class PlayerViewer:

    def __init__(self, player):

        self.root = tk.Toplevel()
        self.root.title(player.name)
        self.root.focus_force()
        self.root.config(bg=colour.bg_low, padx=10, pady=10)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_rowconfigure(9, weight=1)
        self.root.grid_rowconfigure(10, weight=1)
        self.root.grid_rowconfigure(11, weight=1)
        self.root.grid_rowconfigure(12, weight=1)

        try:
            img = urlopen(player.avatarmedium)
            img = ImageTk.PhotoImage(data=img.read())

        except:
            img = Image.open("./icons/blank_medium.jpg")
            img = ImageTk.PhotoImage(img)

        player_title = tk.Label(
            self.root,
            bg=colour.bg_high,
            text="  " + player.name + "  ",
            image=img,
            compound="left",
            font=(font.semibold, 26),
            fg=colour.txt_title
        )

        player_title.grid(
            column=0,
            row=0,
            columnspan=5,
            stick="nesw",
        )

        player_title.imgref = img

# ============ Player Info ======================================

        tk.Label(
            self.root,
            text="Steam ID",
            fg=colour.txt_title,
            font=(font.medium, 16),
            bg=colour.bg_high
        ).grid(column=0, row=1, stick="nesw")

        steamid_label = tk.Label(
            self.root,
            text=player.steamid,
            fg=colour.txt_title,
            font=(font.medium, 12),
            bg=colour.bg_mid
        )
        steamid_label.grid(column=0, row=2, stick="nesw")

        tk.Label(
            self.root,
            text="Profile URL",
            fg=colour.txt_title,
            font=(font.medium, 16),
            bg=colour.bg_high
        ).grid(column=0, row=3, stick="nesw")

        def callback(url):
            webbrowser.open_new_tab(url)

        url_label = tk.Label(
            self.root,
            text="Open in Web",
            fg="#0000EE",
            font=(font.medium, 12, "underline"),
            bg=colour.bg_mid
        )
        url_label.grid(column=0, row=4, stick="nesw")
        url_label.bind("<Button-1>", lambda e:
                       callback(player.url))

        tk.Label(
            self.root,
            text="Profile State",
            fg=colour.txt_title,
            font=(font.medium, 16),
            bg=colour.bg_high
        ).grid(column=0, row=5, stick="nesw")

        visibility_label = tk.Label(
            self.root,
            fg=colour.txt_title,
            font=(font.medium, 12),
            bg=colour.bg_mid
        )
        visibility_label.grid(column=0, row=6, stick="nesw")

        if player.visibility == 1:
            visibility_label.config(text="Private")
        else:
            visibility_label.config(text="Public")

        if player.visibility != 1:

            tk.Label(
                self.root,
                text="Online",
                fg=colour.txt_title,
                font=(font.medium, 16),
                bg=colour.bg_high,
                height=1
            ).grid(column=0, row=7, stick="nesw")

            onlinestate_label = tk.Label(
                self.root,
                fg=colour.txt_title,
                font=(font.medium, 12),
                bg=colour.bg_mid,
                height=1
            )
            onlinestate_label.grid(column=0, row=8, stick="nesw")

            if player.onlinestate == 0:
                onlinestate_label.config(text="Offline")
            else:
                onlinestate_label.config(text="Online")

            tk.Label(
                self.root,
                text="Total Hours",
                fg=colour.txt_title,
                font=(font.medium, 16),
                bg=colour.bg_high,
                height=1
            ).grid(column=0, row=9, stick="nesw")

            hours_label = tk.Label(
                self.root,
                text="PLACEHOLDER",
                fg=colour.txt_title,
                font=(font.medium, 12),
                bg=colour.bg_mid,
                height=1
            )
            hours_label.grid(column=0, row=10, stick="nesw")

            if player.bmid:
                tk.Label(
                    self.root,
                    text="BatMet ID",
                    fg=colour.txt_title,
                    font=(font.medium, 16),
                    bg=colour.bg_high,
                    height=1
                ).grid(column=0, row=11, stick="nesw")

                hours_label = tk.Label(
                    self.root,
                    text=player.bmid,
                    fg=colour.txt_title,
                    font=(font.medium, 12),
                    bg=colour.bg_mid,
                    height=1
                )
                hours_label.grid(column=0, row=12, stick="nesw")

# ============ Player Notes =====================================

        tk.Label(
            self.root,
            text="Player Notes",
            fg=colour.txt_title,
            font=(font.medium, 16),
            bg=colour.bg_high
        ).grid(column=1, row=1, stick="nesw")

        notes_box = tk.Text(
            self.root,
            fg=colour.txt_title,
            font=(font.medium, 12),
            bg=colour.bg_mid,
            exportselection=0,
            wrap="word",
            width=24
        )
        notes_box.grid(column=1, row=2, rowspan=100, stick="nesw")

# ============ Player Session Info ==============================

        tk.Label(
            self.root,
            text="Player Sessions",
            fg=colour.txt_title,
            font=(font.medium, 16),
            bg=colour.bg_high
        ).grid(column=2, row=1, stick="nesw")

# ============ Player Stats =====================================

        tk.Label(
            self.root,
            text="Player Stats",
            fg=colour.txt_title,
            font=(font.medium, 16),
            bg=colour.bg_high
        ).grid(column=3, row=1, columnspan=2, stick="nesw")

        stats_scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical"
        )
        stats_scrollbar.grid(column=4, row=2, rowspan=11, stick="ns")

        stats_box = tk.Text(
            self.root,
            bg=colour.bg_mid,
            yscrollcommand=stats_scrollbar.set,
            fg=colour.txt_title,
            font=(font.medium, 14),
            width=22
        )
        stats_box.grid(column=3, row=2, rowspan=100, stick="nesw")

        stats_scrollbar.config(command=stats_box.yview)

        for stat in player.stats:
            stats_box.insert("end", stat+":\n"+player.stats[stat]+"\n\n")

        stats_box.delete("end-3c")
