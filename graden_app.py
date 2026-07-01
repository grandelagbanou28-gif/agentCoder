"""
Grden IA v3.0 - Application GUI Ultra Professionnelle
Interface moderne, élégante et performante
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import os
import subprocess
import threading
import time
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

APP_NAME = "Grden IA"
APP_VERSION = "3.0.0"
APP_SUBTITLE = "Intelligence Artificielle pour Développeurs"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Palette de couleurs premium
C = {
    "bg": "#0a0a12",
    "bg2": "#12121e",
    "bg3": "#1a1a2e",
    "bg4": "#222240",
    "card": "#16162a",
    "card_hover": "#1e1e38",
    "border": "#2a2a4a",
    "border_light": "#3a3a5a",
    "text": "#f0f0ff",
    "text2": "#9090b0",
    "text3": "#606080",
    "accent": "#6c5ce7",
    "accent2": "#a29bfe",
    "accent3": "#5a4bd1",
    "green": "#00d68f",
    "green2": "#00b377",
    "red": "#ff4757",
    "yellow": "#ffc048",
    "blue": "#339af0",
    "cyan": "#22d3ee",
    "orange": "#ff922b",
    "pink": "#f06595",
    "purple": "#9775fa",
    "gradient1": "#6c5ce7",
    "gradient2": "#a29bfe",
}

F = {
    "logo": ("Segoe UI", 36, "bold"),
    "title": ("Segoe UI", 24, "bold"),
    "h1": ("Segoe UI", 18, "bold"),
    "h2": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 12),
    "small": ("Segoe UI", 10),
    "tiny": ("Segoe UI", 9),
    "mono": ("Cascadia Code", 12),
    "mono_s": ("Cascadia Code", 10),
    "mono_t": ("Cascadia Code", 9),
}


class Splash(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.geometry("600x400")
        self.configure(fg_color=C["bg"])
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"+{x}+{y}")
        
        # Glow effect background
        bg = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        bg.pack(fill="both", expand=True)
        
        # Animated circles
        for i, (cx, cy, r, color) in enumerate([
            (0.3, 0.4, 80, C["bg3"]),
            (0.7, 0.6, 60, C["bg4"]),
            (0.5, 0.3, 100, C["bg2"]),
        ]):
            circle = ctk.CTkFrame(bg, fg_color=color, width=r, height=r, corner_radius=r//2)
            circle.place(relx=cx, rely=cy, anchor="center")
        
        # Logo
        logo = ctk.CTkFrame(bg, fg_color=C["accent"], width=90, height=90, corner_radius=24)
        logo.place(relx=0.5, rely=0.35, anchor="center")
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 40, "bold"), text_color="white").pack(expand=True)
        
        # Title
        ctk.CTkLabel(bg, text=APP_NAME, font=("Segoe UI", 32, "bold"),
                    text_color=C["text"]).place(relx=0.5, rely=0.55, anchor="center")
        ctk.CTkLabel(bg, text="v" + APP_VERSION, font=F["small"],
                    text_color=C["text2"]).place(relx=0.5, rely=0.63, anchor="center")
        
        # Progress
        self.progress = ctk.CTkProgressBar(bg, width=350, height=8,
                                           fg_color=C["bg3"], progress_color=C["accent"])
        self.progress.place(relx=0.5, rely=0.78, anchor="center")
        self.progress.set(0)
        
        self.status = ctk.CTkLabel(bg, text="Initialisation...", font=F["small"],
                                  text_color=C["text3"])
        self.status.place(relx=0.5, rely=0.86, anchor="center")
        
        self.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def update_progress(self, val, text="Chargement..."):
        self.progress.set(val)
        self.status.configure(text=text)
        self.update()


class GrdenIA(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(APP_NAME)
        self.geometry("1500x950")
        self.configure(fg_color=C["bg"])
        self.minsize(1100, 750)
        
        try:
            icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IAtrainer.ico")
            if os.path.exists(icon):
                self.iconbitmap(icon)
        except:
            pass
        
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.editor_file = None
        self.chat_history = []
        self.page_stack = []
        
        self.withdraw()
        self.show_splash()
    
    def show_splash(self):
        splash = Splash(self)
        
        def load():
            steps = [
                (0.1, "Chargement du noyau..."),
                (0.3, "Initialisation des modules..."),
                (0.5, "Chargement de l'interface..."),
                (0.7, "Préparation des outils..."),
                (0.9, "Finalisation..."),
                (1.0, "Prêt !"),
            ]
            for val, text in steps:
                splash.update_progress(val, text)
                time.sleep(0.15)
            
            splash.destroy()
            self.deiconify()
            self.build_ui()
        
        threading.Thread(target=load, daemon=True).start()
    
    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.build_sidebar()
        self.build_header()
        self.build_content()
        self.build_statusbar()
        
        self.show_home()
    
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=C["bg2"], width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo
        logo_box = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_box.pack(fill="x", padx=20, pady=(25, 5))
        
        logo = ctk.CTkFrame(logo_box, fg_color=C["accent"], width=48, height=48, corner_radius=14)
        logo.pack(side="left")
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 20, "bold"), text_color="white").pack(expand=True)
        
        name = ctk.CTkFrame(logo_box, fg_color="transparent")
        name.pack(side="left", padx=(14, 0))
        ctk.CTkLabel(name, text=APP_NAME, font=F["h2"], text_color=C["text"]).pack(anchor="w")
        ctk.CTkLabel(name, text="Pro v" + APP_VERSION, font=F["tiny"], text_color=C["accent2"]).pack(anchor="w")
        
        # Separator
        ctk.CTkFrame(self.sidebar, fg_color=C["border"], height=1).pack(fill="x", padx=20, pady=(20, 15))
        
        # Nav
        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.pack(fill="x", padx=10)
        
        self.nav_items = [
            ("🏠", "Accueil", self.show_home, C["text"]),
            ("💬", "Chat IA", self.show_chat, C["accent2"]),
            ("📊", "Dashboard", self.show_dashboard, C["blue"]),
            ("🤖", "Modèles", self.show_models, C["purple"]),
            ("🎯", "Entraînement", self.show_training, C["orange"]),
            ("📁", "Fichiers", self.show_files, C["cyan"]),
            ("📝", "Éditeur", self.show_editor, C["green"]),
            ("⚡", "Terminal", self.show_terminal, C["yellow"]),
            ("📋", "Git", self.show_git, C["pink"]),
        ]
        
        self.nav_btns = {}
        for icon, text, cmd, color in self.nav_items:
            self.make_nav(nav, icon, text, cmd, color)
        
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)
        
        # Bottom
        ctk.CTkFrame(self.sidebar, fg_color=C["border"], height=1).pack(fill="x", padx=20, pady=(0, 10))
        
        self.make_nav(nav, "⚙", "Paramètres", self.show_settings, C["text3"])
        
        # Status
        status_frame = ctk.CTkFrame(self.sidebar, fg_color=C["bg3"], corner_radius=10)
        status_frame.pack(fill="x", padx=15, pady=(10, 15))
        
        ctk.CTkLabel(status_frame, text="●  En ligne", font=F["small"],
                    text_color=C["green"]).pack(padx=12, pady=8, anchor="w")
    
    def make_nav(self, parent, icon, text, cmd, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent", height=42, corner_radius=10)
        frame.pack(fill="x", pady=2)
        frame.pack_propagate(False)
        
        btn = ctk.CTkButton(frame, text=f"  {icon}    {text}", font=F["body"],
                           fg_color="transparent", text_color=C["text2"],
                           hover_color=C["bg3"], anchor="w",
                           command=cmd, corner_radius=10, height=42,
                           text_color_disabled=C["text3"])
        btn.pack(fill="x", padx=5)
        
        self.nav_btns[text] = btn
    
    def build_header(self):
        self.header = ctk.CTkFrame(self, fg_color=C["bg2"], height=65, corner_radius=0)
        self.header.grid(row=0, column=1, sticky="ew")
        self.header.grid_propagate(False)
        
        self.page_title = ctk.CTkLabel(self.header, text="🏠 Accueil",
                                       font=F["title"], text_color=C["text"])
        self.page_title.pack(side="left", padx=30)
        
        # Search
        search = ctk.CTkFrame(self.header, fg_color="transparent")
        search.pack(side="right", padx=30)
        
        self.search = ctk.CTkEntry(search, placeholder_text="⌘ Rechercher...",
                                   width=400, height=40,
                                   fg_color=C["bg3"], border_color=C["border"],
                                   text_color=C["text"],
                                   placeholder_text_color=C["text3"],
                                   font=F["body"], corner_radius=12)
        self.search.pack()
    
    def build_content(self):
        self.content = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", pady=(65, 35))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        
        self.page = ctk.CTkFrame(self.content, fg_color="transparent", corner_radius=0)
        self.page.grid(row=0, column=0, sticky="nsew")
    
    def build_statusbar(self):
        self.statusbar = ctk.CTkFrame(self, fg_color=C["bg2"], height=35, corner_radius=0)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.statusbar.grid_propagate(False)
        
        left = ctk.CTkFrame(self.statusbar, fg_color="transparent")
        left.pack(side="left", padx=20, fill="y")
        
        self.status_dot = ctk.CTkLabel(left, text="●", font=("Segoe UI", 8), text_color=C["green"])
        self.status_dot.pack(side="left", pady=8)
        
        self.status_text = ctk.CTkLabel(left, text="  Prêt", font=F["small"], text_color=C["text2"])
        self.status_text.pack(side="left", padx=(5, 0))
        
        ctk.CTkLabel(self.statusbar, text=f"📁 {self.dir}", font=F["tiny"],
                    text_color=C["text3"]).pack(side="right", padx=20)
        
        ctk.CTkLabel(self.statusbar, text=f"v{APP_VERSION}", font=F["tiny"],
                    text_color=C["text3"]).pack(side="right", padx=10)
    
    def clear(self):
        for w in self.page.winfo_children():
            w.destroy()
    
    def set_title(self, t):
        self.page_title.configure(text=t)
    
    def set_status(self, t, c="green"):
        self.status_text.configure(text=f"  {t}")
        self.status_dot.configure(text_color=C.get(c, C["green"]))
    
    # ═══════════════════════════════════════════════════════════════
    # HOME
    # ═══════════════════════════════════════════════════════════════
    
    def show_home(self):
        self.clear()
        self.set_title("🏠  Accueil")
        self.set_status("Accueil")
        
        s = ctk.CTkScrollableFrame(self.page, fg_color="transparent")
        s.pack(fill="both", expand=True, padx=35, pady=25)
        
        # Hero
        hero = ctk.CTkFrame(s, fg_color=C["card"], corner_radius=20)
        hero.pack(fill="x", pady=(0, 25))
        
        h = ctk.CTkFrame(hero, fg_color="transparent")
        h.pack(fill="x", padx=40, pady=35)
        
        logo = ctk.CTkFrame(h, fg_color=C["accent"], width=80, height=80, corner_radius=22)
        logo.pack(pady=(0, 20))
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 36, "bold"), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(h, text=APP_NAME, font=F["logo"], text_color=C["text"]).pack()
        ctk.CTkLabel(h, text=APP_SUBTITLE, font=F["body"], text_color=C["text2"]).pack(pady=(8, 0))
        
        # Stats row
        stats = ctk.CTkFrame(s, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 25))
        stats.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        for i, (val, label, color) in enumerate([
            (len([f for f in os.listdir(self.dir) if f.endswith('.py')]), "Fichiers Python", C["blue"]),
            (len([f for f in os.listdir(os.path.join(self.dir, 'models')) if os.path.isdir(os.path.join(self.dir, 'models', f))]) if os.path.exists(os.path.join(self.dir, 'models')) else 0, "Modèles", C["purple"]),
            (8, "Outils", C["green"]),
            (1, "Chat IA", C["accent2"]),
        ]):
            card = ctk.CTkFrame(stats, fg_color=C["card"], corner_radius=14)
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=20, pady=18)
            
            ctk.CTkLabel(inner, text=str(val), font=("Segoe UI", 28, "bold"),
                        text_color=color).pack(anchor="w")
            ctk.CTkLabel(inner, text=label, font=F["small"],
                        text_color=C["text2"]).pack(anchor="w")
        
        # Quick actions
        ctk.CTkLabel(s, text="⚡  Actions Rapides", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 15))
        
        grid = ctk.CTkFrame(s, fg_color="transparent")
        grid.pack(fill="x", pady=(0, 25))
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, (icon, title, desc, cmd, color) in enumerate([
            ("💬", "Chat IA", "Discuter avec l'IA", self.show_chat, C["accent"]),
            ("📊", "Dashboard", "Vue d'ensemble", self.show_dashboard, C["blue"]),
            ("📝", "Éditeur", "Écrire du code", self.show_editor, C["green"]),
            ("🎯", "Entraîner", "Entraîner le modèle", self.show_training, C["orange"]),
            ("🤖", "Modèles", "Gérer les modèles", self.show_models, C["purple"]),
            ("⚡", "Terminal", "Exécuter des commandes", self.show_terminal, C["yellow"]),
        ]):
            r, c = divmod(i, 3)
            self.action_card(grid, icon, title, desc, cmd, color).grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
    
    def action_card(self, parent, icon, title, desc, cmd, color):
        card = ctk.CTkFrame(parent, fg_color=C["card"], corner_radius=16, height=150, cursor="hand2")
        card.grid_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=22, pady=22)
        
        ico = ctk.CTkFrame(inner, fg_color=color, width=48, height=48, corner_radius=14)
        ico.pack(anchor="w")
        ico.pack_propagate(False)
        ctk.CTkLabel(ico, text=icon, font=("Segoe UI", 22), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(inner, text=title, font=F["h2"], text_color=C["text"]).pack(anchor="w", pady=(14, 4))
        ctk.CTkLabel(inner, text=desc, font=F["small"], text_color=C["text2"]).pack(anchor="w")
        
        card.bind("<Button-1>", lambda e: cmd())
        return card
    
    # ═══════════════════════════════════════════════════════════════
    # CHAT
    # ═══════════════════════════════════════════════════════════════
    
    def show_chat(self):
        self.clear()
        self.set_title("💬  Chat IA")
        self.set_status("Chat IA", "purple")
        
        cf = ctk.CTkFrame(self.page, fg_color="transparent")
        cf.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header
        hdr = ctk.CTkFrame(cf, fg_color=C["card"], corner_radius=16, height=75)
        hdr.pack(fill="x", pady=(0, 12))
        hdr.pack_propagate(False)
        
        av = ctk.CTkFrame(hdr, fg_color=C["accent"], width=50, height=50, corner_radius=14)
        av.pack(side="left", padx=(20, 15), pady=12)
        av.pack_propagate(False)
        ctk.CTkLabel(av, text="G", font=("Segoe UI", 20, "bold"), text_color="white").pack(expand=True)
        
        info = ctk.CTkFrame(hdr, fg_color="transparent")
        info.pack(side="left", fill="y")
        ctk.CTkLabel(info, text="Grden IA Assistant", font=F["h2"], text_color=C["text"]).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(info, text="●  En ligne • Prêt à vous aider", font=F["small"], text_color=C["green"]).pack(anchor="w")
        
        ctk.CTkButton(hdr, text="🗑️  Effacer", font=F["small"],
                     fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                     width=100, command=self.clear_chat).pack(side="right", padx=20)
        
        # Messages
        self.chat_scroll = ctk.CTkScrollableFrame(cf, fg_color=C["card"], corner_radius=16)
        self.chat_scroll.pack(fill="both", expand=True, pady=(0, 12))
        
        self.chat_msgs = []
        
        # Welcome
        self.ai_msg("Bonjour ! 👋\n\nJe suis **Grden IA**, votre assistant intelligent.\n\nJe peux vous aider avec :\n• 💻 Génération de code\n• 🔍 Analyse de fichiers\n• 🐛 Debug d'erreurs\n• 📚 Explications\n• ⚡ Optimisations\n\nComment puis-je vous aider ?")
        
        # Quick actions
        qf = ctk.CTkFrame(cf, fg_color=C["card"], corner_radius=16)
        qf.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(qf, text="  ⚡  Actions Rapides", font=F["h2"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(12, 8))
        
        qbtns = ctk.CTkFrame(qf, fg_color="transparent")
        qbtns.pack(fill="x", padx=15, pady=(0, 12))
        
        for text in ["💡 Générer du code", "🔍 Analyser fichier", "🐛 Debug erreur", "📚 Expliquer concept", "⚡ Optimiser"]:
            ctk.CTkButton(qbtns, text=text, font=F["small"],
                         fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                         height=32, command=lambda t=text: self.quick_chat(t)).pack(side="left", padx=(0, 6))
        
        # Input
        inp = ctk.CTkFrame(cf, fg_color=C["card"], corner_radius=16)
        inp.pack(fill="x")
        
        self.chat_input = ctk.CTkTextbox(inp, fg_color=C["bg3"], text_color=C["text"],
                                         font=F["body"], corner_radius=12, height=55, wrap="word")
        self.chat_input.pack(fill="x", padx=15, pady=(12, 8))
        self.chat_input.bind("<Return>", lambda e: self.send_msg())
        
        ib = ctk.CTkFrame(inp, fg_color="transparent")
        ib.pack(fill="x", padx=15, pady=(0, 12))
        
        ctk.CTkButton(ib, text="📤  Envoyer", font=F["h2"],
                     fg_color=C["accent"], text_color="white", hover_color=C["accent2"],
                     height=42, command=self.send_msg).pack(side="right")
        
        ctk.CTkButton(ib, text="📎  Joindre un fichier", font=F["small"],
                     fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                     height=36).pack(side="left")
    
    def ai_msg(self, text):
        f = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        f.pack(fill="x", pady=6, padx=10)
        
        c = ctk.CTkFrame(f, fg_color=C["bg3"], corner_radius=14)
        c.pack(anchor="w", padx=(0, 60))
        
        h = ctk.CTkFrame(c, fg_color="transparent")
        h.pack(fill="x", padx=14, pady=(12, 6))
        
        av = ctk.CTkFrame(h, fg_color=C["accent"], width=22, height=22, corner_radius=6)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text="G", font=("Segoe UI", 9, "bold"), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(h, text="Grden IA", font=F["small"], text_color=C["accent2"]).pack(side="left", padx=(8, 0))
        ctk.CTkLabel(h, text=datetime.now().strftime("%H:%M"), font=F["tiny"], text_color=C["text3"]).pack(side="right")
        
        # Format markdown-like text
        display_text = text.replace("**", "").replace("• ", "  • ")
        ctk.CTkLabel(c, text=display_text, font=F["body"], text_color=C["text"],
                    wraplength=550, justify="left", anchor="w").pack(fill="x", padx=14, pady=(0, 14))
        
        self.chat_msgs.append({"role": "ai", "text": text})
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
    
    def user_msg(self, text):
        f = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        f.pack(fill="x", pady=6, padx=10)
        
        c = ctk.CTkFrame(f, fg_color=C["accent"], corner_radius=14)
        c.pack(anchor="e", padx=(60, 0))
        
        ctk.CTkLabel(c, text=text, font=F["body"], text_color="white",
                    wraplength=550, justify="left", anchor="w").pack(fill="x", padx=14, pady=12)
        
        self.chat_msgs.append({"role": "user", "text": text})
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
    
    def typing_indicator(self):
        self.typing = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        self.typing.pack(fill="x", pady=6, padx=10)
        
        c = ctk.CTkFrame(self.typing, fg_color=C["bg3"], corner_radius=14)
        c.pack(anchor="w")
        
        ctk.CTkLabel(c, text="● ● ●  Grden IA réfléchit...", font=F["small"],
                    text_color=C["text3"]).pack(padx=16, pady=12)
    
    def send_msg(self):
        text = self.chat_input.get("1.0", "end-1c").strip()
        if not text:
            return
        
        self.user_msg(text)
        self.chat_input.delete("1.0", "end")
        
        threading.Thread(target=self.gen_response, args=(text,), daemon=True).start()
    
    def gen_response(self, msg):
        self.after(300, self.typing_indicator)
        
        time.sleep(0.8)
        
        ml = msg.lower()
        
        if any(w in ml for w in ["code", "générer", "créer", "fonction", "écrire"]):
            r = """Voici un exemple de code :

