"""
Graden IA - Application GUI Professionnelle
Interface moderne et élégante pour le développement logiciel
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font as tkfont
import os
import sys
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

APP_NAME = "Graden IA"
APP_VERSION = "2.0.0"
APP_SUBTITLE = "Intelligence Artificielle pour Développeurs"

# Palette de couleurs professionnelle
COLORS = {
    "bg": "#0f0f1a",
    "bg_secondary": "#161625",
    "bg_tertiary": "#1e1e32",
    "bg_card": "#22223a",
    "bg_hover": "#2a2a45",
    "border": "#2d2d4a",
    "border_light": "#3d3d5c",
    "text": "#e4e4f0",
    "text_secondary": "#a0a0c0",
    "text_dim": "#6a6a8a",
    "accent": "#6c5ce7",
    "accent_light": "#a29bfe",
    "accent_dark": "#5a4bd1",
    "green": "#00d2a0",
    "green_dark": "#00b388",
    "red": "#ff6b6b",
    "yellow": "#feca57",
    "blue": "#54a0ff",
    "cyan": "#00d2d3",
    "orange": "#ff9f43",
    "pink": "#ff6b9d",
}

FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "subtitle": ("Segoe UI", 11),
    "heading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 11),
    "small": ("Segoe UI", 9),
    "mono": ("Cascadia Code", 11),
    "mono_small": ("Cascadia Code", 9),
    "logo": ("Segoe UI", 28, "bold"),
}


class GradenIA:
    """Application principale Graden IA."""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(1000, 700)
        
        # Icon
        self.set_icon()
        
        # Variables
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.editor_file = None
        self.process = None
        
        # Build UI
        self.setup_styles()
        self.build_ui()
        self.show_home()
        
        # Bindings
        self.setup_bindings()
    
    def set_icon(self):
        """Définit l'icône de l'application."""
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IAtrainer.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
    
    def setup_styles(self):
        """Configure les styles ttk."""
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TButton", background=COLORS["accent"], foreground="white")
        style.configure("Treeview", background=COLORS["bg_tertiary"], foreground=COLORS["text"])
    
    def build_ui(self):
        """Construit l'interface principale."""
        # Main container
        self.main_container = tk.Frame(self.root, bg=COLORS["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.build_header()
        
        # Content
        self.content = tk.Frame(self.main_container, bg=COLORS["bg"])
        self.content.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.build_sidebar()
        
        # Main area
        self.main_area = tk.Frame(self.content, bg=COLORS["bg"])
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.build_statusbar()
    
    def build_header(self):
        """Construit l'en-tête professionnel."""
        header = tk.Frame(self.main_container, bg=COLORS["bg_secondary"], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Left: Logo
        left = tk.Frame(header, bg=COLORS["bg_secondary"])
        left.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        # Logo hexagon
        logo_frame = tk.Frame(left, bg=COLORS["accent"], width=36, height=36)
        logo_frame.pack(side=tk.LEFT, pady=12)
        logo_frame.pack_propagate(False)
        tk.Label(logo_frame, text="G", font=("Segoe UI", 16, "bold"),
                bg=COLORS["accent"], fg="white").pack(expand=True)
        
        # Title
        title_frame = tk.Frame(left, bg=COLORS["bg_secondary"])
        title_frame.pack(side=tk.LEFT, padx=(12, 0), pady=12)
        
        tk.Label(title_frame, text=APP_NAME, font=FONTS["heading"],
                bg=COLORS["bg_secondary"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(title_frame, text=APP_VERSION, font=FONTS["small"],
                bg=COLORS["bg_secondary"], fg=COLORS["text_dim"]).pack(anchor="w")
        
        # Center: Search
        center = tk.Frame(header, bg=COLORS["bg_secondary"])
        center.pack(side=tk.LEFT, expand=True, padx=40)
        
        self.search_var = tk.StringVar()
        search = tk.Entry(center, textvariable=self.search_var, font=FONTS["body"],
                         bg=COLORS["bg_tertiary"], fg=COLORS["text"],
                         insertbackground=COLORS["text"], relief=tk.FLAT,
                         bd=0)
        search.pack(ipady=8, padx=100, fill=tk.X)
        search.insert(0, "  Rechercher un fichier, une commande...")
        search.bind("<FocusIn>", lambda e: search.delete(0, tk.END) if "Rechercher" in search.get() else None)
        search.bind("<FocusOut>", lambda e: search.insert(0, "  Rechercher un fichier, une commande...") if not search.get() else None)
        
        # Right: Window controls
        right = tk.Frame(header, bg=COLORS["bg_secondary"])
        right.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        self.build_window_btn(right, "—", self.minimize, COLORS["text_dim"])
        self.build_window_btn(right, "□", self.maximize, COLORS["text_dim"])
        self.build_window_btn(right, "×", self.root.quit, COLORS["red"])
    
    def build_window_btn(self, parent, text, command, color):
        """Bouton de controle window."""
        btn = tk.Label(parent, text=text, font=("Segoe UI", 12),
                      bg=COLORS["bg_secondary"], fg=color, cursor="hand2",
                      padx=12, pady=4)
        btn.pack(side=tk.LEFT, padx=1)
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.configure(bg=COLORS["bg_hover"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=COLORS["bg_secondary"]))
    
    def build_sidebar(self):
        """Construit la barre latérale."""
        self.sidebar = tk.Frame(self.content, bg=COLORS["bg_secondary"], width=240)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Navigation label
        tk.Label(self.sidebar, text="NAVIGATION", font=FONTS["small"],
                bg=COLORS["bg_secondary"], fg=COLORS["text_dim"],
                anchor="w").pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Nav items
        nav_items = [
            ("🏠", "Accueil", self.show_home),
            ("🤖", "Modèles IA", self.show_models),
            ("📊", "Analyse Code", self.show_analysis),
            ("🎯", "Entraînement", self.show_training),
            ("📁", "Explorateur", self.show_files),
            ("📝", "Éditeur", self.show_editor),
            ("⚡", "Terminal", self.show_terminal),
            ("📋", "Git", self.show_git),
            ("⚙", "Paramètres", self.show_settings),
        ]
        
        for icon, text, command in nav_items:
            self.create_nav_item(icon, text, command)
        
        # Spacer
        tk.Frame(self.sidebar, bg=COLORS["bg_secondary"]).pack(fill=tk.BOTH, expand=True)
        
        # Bottom info
        bottom = tk.Frame(self.sidebar, bg=COLORS["bg_secondary"])
        bottom.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(bottom, text="Graden IA v2.0", font=FONTS["small"],
                bg=COLORS["bg_secondary"], fg=COLORS["text_dim"]).pack(anchor="w")
        tk.Label(bottom, text="© 2026 Tous droits réservés", font=("Segoe UI", 8),
                bg=COLORS["bg_secondary"], fg=COLORS["text_dim"]).pack(anchor="w")
    
    def create_nav_item(self, icon, text, command):
        """Crée un élément de navigation."""
        frame = tk.Frame(self.sidebar, bg=COLORS["bg_secondary"], cursor="hand2", height=42)
        frame.pack(fill=tk.X, padx=8, pady=2)
        frame.pack_propagate(False)
        
        lbl = tk.Label(frame, text=f"  {icon}    {text}", font=FONTS["body"],
                       bg=COLORS["bg_secondary"], fg=COLORS["text_secondary"],
                       anchor="w", padx=12)
        lbl.pack(fill=tk.X, expand=True)
        
        def on_enter(e):
            frame.configure(bg=COLORS["bg_hover"])
            lbl.configure(bg=COLORS["bg_hover"], fg=COLORS["text"])
        
        def on_leave(e):
            frame.configure(bg=COLORS["bg_secondary"])
            lbl.configure(bg=COLORS["bg_secondary"], fg=COLORS["text_secondary"])
        
        def on_click(e):
            command()
        
        for widget in [frame, lbl]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
    
    def build_statusbar(self):
        """Construit la barre de statut."""
        self.statusbar = tk.Frame(self.main_container, bg=COLORS["bg_secondary"], height=32)
        self.statusbar.pack(fill=tk.X)
        self.statusbar.pack_propagate(False)
        
        # Left
        left = tk.Frame(self.statusbar, bg=COLORS["bg_secondary"])
        left.pack(side=tk.LEFT, padx=15, fill=tk.Y)
        
        self.status_indicator = tk.Canvas(left, width=8, height=8,
                                         bg=COLORS["bg_secondary"], highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, pady=10)
        self.status_indicator.create_oval(0, 0, 8, 8, fill=COLORS["green"], outline="")
        
        self.status_text = tk.Label(left, text="  Prêt", font=FONTS["small"],
                                   bg=COLORS["bg_secondary"], fg=COLORS["text_secondary"])
        self.status_text.pack(side=tk.LEFT, padx=(5, 0))
        
        # Right
        right = tk.Frame(self.statusbar, bg=COLORS["bg_secondary"])
        right.pack(side=tk.RIGHT, padx=15, fill=tk.Y)
        
        self.dir_text = tk.Label(right, text=f"📁 {self.current_dir}",
                                font=FONTS["small"], bg=COLORS["bg_secondary"],
                                fg=COLORS["text_dim"])
        self.dir_text.pack(side=tk.RIGHT)
    
    def clear_main(self):
        """Efface la zone principale."""
        for w in self.main_area.winfo_children():
            w.destroy()
    
    def update_status(self, text, color=None):
        """Met à jour la barre de statut."""
        self.status_text.config(text=f"  {text}")
        if color:
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(0, 0, 8, 8, fill=color, outline="")
    
    # ═══════════════════════════════════════════════════════════════
    # PAGES
    # ═══════════════════════════════════════════════════════════════
    
    def show_home(self):
        """Page d'accueil."""
        self.clear_main()
        self.update_status("Accueil", COLORS["green"])
        
        # Scrollable frame
        canvas = tk.Canvas(self.main_area, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_area, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=COLORS["bg"])
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Welcome section
        welcome = tk.Frame(scrollable, bg=COLORS["bg"])
        welcome.pack(fill=tk.X, padx=50, pady=(40, 30))
        
        # Logo
        logo = tk.Frame(welcome, bg=COLORS["accent"], width=60, height=60)
        logo.pack(pady=(0, 15))
        logo.pack_propagate(False)
        tk.Label(logo, text="G", font=("Segoe UI", 28, "bold"),
                bg=COLORS["accent"], fg="white").pack(expand=True)
        
        tk.Label(welcome, text=APP_NAME, font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack()
        tk.Label(welcome, text=APP_SUBTITLE, font=FONTS["subtitle"],
                bg=COLORS["bg"], fg=COLORS["text_secondary"]).pack(pady=(5, 0))
        
        # Quick actions
        actions_frame = tk.Frame(scrollable, bg=COLORS["bg"])
        actions_frame.pack(fill=tk.X, padx=50, pady=(10, 30))
        
        tk.Label(actions_frame, text=" ACTIONS RAPIDES", font=FONTS["heading"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 15))
        
        actions = [
            ("📄", "Lire un Fichier", "Analyser le contenu d'un fichier code", self.action_read, COLORS["blue"]),
            ("✏️", "Écrire du Code", "Créer ou modifier un fichier", self.action_write, COLORS["green"]),
            ("🔎", "Rechercher", "Trouver du texte dans les fichiers", self.action_search, COLORS["cyan"]),
            ("📊", "Analyser Code", "Évaluer la qualité et la complexité", self.action_analyze_code, COLORS["orange"]),
            ("▶️", "Exécuter Script", "Lancer un fichier Python", self.action_run, COLORS["accent_light"]),
            ("🎯", "Entraîner IA", "Lancer l'entraînement du modèle", self.action_train, COLORS["pink"]),
        ]
        
        grid = tk.Frame(actions_frame, bg=COLORS["bg"])
        grid.pack(fill=tk.X)
        
        for i, (icon, title, desc, cmd, color) in enumerate(actions):
            row, col = divmod(i, 3)
            card = self.create_action_card(grid, icon, title, desc, cmd, color)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)
        
        # Recent files
        recent_frame = tk.Frame(scrollable, bg=COLORS["bg"])
        recent_frame.pack(fill=tk.X, padx=50, pady=(0, 30))
        
        tk.Label(recent_frame, text=" FICHIERS DU PROJET", font=FONTS["heading"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 15))
        
        files_frame = tk.Frame(recent_frame, bg=COLORS["bg_card"])
        files_frame.pack(fill=tk.X)
        
        py_files = [f for f in os.listdir(self.current_dir) if f.endswith('.py')]
        for f in py_files[:8]:
            item = tk.Frame(files_frame, bg=COLORS["bg_card"], cursor="hand2")
            item.pack(fill=tk.X, padx=1, pady=1)
            
            tk.Label(item, text=f"  🐍  {f}", font=FONTS["mono_small"],
                    bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                    anchor="w").pack(fill=tk.X, padx=10, pady=6)
            
            item.bind("<Enter>", lambda e, i=item: i.configure(bg=COLORS["bg_hover"]))
            item.bind("<Leave>", lambda e, i=item: i.configure(bg=COLORS["bg_card"]))
            item.bind("<Button-1>", lambda e, f=f: self.open_file(os.path.join(self.current_dir, f)))
    
    def create_action_card(self, parent, icon, title, desc, command, color):
        """Crée une carte d'action."""
        card = tk.Frame(parent, bg=COLORS["bg_card"], cursor="hand2", height=100)
        card.pack_propagate(False)
        
        content = tk.Frame(card, bg=COLORS["bg_card"])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icon with color
        icon_frame = tk.Frame(content, bg=color, width=36, height=36)
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text=icon, font=("Segoe UI", 16),
                bg=color, fg="white").pack(expand=True)
        
        tk.Label(content, text=title, font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", pady=(10, 2))
        tk.Label(content, text=desc, font=FONTS["small"],
                bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(anchor="w")
        
        def on_enter(e):
            card.configure(bg=COLORS["bg_hover"])
            for c in card.winfo_children():
                c.configure(bg=COLORS["bg_hover"])
                for cc in c.winfo_children():
                    try:
                        cc.configure(bg=COLORS["bg_hover"])
                    except:
                        pass
        
        def on_leave(e):
            card.configure(bg=COLORS["bg_card"])
            for c in card.winfo_children():
                c.configure(bg=COLORS["bg_card"])
                for cc in c.winfo_children():
                    try:
                        cc.configure(bg=COLORS["bg_card"])
                    except:
                        pass
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e: command())
        
        return card
    
    def show_models(self):
        """Page des modèles IA."""
        self.clear_main()
        self.update_status("Modèles IA", COLORS["blue"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Header
        header = tk.Frame(frame, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(header, text="🤖 Modèles IA", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(header, text="Gérez vos modèles de langage", font=FONTS["subtitle"],
                bg=COLORS["bg"], fg=COLORS["text_secondary"]).pack(anchor="w")
        
        # Models grid
        grid = tk.Frame(frame, bg=COLORS["bg"])
        grid.pack(fill=tk.BOTH, expand=True)
        
        models_dir = os.path.join(self.current_dir, "models")
        if os.path.exists(models_dir):
            model_folders = [d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]
            
            for i, model in enumerate(model_folders):
                row, col = divmod(i, 3)
                
                card = tk.Frame(grid, bg=COLORS["bg_card"])
                card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
                
                # Model icon
                icon_frame = tk.Frame(card, bg=COLORS["accent"], width=50, height=50)
                icon_frame.pack(padx=20, pady=(20, 10))
                icon_frame.pack_propagate(False)
                tk.Label(icon_frame, text="🧠", font=("Segoe UI", 22),
                        bg=COLORS["accent"], fg="white").pack(expand=True)
                
                tk.Label(card, text=model, font=FONTS["heading"],
                        bg=COLORS["bg_card"], fg=COLORS["text"]).pack(pady=(0, 5))
                
                # Count files
                model_path = os.path.join(models_dir, model)
                file_count = sum(len(files) for _, _, files in os.walk(model_path))
                tk.Label(card, text=f"{file_count} fichiers", font=FONTS["small"],
                        bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack()
        
        else:
            tk.Label(grid, text="Aucun modèle trouvé", font=FONTS["body"],
                    bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(pady=50)
        
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)
    
    def show_analysis(self):
        """Page d'analyse de code."""
        self.clear_main()
        self.update_status("Analyse Code", COLORS["orange"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="📊 Analyse de Code", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # Input card
        input_card = tk.Frame(frame, bg=COLORS["bg_card"])
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(input_card, text="  Sélectionner un fichier", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        path_frame = tk.Frame(input_card, bg=COLORS["bg_card"])
        path_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.analysis_path = tk.Entry(path_frame, bg=COLORS["bg_tertiary"], fg=COLORS["text"],
                                     insertbackground=COLORS["text"], font=FONTS["mono"],
                                     relief=tk.FLAT, bd=0)
        self.analysis_path.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        
        self.create_btn(path_frame, "📂 Parcourir", self.browse_file, COLORS["bg_tertiary"])
        self.create_btn(path_frame, "📊 Analyser", self.run_analysis, COLORS["accent"])
        
        # Results card
        result_card = tk.Frame(frame, bg=COLORS["bg_card"])
        result_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(result_card, text="  Résultats", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.analysis_result = scrolledtext.ScrolledText(result_card, bg=COLORS["bg_tertiary"],
                                                        fg=COLORS["text"], font=FONTS["mono"],
                                                        relief=tk.FLAT, wrap=tk.WORD,
                                                        insertbackground=COLORS["text"])
        self.analysis_result.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def show_training(self):
        """Page d'entraînement."""
        self.clear_main()
        self.update_status("Entraînement", COLORS["pink"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="🎯 Entraînement IA", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # Config card
        config_card = tk.Frame(frame, bg=COLORS["bg_card"])
        config_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(config_card, text="  Configuration", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Topic
        tk.Label(config_card, text="Sujet d'entraînement:", font=FONTS["small"],
                bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", padx=15)
        self.topic_entry = tk.Entry(config_card, bg=COLORS["bg_tertiary"], fg=COLORS["text"],
                                   insertbackground=COLORS["text"], font=FONTS["mono"],
                                   relief=tk.FLAT, bd=0)
        self.topic_entry.pack(fill=tk.X, padx=15, ipady=10, pady=(5, 15))
        self.topic_entry.insert(0, "Unity game development best practices")
        
        # Params row
        params = tk.Frame(config_card, bg=COLORS["bg_card"])
        params.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        tk.Label(params, text="Pages:", font=FONTS["small"],
                bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)
        self.pages_spin = tk.Spinbox(params, from_=1, to=20, width=5,
                                     bg=COLORS["bg_tertiary"], fg=COLORS["text"],
                                     font=FONTS["mono"], relief=tk.FLAT)
        self.pages_spin.pack(side=tk.LEFT, padx=(5, 20))
        self.pages_spin.delete(0, tk.END)
        self.pages_spin.insert(0, "3")
        
        tk.Label(params, text="Itérations:", font=FONTS["small"],
                bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)
        self.iter_spin = tk.Spinbox(params, from_=1, to=20, width=5,
                                    bg=COLORS["bg_tertiary"], fg=COLORS["text"],
                                    font=FONTS["mono"], relief=tk.FLAT)
        self.iter_spin.pack(side=tk.LEFT, padx=(5, 0))
        self.iter_spin.delete(0, tk.END)
        self.iter_spin.insert(0, "3")
        
        self.create_btn(config_card, "🎯 Lancer l'Entraînement", self.start_training, COLORS["accent"], large=True)
        
        # Log card
        log_card = tk.Frame(frame, bg=COLORS["bg_card"])
        log_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(log_card, text="  Journal", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.training_log = scrolledtext.ScrolledText(log_card, bg=COLORS["bg_tertiary"],
                                                     fg=COLORS["text"], font=FONTS["mono"],
                                                     relief=tk.FLAT, wrap=tk.WORD,
                                                     insertbackground=COLORS["text"])
        self.training_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def show_files(self):
        """Explorateur de fichiers."""
        self.clear_main()
        self.update_status("Explorateur", COLORS["cyan"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="📁 Explorateur", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # File tree
        tree_card = tk.Frame(frame, bg=COLORS["bg_card"])
        tree_card.pack(fill=tk.BOTH, expand=True)
        
        self.file_tree = tk.Frame(tree_card, bg=COLORS["bg_card"])
        self.file_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.load_tree(self.current_dir, self.file_tree)
    
    def load_tree(self, path, parent, level=0):
        """Charge l'arborescence."""
        if level > 4:
            return
        
        try:
            items = sorted(os.listdir(path))
            for item in items:
                if item.startswith('.') or item == '__pycache__':
                    continue
                
                full = os.path.join(path, item)
                is_dir = os.path.isdir(full)
                
                row = tk.Frame(parent, bg=COLORS["bg_card"])
                row.pack(fill=tk.X, padx=level * 20, pady=1)
                
                icon = "📁" if is_dir else "📄"
                color = COLORS["blue"] if is_dir else COLORS["text_secondary"]
                
                lbl = tk.Label(row, text=f"  {icon}  {item}", font=FONTS["mono_small"],
                              bg=COLORS["bg_card"], fg=color, anchor="w", cursor="hand2")
                lbl.pack(fill=tk.X, padx=10, pady=4)
                
                if is_dir:
                    lbl.bind("<Button-1>", lambda e, p=full: self.load_tree(p, parent))
                else:
                    lbl.bind("<Button-1>", lambda e, p=full: self.open_file(p))
        except:
            pass
    
    def show_editor(self):
        """Éditeur de code."""
        self.clear_main()
        self.update_status("Éditeur", COLORS["green"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="📝 Éditeur", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # Toolbar
        toolbar = tk.Frame(frame, bg=COLORS["bg_card"])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.create_btn(toolbar, "📂 Ouvrir", self.action_read, COLORS["bg_tertiary"])
        self.create_btn(toolbar, "💾 Sauvegarder", self.save_file, COLORS["green"])
        
        self.file_label = tk.Label(toolbar, text="Aucun fichier", font=FONTS["small"],
                                   bg=COLORS["bg_card"], fg=COLORS["text_dim"])
        self.file_label.pack(side=tk.RIGHT, padx=10)
        
        # Editor
        editor_card = tk.Frame(frame, bg=COLORS["bg_card"])
        editor_card.pack(fill=tk.BOTH, expand=True)
        
        self.editor = scrolledtext.ScrolledText(editor_card, bg=COLORS["bg_tertiary"],
                                               fg=COLORS["text"], font=FONTS["mono"],
                                               relief=tk.FLAT, wrap=tk.WORD,
                                               insertbackground=COLORS["text"],
                                               undo=True)
        self.editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_terminal(self):
        """Terminal intégré."""
        self.clear_main()
        self.update_status("Terminal", COLORS["yellow"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="⚡ Terminal", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # Terminal card
        term_card = tk.Frame(frame, bg=COLORS["bg_card"])
        term_card.pack(fill=tk.BOTH, expand=True)
        
        self.term_output = scrolledtext.ScrolledText(term_card, bg="#0a0a12",
                                                    fg=COLORS["green"], font=FONTS["mono"],
                                                    relief=tk.FLAT, wrap=tk.WORD,
                                                    insertbackground=COLORS["green"])
        self.term_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        self.term_output.insert(tk.END, f"{self.current_dir}>\n")
        
        # Input
        input_frame = tk.Frame(term_card, bg="#0a0a12")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(input_frame, text="$ ", font=FONTS["mono"],
                bg="#0a0a12", fg=COLORS["green"]).pack(side=tk.LEFT)
        
        self.term_input = tk.Entry(input_frame, bg="#0a0a12", fg=COLORS["green"],
                                  insertbackground=COLORS["green"], font=FONTS["mono"],
                                  relief=tk.FLAT, bd=0)
        self.term_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.term_input.bind("<Return>", self.exec_terminal)
        self.term_input.focus_set()
    
    def show_git(self):
        """Page Git."""
        self.clear_main()
        self.update_status("Git", COLORS["orange"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="📋 Git", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # Actions
        actions_card = tk.Frame(frame, bg=COLORS["bg_card"])
        actions_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(actions_card, text="  Actions", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        btn_frame = tk.Frame(actions_card, bg=COLORS["bg_card"])
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        for text, cmd in [("📋 Statut", "git status"), ("📝 Diff", "git diff"),
                         ("📜 Log", "git log --oneline -10"), ("➕ Add All", "git add .")]:
            self.create_btn(btn_frame, text, lambda c=cmd: self.run_git(c), COLORS["bg_tertiary"])
        
        # Commit
        commit_frame = tk.Frame(actions_card, bg=COLORS["bg_card"])
        commit_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.commit_entry = tk.Entry(commit_frame, bg=COLORS["bg_tertiary"], fg=COLORS["text"],
                                    insertbackground=COLORS["text"], font=FONTS["mono"],
                                    relief=tk.FLAT, bd=0)
        self.commit_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.commit_entry.insert(0, "Message de commit...")
        
        self.create_btn(commit_frame, "💾 Commit", self.git_commit, COLORS["green"])
        
        # Output
        output_card = tk.Frame(frame, bg=COLORS["bg_card"])
        output_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(output_card, text="  Sortie", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.git_output = scrolledtext.ScrolledText(output_card, bg=COLORS["bg_tertiary"],
                                                   fg=COLORS["text"], font=FONTS["mono"],
                                                   relief=tk.FLAT, wrap=tk.WORD)
        self.git_output.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def show_settings(self):
        """Page paramètres."""
        self.clear_main()
        self.update_status("Paramètres", COLORS["text_dim"])
        
        frame = tk.Frame(self.main_area, bg=COLORS["bg"])
        frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        tk.Label(frame, text="⚙ Paramètres", font=FONTS["title"],
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 25))
        
        # Settings card
        card = tk.Frame(frame, bg=COLORS["bg_card"])
        card.pack(fill=tk.X)
        
        tk.Label(card, text="  Apparence", font=FONTS["heading"],
                bg=COLORS["bg_card"], fg=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        tk.Label(card, text="Thème: Sombre (actuel)", font=FONTS["body"],
                bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", padx=15, pady=5)
        
        tk.Label(card, text="Dossier de travail:", font=FONTS["body"],
                bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", padx=15, pady=(15, 5))
        
        tk.Label(card, text=f"  {self.current_dir}", font=FONTS["mono_small"],
                bg=COLORS["bg_tertiary"], fg=COLORS["text"], anchor="w").pack(fill=tk.X, padx=15, pady=(0, 15), ipady=8)
    
    # ═══════════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    def create_btn(self, parent, text, command, bg=None, large=False):
        """Crée un bouton stylisé."""
        if bg is None:
            bg = COLORS["accent"]
        
        fg = "white" if bg == COLORS["accent"] else COLORS["text"]
        font_size = 11 if large else 10
        
        btn = tk.Button(parent, text=text, font=("Segoe UI", font_size),
                       bg=bg, fg=fg, activebackground=COLORS["accent_dark"],
                       activeforeground="white", relief=tk.FLAT, cursor="hand2",
                       command=command, padx=15, pady=8 if large else 5)
        btn.pack(side=tk.LEFT if not large else tk.TOP, padx=5, pady=5)
        
        btn.bind("<Enter>", lambda e: btn.configure(bg=COLORS["accent_light"]))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        
        return btn
    
    def action_read(self):
        path = filedialog.askopenfilename(
            title="Ouvrir un fichier",
            filetypes=[("Python", "*.py"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if path:
            self.open_file(path)
    
    def open_file(self, path):
        """Ouvre un fichier."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.show_editor()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)
            self.editor_file = path
            self.file_label.config(text=os.path.basename(path))
            self.update_status(f"Ouvert: {os.path.basename(path)}", COLORS["green"])
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def action_write(self):
        path = filedialog.asksaveasfilename(
            title="Sauvegarder",
            defaultextension=".py",
            filetypes=[("Python", "*.py"), ("All", "*.*")]
        )
        if path:
            self.show_editor()
            self.editor_file = path
            self.file_label.config(text=os.path.basename(path))
    
    def save_file(self):
        if self.editor_file:
            try:
                with open(self.editor_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.get("1.0", tk.END))
                self.update_status(f"Sauvegardé: {os.path.basename(self.editor_file)}", COLORS["green"])
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
    
    def action_search(self):
        self.show_terminal()
        pattern = tk.simpledialog.askstring("Rechercher", "Texte à rechercher:")
        if pattern:
            self.term_output.insert(tk.END, f"\nRecherche de '{pattern}'...\n")
            for root_dir, dirs, files in os.walk(self.current_dir):
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]
                for file in files:
                    fp = os.path.join(root_dir, file)
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                            for i, line in enumerate(f, 1):
                                if pattern.lower() in line.lower():
                                    self.term_output.insert(tk.END, f"  {fp}:{i} {line.rstrip()[:80]}\n")
                    except:
                        pass
    
    def action_analyze_code(self):
        self.show_analysis()
    
    def action_run(self):
        path = filedialog.askopenfilename(title="Script Python", filetypes=[("Python", "*.py")])
        if path:
            self.show_terminal()
            self.term_output.insert(tk.END, f"\n$ python {path}\n")
            thread = threading.Thread(target=self._run_thread, args=(path,), daemon=True)
            thread.start()
    
    def _run_thread(self, path):
        try:
            proc = subprocess.Popen(f'python "{path}"', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=self.current_dir, text=True)
            for line in proc.stdout:
                self.root.after(0, lambda l=line: self.term_output.insert(tk.END, l))
                self.root.after(0, lambda: self.term_output.see(tk.END))
            proc.wait()
        except Exception as e:
            self.root.after(0, lambda: self.term_output.insert(tk.END, f"Erreur: {e}\n"))
    
    def action_train(self):
        self.show_training()
    
    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("All", "*.*")])
        if path:
            self.analysis_path.delete(0, tk.END)
            self.analysis_path.insert(0, path)
    
    def run_analysis(self):
        path = self.analysis_path.get()
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
            
            ext = os.path.splitext(path)[1].lower()
            lang_map = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                       '.java': 'Java', '.cpp': 'C++', '.cs': 'C#'}
            lang = lang_map.get(ext, 'Inconnu')
            
            result = f"""
{'='*60}
  RÉSULTATS DE L'ANALYSE
{'='*60}

  Fichier:   {os.path.basename(path)}
  Langage:   {lang}
  Taille:    {os.path.getsize(path)} bytes

{'─'*60}
  STATISTIQUES
{'─'*60}
  Lignes:      {len(lines):>8}
  Mots:        {words:>8}
  Fonctions:   {funcs:>8}
  Classes:     {classes:>8}
  Imports:     {imports:>8}
  Complexité:  {complexity:>8}

{'─'*60}
  SCORE: {min(100, max(0, 100 - (complexity * 2)))}/100
{'='*60}
"""
            self.analysis_result.delete("1.0", tk.END)
            self.analysis_result.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def start_training(self):
        topic = self.topic_entry.get()
        pages = self.pages_spin.get()
        iters = self.iter_spin.get()
        
        cmd = f'python orchestrator.py --topic "{topic}" --pages {pages} --iterations {iters} --no-dashboard'
        self.training_log.insert(tk.END, f"$ {cmd}\n\n")
        self.update_status("Entraînement en cours...", COLORS["yellow"])
        
        thread = threading.Thread(target=self._train_thread, args=(cmd,), daemon=True)
        thread.start()
    
    def _train_thread(self, cmd):
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=self.current_dir, text=True)
            for line in proc.stdout:
                self.root.after(0, lambda l=line: self.training_log.insert(tk.END, l))
                self.root.after(0, lambda: self.training_log.see(tk.END))
            proc.wait()
            self.root.after(0, lambda: self.update_status("Entraînement terminé", COLORS["green"]))
        except Exception as e:
            self.root.after(0, lambda: self.training_log.insert(tk.END, f"Erreur: {e}\n"))
    
    def exec_terminal(self, event):
        cmd = self.term_input.get()
        if not cmd:
            return
        self.term_input.delete(0, tk.END)
        self.term_output.insert(tk.END, f"$ {cmd}\n")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.current_dir)
            if result.stdout:
                self.term_output.insert(tk.END, result.stdout)
            if result.stderr:
                self.term_output.insert(tk.END, result.stderr)
        except Exception as e:
            self.term_output.insert(tk.END, f"Erreur: {e}\n")
        self.term_output.see(tk.END)
    
    def run_git(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.current_dir)
            self.git_output.insert(tk.END, f"$ {cmd}\n{result.stdout}\n")
            if result.stderr:
                self.git_output.insert(tk.END, f"Erreur: {result.stderr}\n")
            self.git_output.see(tk.END)
        except Exception as e:
            self.git_output.insert(tk.END, f"Erreur: {e}\n")
    
    def git_commit(self):
        msg = self.commit_entry.get()
        if not msg or "Message" in msg:
            messagebox.showerror("Erreur", "Entrez un message de commit")
            return
        self.run_git("git add .")
        self.run_git(f'git commit -m "{msg}"')
        self.commit_entry.delete(0, tk.END)
    
    def minimize(self):
        self.root.iconify()
    
    def maximize(self):
        if self.root.state() == 'zoomed':
            self.root.state('normal')
        else:
            self.root.state('zoomed')
    
    def setup_bindings(self):
        """Raccourcis clavier."""
        self.root.bind("<Control-o>", lambda e: self.action_read())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-n>", lambda e: self.action_write())
        self.root.bind("<F5>", lambda e: self.action_run())
        self.root.bind("<F12>", lambda e: self.show_terminal())


def main():
    import tkinter.simpledialog
    root = tk.Tk()
    app = GradenIA(root)
    root.mainloop()


if __name__ == "__main__":
    main()
