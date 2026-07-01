"""
Graden IA - Application GUI Professionnelle
Interface moderne et élégante avec customtkinter
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import tkinter as tk
import os
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

APP_NAME = "Graden IA"
APP_VERSION = "2.5.0"
APP_SUBTITLE = "Intelligence Artificielle pour Développeurs"

# Thème moderne
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Couleurs
COLORS = {
    "bg": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#21262d",
    "bg_card": "#1c2128",
    "border": "#30363d",
    "text": "#f0f6fc",
    "text_secondary": "#8b949e",
    "accent": "#7c3aed",
    "accent_hover": "#8b5cf6",
    "green": "#3fb950",
    "red": "#f85149",
    "yellow": "#d29922",
    "blue": "#58a6ff",
    "cyan": "#39d2c0",
    "orange": "#d18616",
    "purple": "#a371f7",
    "text_dim": "#6e7681",
}

FONTS = {
    "logo": ("Segoe UI", 32, "bold"),
    "title": ("Segoe UI", 22, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 12),
    "small": ("Segoe UI", 10),
    "mono": ("Cascadia Code", 12),
    "mono_small": ("Cascadia Code", 10),
}


class SplashWindow(ctk.CTkToplevel):
    """Fenêtre de splash screen."""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.geometry("500x350")
        self.configure(fg_color=COLORS["bg"])
        
        # Center
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 175
        self.geometry(f"+{x}+{y}")
        
        # Content
        frame = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        frame.pack(fill="both", expand=True)
        
        # Logo
        logo_frame = ctk.CTkFrame(frame, fg_color=COLORS["accent"], 
                                  width=80, height=80, corner_radius=20)
        logo_frame.place(relx=0.5, rely=0.3, anchor="center")
        logo_frame.pack_propagate(False)
        ctk.CTkLabel(logo_frame, text="G", font=("Segoe UI", 36, "bold"),
                    text_color="white").pack(expand=True)
        
        # Title
        ctk.CTkLabel(frame, text=APP_NAME, font=FONTS["logo"],
                    text_color=COLORS["text"]).place(relx=0.5, rely=0.55, anchor="center")
        ctk.CTkLabel(frame, text=APP_SUBTITLE, font=FONTS["small"],
                    text_color=COLORS["text_secondary"]).place(relx=0.5, rely=0.65, anchor="center")
        
        # Progress
        self.progress = ctk.CTkProgressBar(frame, width=300, height=6,
                                           fg_color=COLORS["bg_tertiary"],
                                           progress_color=COLORS["accent"])
        self.progress.place(relx=0.5, rely=0.8, anchor="center")
        self.progress.set(0)
        
        # Loading text
        self.loading_label = ctk.CTkLabel(frame, text="Chargement...",
                                         font=FONTS["small"], text_color=COLORS["text_dim"])
        self.loading_label.place(relx=0.5, rely=0.88, anchor="center")
        
        self.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def update_progress(self, value, text="Chargement..."):
        self.progress.set(value)
        self.loading_label.configure(text=text)
        self.update()


class GradenIA(ctk.CTk):
    """Application principale Grden IA."""
    
    def __init__(self):
        super().__init__()
        
        self.title(APP_NAME)
        self.geometry("1400x900")
        self.configure(fg_color=COLORS["bg"])
        self.minsize(1000, 700)
        
        # Icon
        self.set_icon()
        
        # Variables
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.editor_file = None
        
        # Show splash
        self.withdraw()
        self.show_splash()
    
    def set_icon(self):
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IAtrainer.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass
    
    def show_splash(self):
        """Affiche le splash screen."""
        splash = SplashWindow(self)
        
        def load():
            for i in range(100):
                splash.update_progress(i / 100, "Chargement des composants...")
                splash.update()
            
            splash.destroy()
            self.deiconify()
            self.build_ui()
        
        self.after(100, load)
    
    def build_ui(self):
        """Construit l'interface complète."""
        # Main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.build_sidebar()
        
        # Main content
        self.build_main()
        
        # Status bar
        self.build_statusbar()
    
    def build_sidebar(self):
        """Construit la sidebar."""
        self.sidebar = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"],
                                    width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(25, 30))
        
        logo = ctk.CTkFrame(logo_frame, fg_color=COLORS["accent"],
                           width=42, height=42, corner_radius=12)
        logo.pack(side="left")
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 18, "bold"),
                    text_color="white").pack(expand=True)
        
        name_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        name_frame.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(name_frame, text=APP_NAME, font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(name_frame, text=f"v{APP_VERSION}", font=FONTS["small"],
                    text_color=COLORS["text_secondary"]).pack(anchor="w")
        
        # Navigation
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=10)
        
        nav_items = [
            ("🏠", "Accueil", self.show_home),
            ("🤖", "Modèles IA", self.show_models),
            ("📊", "Analyse", self.show_analysis),
            ("🎯", "Entraînement", self.show_training),
            ("📁", "Explorateur", self.show_files),
            ("📝", "Éditeur", self.show_editor),
            ("⚡", "Terminal", self.show_terminal),
            ("📋", "Git", self.show_git),
        ]
        
        self.nav_buttons = {}
        for icon, text, cmd in nav_items:
            self.create_nav_btn(nav_frame, icon, text, cmd)
        
        # Spacer
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)
        
        # Settings
        self.create_nav_btn(nav_frame, "⚙", "Paramètres", self.show_settings, bottom=True)
        
        # Version
        ctk.CTkLabel(self.sidebar, text="© 2026 Grden IA",
                    font=("Segoe UI", 9), text_color=COLORS["text_secondary"]).pack(pady=(0, 15))
    
    def create_nav_btn(self, parent, icon, text, command, bottom=False):
        """Crée un bouton de navigation."""
        if not bottom:
            frame = ctk.CTkFrame(parent, fg_color="transparent", height=44, corner_radius=10)
            frame.pack(fill="x", pady=2)
            frame.pack_propagate(False)
            
            btn = ctk.CTkButton(frame, text=f"  {icon}  {text}", font=FONTS["body"],
                               fg_color="transparent", text_color=COLORS["text_secondary"],
                               hover_color=COLORS["bg_tertiary"], anchor="w",
                               command=command, corner_radius=10, height=44)
            btn.pack(fill="x", padx=5)
            
            self.nav_buttons[text] = btn
        else:
            frame = ctk.CTkFrame(parent, fg_color="transparent", height=44, corner_radius=10)
            frame.pack(fill="x", pady=2)
            frame.pack_propagate(False)
            
            btn = ctk.CTkButton(frame, text=f"  {icon}  {text}", font=FONTS["body"],
                               fg_color="transparent", text_color=COLORS["text_secondary"],
                               hover_color=COLORS["bg_tertiary"], anchor="w",
                               command=command, corner_radius=10, height=44)
            btn.pack(fill="x", padx=5)
    
    def build_main(self):
        """Construit la zone principale."""
        # Header
        self.header = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"],
                                   height=60, corner_radius=0)
        self.header.grid(row=0, column=1, sticky="ew")
        self.header.grid_propagate(False)
        
        # Header content
        self.header_title = ctk.CTkLabel(self.header, text="🏠 Accueil",
                                         font=FONTS["title"], text_color=COLORS["text"])
        self.header_title.pack(side="left", padx=25)
        
        # Search bar
        search_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        search_frame.pack(side="right", padx=25)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Rechercher...",
                                         width=350, height=38,
                                         fg_color=COLORS["bg_tertiary"],
                                         border_color=COLORS["border"],
                                         text_color=COLORS["text"],
                                         placeholder_text_color=COLORS["text_secondary"],
                                         font=FONTS["body"])
        self.search_entry.pack()
        
        # Content area
        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=(60, 32))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)
        
        # Current page frame
        self.page_frame = ctk.CTkFrame(self.content, fg_color="transparent", corner_radius=0)
        self.page_frame.grid(row=0, column=0, sticky="nsew")
    
    def build_statusbar(self):
        """Construit la barre de statut."""
        self.statusbar = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"],
                                      height=32, corner_radius=0)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.statusbar.grid_propagate(False)
        
        # Status indicator
        self.status_dot = ctk.CTkLabel(self.statusbar, text="●", font=("Segoe UI", 10),
                                       text_color=COLORS["green"])
        self.status_dot.pack(side="left", padx=(15, 5))
        
        self.status_label = ctk.CTkLabel(self.statusbar, text="Prêt",
                                         font=FONTS["small"],
                                         text_color=COLORS["text_secondary"])
        self.status_label.pack(side="left")
        
        # Dir
        self.dir_label = ctk.CTkLabel(self.statusbar, text=f"📁 {self.current_dir}",
                                      font=FONTS["small"],
                                      text_color=COLORS["text_secondary"])
        self.dir_label.pack(side="right", padx=15)
    
    def clear_page(self):
        """Efface la page actuelle."""
        for w in self.page_frame.winfo_children():
            w.destroy()
    
    def set_page_title(self, title, icon=""):
        """Met à jour le titre de la page."""
        self.header_title.configure(text=f"{icon} {title}")
    
    def set_status(self, text, color="green"):
        """Met à jour le statut."""
        self.status_label.configure(text=text)
        self.status_dot.configure(text_color=COLORS.get(color, COLORS["green"]))
    
    # ═══════════════════════════════════════════════════════════════
    # PAGES
    # ═══════════════════════════════════════════════════════════════
    
    def show_home(self):
        """Page d'accueil."""
        self.clear_page()
        self.set_page_title("Accueil", "🏠")
        self.set_status("Accueil")
        
        # Scrollable
        scroll = ctk.CTkScrollableFrame(self.page_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Welcome card
        welcome = ctk.CTkFrame(scroll, fg_color=COLORS["bg_card"], corner_radius=16)
        welcome.pack(fill="x", pady=(0, 20))
        
        inner = ctk.CTkFrame(welcome, fg_color="transparent")
        inner.pack(fill="x", padx=30, pady=30)
        
        # Logo
        logo = ctk.CTkFrame(inner, fg_color=COLORS["accent"],
                           width=70, height=70, corner_radius=18)
        logo.pack(pady=(0, 15))
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 32, "bold"),
                    text_color="white").pack(expand=True)
        
        ctk.CTkLabel(inner, text=APP_NAME, font=FONTS["logo"],
                    text_color=COLORS["text"]).pack()
        ctk.CTkLabel(inner, text=APP_SUBTITLE, font=FONTS["body"],
                    text_color=COLORS["text_secondary"]).pack(pady=(5, 0))
        
        # Quick actions
        actions_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(10, 20))
        
        ctk.CTkLabel(actions_frame, text="Actions Rapides", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 15))
        
        grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        actions = [
            ("📄", "Lire un Fichier", "Analyser un fichier code", self.action_read, COLORS["blue"]),
            ("✏️", "Écrire du Code", "Créer un nouveau fichier", self.action_write, COLORS["green"]),
            ("🔎", "Rechercher", "Trouver dans les fichiers", self.action_search, COLORS["cyan"]),
            ("📊", "Analyser", "Évaluer la qualité", self.action_analyze_code, COLORS["orange"]),
            ("▶️", "Exécuter", "Lancer un script Python", self.action_run, COLORS["purple"]),
            ("🎯", "Entraîner", "Entraîner le modèle IA", self.action_train, COLORS["accent"]),
        ]
        
        for i, (icon, title, desc, cmd, color) in enumerate(actions):
            row, col = divmod(i, 3)
            self.create_action_card(grid, icon, title, desc, cmd, color).grid(
                row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        # Files
        files_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        files_frame.pack(fill="x", pady=(10, 0))
        
        ctk.CTkLabel(files_frame, text="Fichiers du Projet", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 15))
        
        files_card = ctk.CTkFrame(files_frame, fg_color=COLORS["bg_card"], corner_radius=12)
        files_card.pack(fill="x")
        
        py_files = [f for f in os.listdir(self.current_dir) if f.endswith('.py')][:6]
        for f in py_files:
            item = ctk.CTkFrame(files_card, fg_color="transparent", height=40)
            item.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(item, text=f"  🐍  {f}", font=FONTS["mono_small"],
                        text_color=COLORS["text_secondary"]).pack(side="left", padx=10)
            
            btn = ctk.CTkButton(item, text="Ouvrir", font=FONTS["small"],
                               fg_color=COLORS["bg_tertiary"], text_color=COLORS["text"],
                               hover_color=COLORS["border"], width=70, height=28,
                               command=lambda f=f: self.open_file(os.path.join(self.current_dir, f)))
            btn.pack(side="right", padx=10)
    
    def create_action_card(self, parent, icon, title, desc, command, color):
        """Crée une carte d'action."""
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"],
                           corner_radius=14, height=140, cursor="hand2")
        card.grid_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icon
        icon_bg = ctk.CTkFrame(inner, fg_color=color, width=44, height=44, corner_radius=12)
        icon_bg.pack(anchor="w")
        icon_bg.pack_propagate(False)
        ctk.CTkLabel(icon_bg, text=icon, font=("Segoe UI", 20),
                    text_color="white").pack(expand=True)
        
        ctk.CTkLabel(inner, text=title, font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(12, 4))
        ctk.CTkLabel(inner, text=desc, font=FONTS["small"],
                    text_color=COLORS["text_secondary"]).pack(anchor="w")
        
        card.bind("<Button-1>", lambda e: command())
        
        return card
    
    def show_models(self):
        """Page modèles."""
        self.clear_page()
        self.set_page_title("Modèles IA", "🤖")
        self.set_status("Modèles IA", "blue")
        
        scroll = ctk.CTkScrollableFrame(self.page_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Header
        header = ctk.CTkFrame(scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header, text="Modèles Disponibles", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(header, text="Vos modèles de langage IA",
                    font=FONTS["body"], text_color=COLORS["text_secondary"]).pack(anchor="w")
        
        # Models grid
        grid = ctk.CTkFrame(scroll, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        models_dir = os.path.join(self.current_dir, "models")
        if os.path.exists(models_dir):
            models = [d for d in os.listdir(models_dir) 
                     if os.path.isdir(os.path.join(models_dir, d))]
            
            for i, model in enumerate(models):
                row, col = divmod(i, 3)
                card = ctk.CTkFrame(grid, fg_color=COLORS["bg_card"], corner_radius=14)
                card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
                
                # Icon
                icon = ctk.CTkFrame(card, fg_color=COLORS["accent"],
                                   width=50, height=50, corner_radius=14)
                icon.pack(padx=20, pady=(20, 10))
                icon.pack_propagate(False)
                ctk.CTkLabel(icon, text="🧠", font=("Segoe UI", 22),
                            text_color="white").pack(expand=True)
                
                ctk.CTkLabel(card, text=model, font=FONTS["heading"],
                            text_color=COLORS["text"]).pack(pady=(0, 5))
                
                # Count
                model_path = os.path.join(models_dir, model)
                count = sum(len(f) for _, _, f in os.walk(model_path))
                ctk.CTkLabel(card, text=f"{count} fichiers",
                            font=FONTS["small"], text_color=COLORS["text_secondary"]).pack()
    
    def show_analysis(self):
        """Page analyse."""
        self.clear_page()
        self.set_page_title("Analyse Code", "📊")
        self.set_status("Analyse", "orange")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(frame, text="Analyse de Code", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 20))
        
        # Input card
        input_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        input_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(input_card, text="  Sélectionner un fichier", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        path_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        path_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.analysis_path = ctk.CTkEntry(path_frame, placeholder_text="Chemin du fichier...",
                                          fg_color=COLORS["bg_tertiary"],
                                          border_color=COLORS["border"],
                                          text_color=COLORS["text"],
                                          font=FONTS["mono"], height=40)
        self.analysis_path.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(path_frame, text="📂 Parcourir", font=FONTS["small"],
                     fg_color=COLORS["bg_tertiary"], text_color=COLORS["text"],
                     hover_color=COLORS["border"], command=self.browse_file).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(path_frame, text="📊 Analyser", font=FONTS["small"],
                     fg_color=COLORS["accent"], text_color="white",
                     hover_color=COLORS["accent_hover"], command=self.run_analysis).pack(side="left")
        
        # Result card
        result_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        result_card.pack(fill="both", expand=True)
        
        ctk.CTkLabel(result_card, text="  Résultats", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.analysis_result = ctk.CTkTextbox(result_card, fg_color=COLORS["bg_tertiary"],
                                             text_color=COLORS["text"], font=FONTS["mono"],
                                             corner_radius=10)
        self.analysis_result.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def show_training(self):
        """Page entraînement."""
        self.clear_page()
        self.set_page_title("Entraînement", "🎯")
        self.set_status("Entraînement", "purple")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(frame, text="Entraînement IA", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 20))
        
        # Config card
        config = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        config.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(config, text="  Configuration", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Topic
        ctk.CTkLabel(config, text="Sujet d'entraînement:",
                    font=FONTS["small"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=15)
        self.topic_entry = ctk.CTkEntry(config, placeholder_text="Unity game development...",
                                       fg_color=COLORS["bg_tertiary"],
                                       border_color=COLORS["border"],
                                       text_color=COLORS["text"],
                                       font=FONTS["mono"], height=40)
        self.topic_entry.pack(fill="x", padx=15, pady=(5, 15))
        self.topic_entry.insert(0, "Unity game development best practices")
        
        # Params
        params = ctk.CTkFrame(config, fg_color="transparent")
        params.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(params, text="Pages:", font=FONTS["small"],
                    text_color=COLORS["text_secondary"]).pack(side="left")
        self.pages_spin = ctk.CTkEntry(params, width=60, height=35,
                                      fg_color=COLORS["bg_tertiary"],
                                      border_color=COLORS["border"],
                                      text_color=COLORS["text"],
                                      font=FONTS["mono"])
        self.pages_spin.pack(side="left", padx=(5, 20))
        self.pages_spin.insert(0, "3")
        
        ctk.CTkLabel(params, text="Itérations:", font=FONTS["small"],
                    text_color=COLORS["text_secondary"]).pack(side="left")
        self.iter_spin = ctk.CTkEntry(params, width=60, height=35,
                                     fg_color=COLORS["bg_tertiary"],
                                     border_color=COLORS["border"],
                                     text_color=COLORS["text"],
                                     font=FONTS["mono"])
        self.iter_spin.pack(side="left", padx=(5, 0))
        self.iter_spin.insert(0, "3")
        
        # Start button
        ctk.CTkButton(config, text="🎯  Lancer l'Entraînement", font=FONTS["heading"],
                     fg_color=COLORS["accent"], text_color="white",
                     hover_color=COLORS["accent_hover"], height=45,
                     command=self.start_training).pack(padx=15, pady=(0, 15))
        
        # Log card
        log_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        log_card.pack(fill="both", expand=True)
        
        ctk.CTkLabel(log_card, text="  Journal", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.training_log = ctk.CTkTextbox(log_card, fg_color=COLORS["bg_tertiary"],
                                          text_color=COLORS["text"], font=FONTS["mono"],
                                          corner_radius=10)
        self.training_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def show_files(self):
        """Explorateur de fichiers."""
        self.clear_page()
        self.set_page_title("Explorateur", "📁")
        self.set_status("Explorateur", "cyan")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(frame, text="Explorateur de Fichiers", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 20))
        
        # Tree
        tree = ctk.CTkScrollableFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        tree.pack(fill="both", expand=True)
        
        self.load_tree(self.current_dir, tree)
    
    def load_tree(self, path, parent, level=0):
        if level > 4:
            return
        
        try:
            items = sorted(os.listdir(path))
            for item in items:
                if item.startswith('.') or item == '__pycache__':
                    continue
                
                full = os.path.join(path, item)
                is_dir = os.path.isdir(full)
                
                row = ctk.CTkFrame(parent, fg_color="transparent", height=36)
                row.pack(fill="x", padx=level * 20, pady=1)
                row.pack_propagate(False)
                
                icon = "📁" if is_dir else "📄"
                color = COLORS["blue"] if is_dir else COLORS["text_secondary"]
                
                label = ctk.CTkLabel(row, text=f"  {icon}  {item}", font=FONTS["mono_small"],
                                    text_color=color, anchor="w")
                label.pack(side="left", fill="x", expand=True)
                
                if not is_dir:
                    ctk.CTkButton(row, text="Ouvrir", font=FONTS["small"],
                                 fg_color=COLORS["bg_tertiary"], text_color=COLORS["text"],
                                 hover_color=COLORS["border"], width=60, height=26,
                                 command=lambda f=full: self.open_file(f)).pack(side="right", padx=5)
        except:
            pass
    
    def show_editor(self):
        """Éditeur de code."""
        self.clear_page()
        self.set_page_title("Éditeur", "📝")
        self.set_status("Éditeur", "green")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Toolbar
        toolbar = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=12)
        toolbar.pack(fill="x", pady=(0, 15))
        
        ctk.CTkButton(toolbar, text="📂 Ouvrir", font=FONTS["small"],
                     fg_color=COLORS["bg_tertiary"], text_color=COLORS["text"],
                     hover_color=COLORS["border"], command=self.action_read).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(toolbar, text="💾 Sauvegarder", font=FONTS["small"],
                     fg_color=COLORS["green"], text_color="white",
                     hover_color=COLORS["green"], command=self.save_file).pack(side="left", padx=(0, 10), pady=10)
        
        self.file_label = ctk.CTkLabel(toolbar, text="Aucun fichier",
                                      font=FONTS["small"], text_color=COLORS["text_secondary"])
        self.file_label.pack(side="right", padx=10)
        
        # Editor
        editor_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        editor_card.pack(fill="both", expand=True)
        
        self.editor = ctk.CTkTextbox(editor_card, fg_color=COLORS["bg_tertiary"],
                                    text_color=COLORS["text"], font=FONTS["mono"],
                                    corner_radius=10, wrap="word")
        self.editor.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_terminal(self):
        """Terminal intégré."""
        self.clear_page()
        self.set_page_title("Terminal", "⚡")
        self.set_status("Terminal", "yellow")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(frame, text="Terminal", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 20))
        
        # Terminal card
        term_card = ctk.CTkFrame(frame, fg_color="#0a0e14", corner_radius=14)
        term_card.pack(fill="both", expand=True)
        
        self.term_output = ctk.CTkTextbox(term_card, fg_color="#0a0e14",
                                         text_color=COLORS["green"], font=FONTS["mono"],
                                         corner_radius=10)
        self.term_output.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        self.term_output.insert("1.0", f"{self.current_dir}>\n")
        
        # Input
        input_frame = ctk.CTkFrame(term_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(input_frame, text="$ ", font=FONTS["mono"],
                    text_color=COLORS["green"]).pack(side="left")
        
        self.term_input = ctk.CTkEntry(input_frame, fg_color="transparent",
                                      border_width=0, text_color=COLORS["green"],
                                      font=FONTS["mono"])
        self.term_input.pack(side="left", fill="x", expand=True)
        self.term_input.bind("<Return>", self.exec_terminal)
        self.term_input.focus_set()
    
    def show_git(self):
        """Page Git."""
        self.clear_page()
        self.set_page_title("Git", "📋")
        self.set_status("Git", "orange")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(frame, text="Git", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 20))
        
        # Actions card
        actions = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        actions.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(actions, text="  Actions Rapides", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        btn_frame = ctk.CTkFrame(actions, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        for text, cmd in [("📋 Statut", "git status"), ("📝 Diff", "git diff"),
                         ("📜 Log", "git log --oneline -10"), ("➕ Add", "git add .")]:
            ctk.CTkButton(btn_frame, text=text, font=FONTS["small"],
                         fg_color=COLORS["bg_tertiary"], text_color=COLORS["text"],
                         hover_color=COLORS["border"],
                         command=lambda c=cmd: self.run_git(c)).pack(side="left", padx=5)
        
        # Commit
        commit_frame = ctk.CTkFrame(actions, fg_color="transparent")
        commit_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.commit_entry = ctk.CTkEntry(commit_frame, placeholder_text="Message de commit...",
                                        fg_color=COLORS["bg_tertiary"],
                                        border_color=COLORS["border"],
                                        text_color=COLORS["text"],
                                        font=FONTS["mono"], height=40)
        self.commit_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(commit_frame, text="💾 Commit", font=FONTS["small"],
                     fg_color=COLORS["green"], text_color="white",
                     hover_color=COLORS["green"], command=self.git_commit).pack(side="left")
        
        # Output
        output = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        output.pack(fill="both", expand=True)
        
        ctk.CTkLabel(output, text="  Sortie", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.git_output = ctk.CTkTextbox(output, fg_color=COLORS["bg_tertiary"],
                                        text_color=COLORS["text"], font=FONTS["mono"],
                                        corner_radius=10)
        self.git_output.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def show_settings(self):
        """Page paramètres."""
        self.clear_page()
        self.set_page_title("Paramètres", "⚙")
        self.set_status("Paramètres")
        
        frame = ctk.CTkFrame(self.page_frame, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        ctk.CTkLabel(frame, text="Paramètres", font=FONTS["title"],
                    text_color=COLORS["text"]).pack(anchor="w", pady=(0, 20))
        
        # Apparence
        card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(card, text="  Apparence", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(card, text="Thème: Sombre (actuel)",
                    font=FONTS["body"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=15, pady=5)
        
        # Info
        info_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=14)
        info_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(info_card, text="  À propos", font=FONTS["heading"],
                    text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(info_card, text=f"Version: {APP_VERSION}",
                    font=FONTS["body"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=15)
        ctk.CTkLabel(info_card, text=f"Dossier: {self.current_dir}",
                    font=FONTS["mono_small"], text_color=COLORS["text_secondary"]).pack(anchor="w", padx=15, pady=5)
    
    # ═══════════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════════
    
    def action_read(self):
        path = filedialog.askopenfilename(
            title="Ouvrir un fichier",
            filetypes=[("Python", "*.py"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if path:
            self.open_file(path)
    
    def open_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.show_editor()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            self.editor_file = path
            self.file_label.configure(text=os.path.basename(path))
            self.set_status(f"Ouvert: {os.path.basename(path)}")
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
            self.file_label.configure(text=os.path.basename(path))
    
    def save_file(self):
        if self.editor_file:
            try:
                with open(self.editor_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.get("1.0", "end"))
                self.set_status(f"Sauvegardé: {os.path.basename(self.editor_file)}")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
    
    def action_search(self):
        self.show_terminal()
        # TODO: Implement search
    
    def action_analyze_code(self):
        self.show_analysis()
    
    def action_run(self):
        path = filedialog.askopenfilename(title="Script Python", filetypes=[("Python", "*.py")])
        if path:
            self.show_terminal()
            self.term_output.insert("end", f"\n$ python {path}\n")
            thread = threading.Thread(target=self._run_thread, args=(path,), daemon=True)
            thread.start()
    
    def _run_thread(self, path):
        try:
            proc = subprocess.Popen(f'python "{path}"', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=self.current_dir, text=True)
            for line in proc.stdout:
                self.after(0, lambda l=line: self.term_output.insert("end", l))
                self.after(0, lambda: self.term_output.see("end"))
            proc.wait()
        except Exception as e:
            self.after(0, lambda: self.term_output.insert("end", f"Erreur: {e}\n"))
    
    def action_train(self):
        self.show_training()
    
    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("All", "*.*")])
        if path:
            self.analysis_path.delete(0, "end")
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
{'═'*55}
  RÉSULTATS DE L'ANALYSE
{'═'*55}

  Fichier:   {os.path.basename(path)}
  Langage:   {lang}
  Taille:    {os.path.getsize(path)} bytes

{'─'*55}
  STATISTIQUES
{'─'*55}
  Lignes:      {len(lines):>8}
  Mots:        {words:>8}
  Fonctions:   {funcs:>8}
  Classes:     {classes:>8}
  Imports:     {imports}:>8
  Complexité:  {complexity:>8}

{'─'*55}
  SCORE: {min(100, max(0, 100 - (complexity * 2)))}/100
{'═'*55}
"""
            self.analysis_result.delete("1.0", "end")
            self.analysis_result.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def start_training(self):
        topic = self.topic_entry.get()
        pages = self.pages_spin.get()
        iters = self.iter_spin.get()
        
        cmd = f'python orchestrator.py --topic "{topic}" --pages {pages} --iterations {iters} --no-dashboard'
        self.training_log.insert("end", f"$ {cmd}\n\n")
        self.set_status("Entraînement en cours...", "purple")
        
        thread = threading.Thread(target=self._train_thread, args=(cmd,), daemon=True)
        thread.start()
    
    def _train_thread(self, cmd):
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, cwd=self.current_dir, text=True)
            for line in proc.stdout:
                self.after(0, lambda l=line: self.training_log.insert("end", l))
                self.after(0, lambda: self.training_log.see("end"))
            proc.wait()
            self.after(0, lambda: self.set_status("Entraînement terminé"))
        except Exception as e:
            self.after(0, lambda: self.training_log.insert("end", f"Erreur: {e}\n"))
    
    def exec_terminal(self, event):
        cmd = self.term_input.get()
        if not cmd:
            return
        self.term_input.delete(0, "end")
        self.term_output.insert("end", f"$ {cmd}\n")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.current_dir)
            if result.stdout:
                self.term_output.insert("end", result.stdout)
            if result.stderr:
                self.term_output.insert("end", result.stderr)
        except Exception as e:
            self.term_output.insert("end", f"Erreur: {e}\n")
        self.term_output.see("end")
    
    def run_git(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.current_dir)
            self.git_output.insert("end", f"$ {cmd}\n{result.stdout}\n")
            if result.stderr:
                self.git_output.insert("end", f"Erreur: {result.stderr}\n")
            self.git_output.see("end")
        except Exception as e:
            self.git_output.insert("end", f"Erreur: {e}\n")
    
    def git_commit(self):
        msg = self.commit_entry.get()
        if not msg:
            messagebox.showerror("Erreur", "Entrez un message de commit")
            return
        self.run_git("git add .")
        self.run_git(f'git commit -m "{msg}"')
        self.commit_entry.delete(0, "end")


def main():
    app = GradenIA()
    app.mainloop()


if __name__ == "__main__":
    main()