def fibonacci_optimized(n):
    '''Suite de Fibonacci optimisée'''
    if n <= 0: return []
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib[:n]

# Exemple d'utilisation
resultat = fibonacci_optimized(10)
print(resultat)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

Voulez-vous que je génère autre chose ?"""
        
        elif any(w in ml for w in ["analyser", "analyse", "review"]):
            r = """📊 **Analyse de Code**

Je peux analyser votre code sous plusieurs angles :

• **Qualité** : Lisibilité, maintenabilité
• **Performance** : Optimisations possibles
• **Sécurité** : Vulnérabilités potentielles
• **Complexité** : Métriques de complexité
• **Conventions** : Respect du style

Envoyez-moi un fichier ou collez du code !"""
        
        elif any(w in ml for w in ["debug", "erreur", "bug", "problème"]):
            r = """🐛 **Debug Assistant**

Pour vous aider efficacement, fournissez :

• Le message d'erreur complet
• Le code qui pose problème
• Les étapes pour reproduire
• Ce que vous avez déjà essayé

💡 **Conseils rapides :**
• Vérifiez les typos
• Imprimez les variables
• Utilisez try/except"""
        
        elif any(w in ml for w in ["expliquer", "comment", "pourquoi"]):
            r = """📚 **Explication**

Je peux expliquer :

• Des concepts de programmation
• Le fonctionnement d'algorithmes
• La logique du code
• Des design patterns
• Les bonnes pratiques

Posez votre question !"""
        
        elif any(w in ml for w in ["bonjour", "salut", "hello", "hey"]):
            r = "Bonjour ! 😊\n\nComment puis-je vous aider aujourd'hui ?"
        
        elif any(w in ml for w in ["merci", "thanks"]):
            r = "De rien ! 😊 N'hésitez pas si vous avez d'autres questions !"
        
        else:
            r = f"""Intéressant ! Pour mieux vous aider, décrivez-moi :

• **Ce que vous voulez faire**
• **Le contexte** (langage, projet)
• **Les détails** (erreurs, comportement)

Je suis là pour vous aider ! 🚀"""
        
        self.after(100, lambda: self.hide_typing())
        self.after(200, lambda: self.ai_msg(r))
    
    def hide_typing(self):
        if hasattr(self, 'typing'):
            self.typing.destroy()
    
    def quick_chat(self, action):
        msgs = {
            "💡 Générer du code": "Génère une fonction de tri en Python",
            "🔍 Analyser fichier": "Analyse la qualité de mon code",
            "🐛 Debug erreur": "J'ai une erreur dans mon code",
            "📚 Expliquer concept": "Explique la récursion",
            "⚡ Optimiser": "Optimise ce code pour la performance",
        }
        if action in msgs:
            self.chat_input.delete("1.0", "end")
            self.chat_input.insert("1.0", msgs[action])
    
    def clear_chat(self):
        for w in self.chat_scroll.winfo_children():
            w.destroy()
        self.chat_msgs = []
        self.ai_msg("Chat effacé ! Comment puis-je vous aider ?")
    
    # ═══════════════════════════════════════════════════════════════
    # DASHBOARD
    # ═══════════════════════════════════════════════════════════════
    
    def show_dashboard(self):
        self.clear()
        self.set_title("📊  Dashboard")
        self.set_status("Dashboard", "blue")
        
        s = ctk.CTkScrollableFrame(self.page, fg_color="transparent")
        s.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(s, text="📊  Vue d'Ensemble", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 25))
        
        # Stats grid
        grid = ctk.CTkFrame(s, fg_color="transparent")
        grid.pack(fill="x", pady=(0, 20))
        grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        py_count = len([f for f in os.listdir(self.dir) if f.endswith('.py')])
        models_dir = os.path.join(self.dir, 'models')
        model_count = len([d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]) if os.path.exists(models_dir) else 0
        
        for i, (val, lbl, sub, color) in enumerate([
            (py_count, "Fichiers Python", "Dans le projet", C["blue"]),
            (model_count, "Modèles IA", "Disponibles", C["purple"]),
            (8, "Outils", "Fonctionnalités", C["green"]),
            (len(self.chat_msgs), "Messages", "Dans le chat", C["accent2"]),
        ]):
            card = ctk.CTkFrame(grid, fg_color=C["card"], corner_radius=14)
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=20, pady=20)
            
            ctk.CTkLabel(inner, text=str(val), font=("Segoe UI", 32, "bold"),
                        text_color=color).pack(anchor="w")
            ctk.CTkLabel(inner, text=lbl, font=F["h2"], text_color=C["text"]).pack(anchor="w")
            ctk.CTkLabel(inner, text=sub, font=F["small"], text_color=C["text2"]).pack(anchor="w")
        
        # Recent files
        ctk.CTkLabel(s, text="📄  Fichiers Récents", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", pady=(20, 15))
        
        files_card = ctk.CTkFrame(s, fg_color=C["card"], corner_radius=14)
        files_card.pack(fill="x")
        
        py_files = [f for f in os.listdir(self.dir) if f.endswith('.py')][:8]
        for f in py_files:
            item = ctk.CTkFrame(files_card, fg_color="transparent", height=44)
            item.pack(fill="x", padx=2, pady=1)
            
            ctk.CTkLabel(item, text=f"  🐍  {f}", font=F["mono_s"],
                        text_color=C["text2"]).pack(side="left", padx=12)
            
            ctk.CTkButton(item, text="Ouvrir", font=F["tiny"],
                         fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                         width=70, height=26,
                         command=lambda f=f: self.open_file(os.path.join(self.dir, f))).pack(side="right", padx=12)
    
    # ═══════════════════════════════════════════════════════════════
    # MODELS
    # ═══════════════════════════════════════════════════════════════
    
    def show_models(self):
        self.clear()
        self.set_title("🤖  Modèles IA")
        self.set_status("Modèles", "purple")
        
        s = ctk.CTkScrollableFrame(self.page, fg_color="transparent")
        s.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(s, text="🤖  Modèles Disponibles", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 25))
        
        grid = ctk.CTkFrame(s, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        models_dir = os.path.join(self.dir, "models")
        if os.path.exists(models_dir):
            models = [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]
            
            for i, model in enumerate(models):
                r, c = divmod(i, 3)
                
                card = ctk.CTkFrame(grid, fg_color=C["card"], corner_radius=16)
                card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
                
                ico = ctk.CTkFrame(card, fg_color=C["accent"], width=60, height=60, corner_radius=16)
                ico.pack(padx=20, pady=(20, 10))
                ico.pack_propagate(False)
                ctk.CTkLabel(ico, text="🧠", font=("Segoe UI", 26), text_color="white").pack(expand=True)
                
                ctk.CTkLabel(card, text=model, font=F["h2"],
                            text_color=C["text"]).pack(pady=(0, 5))
                
                count = sum(len(f) for _, _, f in os.walk(os.path.join(models_dir, model)))
                ctk.CTkLabel(card, text=f"{count} fichiers", font=F["small"],
                            text_color=C["text2"]).pack()
    
    # ═══════════════════════════════════════════════════════════════
    # TRAINING
    # ═══════════════════════════════════════════════════════════════
    
    def show_training(self):
        self.clear()
        self.set_title("🎯  Entraînement")
        self.set_status("Entraînement", "orange")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="🎯  Entraînement IA", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 20))
        
        # Config
        cfg = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        cfg.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(cfg, text="  ⚙  Configuration", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(cfg, text="Sujet d'entraînement :",
                    font=F["small"], text_color=C["text2"]).pack(anchor="w", padx=15)
        self.topic = ctk.CTkEntry(cfg, placeholder_text="Unity game development...",
                                 fg_color=C["bg3"], border_color=C["border"],
                                 text_color=C["text"], font=F["mono"], height=42)
        self.topic.pack(fill="x", padx=15, pady=(5, 12))
        self.topic.insert(0, "Unity game development best practices")
        
        pf = ctk.CTkFrame(cfg, fg_color="transparent")
        pf.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(pf, text="Pages :", font=F["small"], text_color=C["text2"]).pack(side="left")
        self.pages = ctk.CTkEntry(pf, width=60, height=36, fg_color=C["bg3"],
                                 border_color=C["border"], text_color=C["text"], font=F["mono"])
        self.pages.pack(side="left", padx=(5, 20))
        self.pages.insert(0, "3")
        
        ctk.CTkLabel(pf, text="Itérations :", font=F["small"], text_color=C["text2"]).pack(side="left")
        self.iters = ctk.CTkEntry(pf, width=60, height=36, fg_color=C["bg3"],
                                 border_color=C["border"], text_color=C["text"], font=F["mono"])
        self.iters.pack(side="left", padx=(5, 0))
        self.iters.insert(0, "3")
        
        ctk.CTkButton(cfg, text="🎯  Lancer l'Entraînement", font=F["h1"],
                     fg_color=C["accent"], text_color="white", hover_color=C["accent2"],
                     height=48, command=self.start_training).pack(padx=15, pady=(0, 15))
        
        # Log
        log = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        log.pack(fill="both", expand=True)
        
        ctk.CTkLabel(log, text="  📋  Journal", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.train_log = ctk.CTkTextbox(log, fg_color=C["bg3"], text_color=C["text"],
                                        font=F["mono"], corner_radius=12)
        self.train_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def start_training(self):
        topic = self.topic.get()
        pages = self.pages.get()
        iters = self.iters.get()
        
        cmd = f'python orchestrator.py --topic "{topic}" --pages {pages} --iterations {iters} --no-dashboard'
        self.train_log.insert("end", f"$ {cmd}\n\n")
        self.set_status("Entraînement...", "orange")
        
        threading.Thread(target=self._train, args=(cmd,), daemon=True).start()
    
    def _train(self, cmd):
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=self.dir, text=True)
            for line in proc.stdout:
                self.after(0, lambda l=line: self.train_log.insert("end", l))
                self.after(0, lambda: self.train_log.see("end"))
            proc.wait()
            self.after(0, lambda: self.set_status("Terminé ✓", "green"))
        except Exception as e:
            self.after(0, lambda: self.train_log.insert("end", f"Erreur: {e}\n"))
    
    # ═══════════════════════════════════════════════════════════════
    # FILES
    # ═══════════════════════════════════════════════════════════════
    
    def show_files(self):
        self.clear()
        self.set_title("📁  Explorateur")
        self.set_status("Fichiers", "cyan")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="📁  Explorateur de Fichiers", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 20))
        
        tree = ctk.CTkScrollableFrame(f, fg_color=C["card"], corner_radius=16)
        tree.pack(fill="both", expand=True)
        
        self.load_tree(self.dir, tree)
    
    def load_tree(self, path, parent, level=0):
        if level > 4:
            return
        try:
            for item in sorted(os.listdir(path)):
                if item.startswith('.') or item == '__pycache__':
                    continue
                
                full = os.path.join(path, item)
                is_dir = os.path.isdir(full)
                
                row = ctk.CTkFrame(parent, fg_color="transparent", height=38)
                row.pack(fill="x", padx=level * 25, pady=1)
                row.pack_propagate(False)
                
                icon = "📁" if is_dir else "📄"
                color = C["blue"] if is_dir else C["text2"]
                
                ctk.CTkLabel(row, text=f"  {icon}  {item}", font=F["mono_s"],
                            text_color=color, anchor="w").pack(side="left", fill="x", expand=True)
                
                if not is_dir:
                    ctk.CTkButton(row, text="→", font=F["small"],
                                 fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                                 width=35, height=26,
                                 command=lambda f=full: self.open_file(f)).pack(side="right", padx=5)
        except:
            pass
    
    # ═══════════════════════════════════════════════════════════════
    # EDITOR
    # ═══════════════════════════════════════════════════════════════
    
    def show_editor(self):
        self.clear()
        self.set_title("📝  Éditeur")
        self.set_status("Éditeur", "green")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        # Toolbar
        tb = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=12)
        tb.pack(fill="x", pady=(0, 12))
        
        ctk.CTkButton(tb, text="📂  Ouvrir", font=F["small"],
                     fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                     command=self.action_read).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(tb, text="💾  Sauvegarder", font=F["small"],
                     fg_color=C["green"], text_color="white", hover_color=C["green2"],
                     command=self.save_file).pack(side="left", padx=(0, 10), pady=10)
        
        self.file_lbl = ctk.CTkLabel(tb, text="Aucun fichier", font=F["small"],
                                    text_color=C["text2"])
        self.file_lbl.pack(side="right", padx=12)
        
        # Editor
        ed = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        ed.pack(fill="both", expand=True)
        
        self.editor = ctk.CTkTextbox(ed, fg_color=C["bg3"], text_color=C["text"],
                                    font=F["mono"], corner_radius=12, wrap="word")
        self.editor.pack(fill="both", expand=True, padx=10, pady=10)
    
    def open_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.show_editor()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            self.editor_file = path
            self.file_lbl.configure(text=os.path.basename(path))
            self.set_status(f"Ouvert : {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def action_read(self):
        path = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("All", "*.*")])
        if path:
            self.open_file(path)
    
    def action_write(self):
        path = filedialog.asksaveasfilename(defaultextension=".py",
                                           filetypes=[("Python", "*.py")])
        if path:
            self.show_editor()
            self.editor_file = path
            self.file_lbl.configure(text=os.path.basename(path))
    
    def save_file(self):
        if self.editor_file:
            try:
                with open(self.editor_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.get("1.0", "end"))
                self.set_status(f"Sauvegardé ✓")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
    
    # ═══════════════════════════════════════════════════════════════
    # TERMINAL
    # ═══════════════════════════════════════════════════════════════
    
    def show_terminal(self):
        self.clear()
        self.set_title("⚡  Terminal")
        self.set_status("Terminal", "yellow")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="⚡  Terminal", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 20))
        
        term = ctk.CTkFrame(f, fg_color="#080810", corner_radius=16)
        term.pack(fill="both", expand=True)
        
        self.term_out = ctk.CTkTextbox(term, fg_color="#080810", text_color=C["green"],
                                       font=F["mono"], corner_radius=12)
        self.term_out.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        self.term_out.insert("1.0", f"{self.dir}>\n")
        
        inp = ctk.CTkFrame(term, fg_color="transparent")
        inp.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(inp, text="$", font=F["mono"], text_color=C["green"]).pack(side="left")
        
        self.term_in = ctk.CTkEntry(inp, fg_color="transparent", border_width=0,
                                    text_color=C["green"], font=F["mono"])
        self.term_in.pack(side="left", fill="x", expand=True)
        self.term_in.bind("<Return>", self.exec_cmd)
        self.term_in.focus_set()
    
    def exec_cmd(self, event):
        cmd = self.term_in.get()
        if not cmd:
            return
        self.term_in.delete(0, "end")
        self.term_out.insert("end", f"$ {cmd}\n")
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.dir)
            if r.stdout:
                self.term_out.insert("end", r.stdout)
            if r.stderr:
                self.term_out.insert("end", r.stderr)
        except Exception as e:
            self.term_out.insert("end", f"Erreur: {e}\n")
        self.term_out.see("end")
    
    # ═══════════════════════════════════════════════════════════════
    # GIT
    # ═══════════════════════════════════════════════════════════════
    
    def show_git(self):
        self.clear()
        self.set_title("📋  Git")
        self.set_status("Git", "pink")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="📋  Git", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 20))
        
        # Actions
        act = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        act.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(act, text="  ⚡  Actions", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        bf = ctk.CTkFrame(act, fg_color="transparent")
        bf.pack(fill="x", padx=15, pady=(0, 10))
        
        for txt, cmd in [("📋 Statut", "git status"), ("📝 Diff", "git diff"),
                        ("📜 Log", "git log --oneline -10"), ("➕ Add", "git add .")]:
            ctk.CTkButton(bf, text=txt, font=F["small"],
                         fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                         command=lambda c=cmd: self.run_git(c)).pack(side="left", padx=5)
        
        # Commit
        cf = ctk.CTkFrame(act, fg_color="transparent")
        cf.pack(fill="x", padx=15, pady=(0, 15))
        
        self.commit_in = ctk.CTkEntry(cf, placeholder_text="Message de commit...",
                                     fg_color=C["bg3"], border_color=C["border"],
                                     text_color=C["text"], font=F["mono"], height=42)
        self.commit_in.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(cf, text="💾  Commit", font=F["small"],
                     fg_color=C["green"], text_color="white", hover_color=C["green2"],
                     command=self.git_commit).pack(side="left")
        
        # Output
        out = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        out.pack(fill="both", expand=True)
        
        ctk.CTkLabel(out, text="  📤  Sortie", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.git_out = ctk.CTkTextbox(out, fg_color=C["bg3"], text_color=C["text"],
                                      font=F["mono"], corner_radius=12)
        self.git_out.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def run_git(self, cmd):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.dir)
            self.git_out.insert("end", f"$ {cmd}\n{r.stdout}\n")
            if r.stderr:
                self.git_out.insert("end", f"⚠ {r.stderr}\n")
            self.git_out.see("end")
        except Exception as e:
            self.git_out.insert("end", f"Erreur: {e}\n")
    
    def git_commit(self):
        msg = self.commit_in.get()
        if not msg:
            return
        self.run_git("git add .")
        self.run_git(f'git commit -m "{msg}"')
        self.commit_in.delete(0, "end")
    
    # ═══════════════════════════════════════════════════════════════
    # ANALYSIS
    # ═══════════════════════════════════════════════════════════════
    
    def show_analysis(self):
        self.clear()
        self.set_title("📊  Analyse Code")
        self.set_status("Analyse", "orange")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="📊  Analyse de Code", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 20))
        
        # Input
        inp = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        inp.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(inp, text="  📄  Fichier à analyser", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        pf = ctk.CTkFrame(inp, fg_color="transparent")
        pf.pack(fill="x", padx=15, pady=(0, 15))
        
        self.ana_path = ctk.CTkEntry(pf, placeholder_text="Chemin du fichier...",
                                    fg_color=C["bg3"], border_color=C["border"],
                                    text_color=C["text"], font=F["mono"], height=42)
        self.ana_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(pf, text="📂", font=F["small"],
                     fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                     width=45, command=self.browse_file).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(pf, text="📊  Analyser", font=F["small"],
                     fg_color=C["accent"], text_color="white", hover_color=C["accent2"],
                     command=self.run_analysis).pack(side="left")
        
        # Results
        res = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        res.pack(fill="both", expand=True)
        
        ctk.CTkLabel(res, text="  📈  Résultats", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.ana_res = ctk.CTkTextbox(res, fg_color=C["bg3"], text_color=C["text"],
                                      font=F["mono"], corner_radius=12)
        self.ana_res.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("All", "*.*")])
        if path:
            self.ana_path.delete(0, "end")
            self.ana_path.insert(0, path)
    
    def run_analysis(self):
        path = self.ana_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Erreur", "Fichier non trouvé")
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            words = len(content.split())
            funcs = content.count('def ') + content.count('function ')
            classes = content.count('class ')
            imports = content.count('import ')
            complexity = content.count('if ') + content.count('for ') + content.count('while ')
            score = min(100, max(0, 100 - (complexity * 2)))
            
            ext = os.path.splitext(path)[1]
            lang = {'.py': 'Python', '.js': 'JS', '.ts': 'TS', '.cs': 'C#'}.get(ext, 'N/A')
            
            result = f"""
{'═'*50}
  📊  RÉSULTATS DE L'ANALYSE
{'═'*50}

  📁 Fichier : {os.path.basename(path)}
  🌐 Langage : {lang}
  📏 Taille  : {os.path.getsize(path)} bytes

{'─'*50}
  📈 STATISTIQUES
{'─'*50}
  Lignes      : {len(lines):>10}
  Mots        : {words:>10}
  Fonctions   : {funcs:>10}
  Classes     : {classes:>10}
  Imports     : {imports:>10}
  Complexité  : {complexity:>10}

{'─'*50}
  🏆 SCORE : {score}/100
{'═'*50}
"""
            self.ana_res.delete("1.0", "end")
            self.ana_res.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    # ═══════════════════════════════════════════════════════════════
    # SETTINGS
    # ═══════════════════════════════════════════════════════════════
    
    def show_settings(self):
        self.clear()
        self.set_title("⚙  Paramètres")
        self.set_status("Paramètres")
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="⚙  Paramètres", font=F["title"],
                    text_color=C["text"]).pack(anchor="w", pady=(0, 25))
        
        # Apparence
        app = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        app.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(app, text="  🎨  Apparence", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(app, text="Thème : Sombre (actuel)", font=F["body"],
                    text_color=C["text2"]).pack(anchor="w", padx=15, pady=5)
        
        ctk.CTkLabel(app, text="Langue : Français", font=F["body"],
                    text_color=C["text2"]).pack(anchor="w", padx=15, pady=5)
        
        # About
        about = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        about.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(about, text="  ℹ️  À propos", font=F["h1"],
                    text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(about, text=f"Application : {APP_NAME}", font=F["body"],
                    text_color=C["text2"]).pack(anchor="w", padx=15)
        ctk.CTkLabel(about, text=f"Version    : {APP_VERSION}", font=F["body"],
                    text_color=C["text2"]).pack(anchor="w", padx=15, pady=3)
        ctk.CTkLabel(about, text=f"Dossier    : {self.dir}", font=F["mono_s"],
                    text_color=C["text2"]).pack(anchor="w", padx=15, pady=3)


def main():
    app = GrdenIA()
    app.mainloop()


if __name__ == "__main__":
    main()
