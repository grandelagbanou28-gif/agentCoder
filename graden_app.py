"""
agentCoder - Application GUI
Interface moderne inspirée d'opencode
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# Configuration
APP_TITLE = "agentCoder"
APP_VERSION = "2.0"
BG_COLOR = "#1e1e2e"
BG_SECONDARY = "#282840"
BG_TERTIARY = "#313145"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
GREEN = "#a6e3a1"
RED = "#f38ba8"
YELLOW = "#f9e2af"
BLUE = "#89dceb"
DIM = "#6c7086"
BORDER_COLOR = "#45475a"


class AgentCoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1200x800")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(900, 600)
        
        # Try to set icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "IAtrainer.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.history = []
        self.history_index = -1
        
        self.setup_ui()
        self.showWelcome()
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Sidebar
        self.create_sidebar()
        
        # Main area
        self.create_main_area()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Crée l'en-tête de l'application."""
        header = tk.Frame(self.main_frame, bg=BG_SECONDARY, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(header, bg=BG_SECONDARY)
        title_frame.pack(side=tk.LEFT, padx=15, fill=tk.Y)
        
        tk.Label(title_frame, text="⬡", font=("Segoe UI", 18), 
                bg=BG_SECONDARY, fg=ACCENT_COLOR).pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(title_frame, text=APP_TITLE, font=("Segoe UI", 14, "bold"),
                bg=BG_SECONDARY, fg=TEXT_COLOR).pack(side=tk.LEFT)
        tk.Label(title_frame, text=f"v{APP_VERSION}", font=("Segoe UI", 9),
                bg=BG_SECONDARY, fg=DIM).pack(side=tk.LEFT, padx=(8, 0))
        
        # Right side buttons
        btn_frame = tk.Frame(header, bg=BG_SECONDARY)
        btn_frame.pack(side=tk.RIGHT, padx=10)
        
        self.create_header_btn(btn_frame, "📁", self.open_folder)
        self.create_header_btn(btn_frame, "⚙", self.show_settings)
        self.create_header_btn(btn_frame, "✕", self.root.quit)
    
    def create_header_btn(self, parent, text, command):
        btn = tk.Label(parent, text=text, font=("Segoe UI", 12),
                      bg=BG_SECONDARY, fg=TEXT_COLOR, cursor="hand2", padx=10)
        btn.pack(side=tk.LEFT, padx=2)
        btn.bind("<Enter>", lambda e: btn.configure(fg=ACCENT_COLOR))
        btn.bind("<Leave>", lambda e: btn.configure(fg=TEXT_COLOR))
        btn.bind("<Button-1>", lambda e: command())
    
    def create_sidebar(self):
        """Crée la barre latérale."""
        self.sidebar = tk.Frame(self.content_frame, bg=BG_SECONDARY, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Search box
        search_frame = tk.Frame(self.sidebar, bg=BG_SECONDARY)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               bg=BG_TERTIARY, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                               font=("Segoe UI", 10), relief=tk.FLAT)
        search_entry.pack(fill=tk.X, ipady=6)
        search_entry.insert(0, "🔍 Rechercher...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "🔍 Rechercher..." else None)
        search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, "🔍 Rechercher...") if not search_entry.get() else None)
        
        # Navigation
        nav_frame = tk.Frame(self.sidebar, bg=BG_SECONDARY)
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        nav_items = [
            ("🏠", "Accueil", self.showWelcome),
            ("🤖", "Modèles", self.showModels),
            ("📊", "Analyse", self.showAnalysis),
            ("🎯", "Entraînement", self.showTraining),
            ("📁", "Fichiers", self.showFiles),
            ("📋", "Git", self.showGit),
            ("💻", "Terminal", self.showTerminal),
            ("⚙", "Paramètres", self.show_settings),
        ]
        
        for icon, text, command in nav_items:
            item = tk.Frame(nav_frame, bg=BG_SECONDARY, cursor="hand2")
            item.pack(fill=tk.X, pady=1)
            
            lbl = tk.Label(item, text=f" {icon}  {text}", font=("Segoe UI", 11),
                          bg=BG_SECONDARY, fg=TEXT_COLOR, anchor="w", padx=10, pady=8)
            lbl.pack(fill=tk.X)
            
            item.bind("<Enter>", lambda e, i=item, l=lbl: (i.configure(bg=BG_TERTIARY), l.configure(bg=BG_TERTIARY)))
            item.bind("<Leave>", lambda e, i=item, l=lbl: (i.configure(bg=BG_SECONDARY), l.configure(bg=BG_SECONDARY)))
            item.bind("<Button-1>", lambda e, cmd=command: cmd())
            lbl.bind("<Button-1>", lambda e, cmd=command: cmd())
    
    def create_main_area(self):
        """Crée la zone principale."""
        self.main_area = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """Crée la barre de statut."""
        self.status_bar = tk.Frame(self.main_frame, bg=BG_SECONDARY, height=28)
        self.status_bar.pack(fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar, text=" ✓ Prêt", 
                                    font=("Segoe UI", 9), bg=BG_SECONDARY, fg=GREEN)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.dir_label = tk.Label(self.status_bar, text=f"📁 {self.current_dir}",
                                 font=("Segoe UI", 9), bg=BG_SECONDARY, fg=DIM)
        self.dir_label.pack(side=tk.RIGHT, padx=10)
    
    def clear_main_area(self):
        """Efface la zone principale."""
        for widget in self.main_area.winfo_children():
            widget.destroy()
    
    def showWelcome(self):
        """Affiche l'écran d'accueil."""
        self.clear_main_area()
        
        # Welcome content
        welcome_frame = tk.Frame(self.main_area, bg=BG_COLOR)
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Logo
        tk.Label(welcome_frame, text="⬡", font=("Segoe UI", 60),
                bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=(20, 10))
        tk.Label(welcome_frame, text=APP_TITLE, font=("Segoe UI", 28, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack()
        tk.Label(welcome_frame, text="Assistant CLI pour le développement logiciel",
                font=("Segoe UI", 12), bg=BG_COLOR, fg=DIM).pack(pady=(5, 30))
        
        # Quick actions
        actions_frame = tk.Frame(welcome_frame, bg=BG_COLOR)
        actions_frame.pack(fill=tk.X)
        
        tk.Label(actions_frame, text="Actions rapides", font=("Segoe UI", 14, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 15))
        
        actions = [
            ("📖", "Lire un fichier", "Lire et analyser un fichier code", self.action_read),
            ("✏️", "Écrire du code", "Créer ou modifier un fichier", self.action_write),
            ("🔎", "Rechercher", "Trouver du texte dans les fichiers", self.action_search),
            ("📊", "Analyser", "Analyser la qualité du code", self.action_analyze),
            ("▶️", "Exécuter", "Lancer un script Python", self.action_run),
            ("🎯", "Entraîner", "Lancer l'entraînement du modèle", self.action_train),
        ]
        
        for icon, title, desc, command in actions:
            card = tk.Frame(actions_frame, bg=BG_SECONDARY, cursor="hand2")
            card.pack(fill=tk.X, pady=4)
            
            content = tk.Frame(card, bg=BG_SECONDARY)
            content.pack(fill=tk.X, padx=15, pady=12)
            
            tk.Label(content, text=icon, font=("Segoe UI", 18),
                    bg=BG_SECONDARY, fg=ACCENT_COLOR).pack(side=tk.LEFT, padx=(0, 15))
            
            text_frame = tk.Frame(content, bg=BG_SECONDARY)
            text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(text_frame, text=title, font=("Segoe UI", 12, "bold"),
                    bg=BG_SECONDARY, fg=TEXT_COLOR).pack(anchor="w")
            tk.Label(text_frame, text=desc, font=("Segoe UI", 9),
                    bg=BG_SECONDARY, fg=DIM).pack(anchor="w")
            
            card.bind("<Enter>", lambda e, c=card: c.configure(bg=BG_TERTIARY))
            card.bind("<Leave>", lambda e, c=card: c.configure(bg=BG_SECONDARY))
            card.bind("<Button-1>", lambda e, cmd=command: cmd())
            for child in content.winfo_children():
                child.bind("<Button-1>", lambda e, cmd=command: cmd())
                for subchild in child.winfo_children():
                    subchild.bind("<Button-1>", lambda e, cmd=command: cmd())
        
        # Keyboard shortcuts
        shortcuts_frame = tk.Frame(welcome_frame, bg=BG_COLOR)
        shortcuts_frame.pack(fill=tk.X, pady=(30, 0))
        
        tk.Label(shortcuts_frame, text="Raccourcis clavier", font=("Segoe UI", 14, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 10))
        
        shortcuts = [
            ("Ctrl+O", "Ouvrir un fichier"),
            ("Ctrl+S", "Sauvegarder"),
            ("Ctrl+F", "Rechercher"),
            ("F5", "Exécuter"),
            ("Ctrl+Shift+T", "Entraîner"),
        ]
        
        for key, desc in shortcuts:
            sc = tk.Frame(shortcuts_frame, bg=BG_COLOR)
            sc.pack(fill=tk.X, pady=2)
            
            tk.Label(sc, text=key, font=("Consolas", 10), bg=BG_TERTIARY, 
                    fg=ACCENT_COLOR, padx=8, pady=2).pack(side=tk.LEFT)
            tk.Label(sc, text=f"  {desc}", font=("Segoe UI", 10),
                    bg=BG_COLOR, fg=DIM).pack(side=tk.LEFT)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.action_read())
        self.root.bind("<Control-s>", lambda e: self.action_write())
        self.root.bind("<Control-f>", lambda e: self.action_search())
        self.root.bind("<F5>", lambda e: self.action_run())
    
    def showModels(self):
        """Affiche la gestion des modèles."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="🤖 Gestion des Modèles", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Models list
        models_frame = tk.Frame(frame, bg=BG_SECONDARY)
        models_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(models_frame, text="Modèles disponibles", font=("Segoe UI", 12, "bold"),
                bg=BG_SECONDARY, fg=TEXT_COLOR).pack(anchor="w", padx=15, pady=(15, 10))
        
        models_dir = os.path.join(self.current_dir, "models")
        if os.path.exists(models_dir):
            for root_dir, dirs, files in os.walk(models_dir):
                level = root_dir.replace(models_dir, '').count(os.sep)
                if level > 2:
                    continue
                indent = '  ' * level
                folder_name = os.path.basename(root_dir)
                
                item = tk.Frame(models_frame, bg=BG_SECONDARY)
                item.pack(fill=tk.X, padx=15, pady=2)
                
                tk.Label(item, text=f"{indent}📁 {folder_name}", font=("Consolas", 10),
                        bg=BG_SECONDARY, fg=BLUE, anchor="w").pack(side=tk.LEFT, padx=10, pady=4)
        else:
            tk.Label(models_frame, text="Aucun modèle trouvé", font=("Segoe UI", 10),
                    bg=BG_SECONDARY, fg=DIM).pack(pady=20)
        
        # Action buttons
        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.create_button(btn_frame, "🔄 Rafraîchir", self.showModels)
        self.create_button(btn_list_frame, "📥 Télécharger", self.action_download_model)
    
    def showAnalysis(self):
        """Affiche l'analyse de code."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="📊 Analyse de Code", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Input area
        input_frame = tk.Frame(frame, bg=BG_SECONDARY)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(input_frame, text="Chemin du fichier à analyser:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR, anchor="w").pack(fill=tk.X, padx=15, pady=(15, 5))
        
        path_frame = tk.Frame(input_frame, bg=BG_SECONDARY)
        path_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.analysis_path = tk.Entry(path_frame, bg=BG_TERTIARY, fg=TEXT_COLOR,
                                     insertbackground=TEXT_COLOR, font=("Consolas", 10),
                                     relief=tk.FLAT)
        self.analysis_path.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        
        self.create_button(path_frame, "📂", self.browse_file)
        self.create_button(path_frame, "📊 Analyser", self.run_analysis)
        
        # Results area
        self.analysis_result = scrolledtext.ScrolledText(input_frame, bg=BG_TERTIARY, 
                                                        fg=TEXT_COLOR, font=("Consolas", 10),
                                                        relief=tk.FLAT, wrap=tk.WORD)
        self.analysis_result.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def showTraining(self):
        """Affiche l'interface d'entraînement."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="🎯 Entraînement du Modèle", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Training form
        form_frame = tk.Frame(frame, bg=BG_SECONDARY)
        form_frame.pack(fill=tk.X)
        
        # Topic
        tk.Label(form_frame, text="Sujet d'entraînement:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR, anchor="w").pack(fill=tk.X, padx=15, pady=(15, 5))
        self.topic_entry = tk.Entry(form_frame, bg=BG_TERTIARY, fg=TEXT_COLOR,
                                   insertbackground=TEXT_COLOR, font=("Consolas", 10),
                                   relief=tk.FLAT)
        self.topic_entry.pack(fill=tk.X, padx=15, ipady=6)
        self.topic_entry.insert(0, "Unity game development best practices")
        
        # Pages and iterations
        params_frame = tk.Frame(form_frame, bg=BG_SECONDARY)
        params_frame.pack(fill=tk.X, padx=15, pady=(15, 0))
        
        tk.Label(params_frame, text="Pages:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.pages_spin = tk.Spinbox(params_frame, from_=1, to=20, width=5,
                                     bg=BG_TERTIARY, fg=TEXT_COLOR, font=("Consolas", 10))
        self.pages_spin.pack(side=tk.LEFT, padx=(5, 20))
        self.pages_spin.delete(0, tk.END)
        self.pages_spin.insert(0, "3")
        
        tk.Label(params_frame, text="Itérations:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR).pack(side=tk.LEFT)
        self.iter_spin = tk.Spinbox(params_frame, from_=1, to=20, width=5,
                                    bg=BG_TERTIARY, fg=TEXT_COLOR, font=("Consolas", 10))
        self.iter_spin.pack(side=tk.LEFT, padx=(5, 0))
        self.iter_spin.delete(0, tk.END)
        self.iter_spin.insert(0, "3")
        
        # Code only checkbox
        self.code_only_var = tk.BooleanVar()
        tk.Checkbutton(form_frame, text="Code only (scraping de code uniquement)",
                      variable=self.code_only_var, bg=BG_SECONDARY, fg=TEXT_COLOR,
                      selectcolor=BG_TERTIARY, font=("Segoe UI", 10)).pack(fill=tk.X, padx=15, pady=(15, 0))
        
        # Start button
        btn_frame = tk.Frame(form_frame, bg=BG_SECONDARY)
        btn_frame.pack(fill=tk.X, padx=15, pady=(20, 15))
        
        self.create_button(btn_frame, "🎯 Lancer l'entraînement", self.start_training, large=True)
        
        # Log area
        tk.Label(frame, text="Journal:", font=("Segoe UI", 12, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(20, 10))
        
        self.training_log = scrolledtext.ScrolledText(frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                                     font=("Consolas", 10), relief=tk.FLAT,
                                                     wrap=tk.WORD, height=12)
        self.training_log.pack(fill=tk.BOTH, expand=True)
    
    def showFiles(self):
        """Affiche l'explorateur de fichiers."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="📁 Explorateur de Fichiers", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # File tree
        tree_frame = tk.Frame(frame, bg=BG_SECONDARY)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_tree = tk.Frame(tree_frame, bg=BG_SECONDARY)
        self.file_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.load_file_tree(self.current_dir, self.file_tree)
    
    def load_file_tree(self, path, parent, level=0):
        """Charge l'arborescence des fichiers."""
        if level > 3:
            return
        
        try:
            items = sorted(os.listdir(path))
            for item in items:
                if item.startswith('.') or item == '__pycache__':
                    continue
                
                full_path = os.path.join(path, item)
                is_dir = os.path.isdir(full_path)
                
                item_frame = tk.Frame(parent, bg=BG_SECONDARY)
                item_frame.pack(fill=tk.X, padx=level * 20, pady=1)
                
                icon = "📁" if is_dir else "📄"
                color = BLUE if is_dir else TEXT_COLOR
                
                lbl = tk.Label(item_frame, text=f" {icon} {item}", font=("Consolas", 10),
                              bg=BG_SECONDARY, fg=color, anchor="w", cursor="hand2")
                lbl.pack(fill=tk.X, padx=10, pady=3)
                
                if is_dir:
                    lbl.bind("<Button-1>", lambda e, p=full_path: self.load_file_tree(p, parent))
                else:
                    lbl.bind("<Button-1>", lambda e, p=full_path: self.open_file(p))
        except PermissionError:
            pass
    
    def showGit(self):
        """Affiche les opérations Git."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="📋 Git", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Git buttons
        btn_frame = tk.Frame(frame, bg=BG_SECONDARY)
        btn_frame.pack(fill=tk.X)
        
        git_actions = [
            ("📋 Statut", "git status", self.current_dir),
            ("📝 Diff", "git diff", self.current_dir),
            ("📜 Log", "git log --oneline -10", self.current_dir),
            ("➕ Ajouter tout", "git add .", self.current_dir),
        ]
        
        for text, cmd, path in git_actions:
            btn = tk.Button(btn_frame, text=text, font=("Segoe UI", 10),
                          bg=BG_TERTIARY, fg=TEXT_COLOR, activebackground=BORDER_COLOR,
                          activeforeground=TEXT_COLOR, relief=tk.FLAT, cursor="hand2",
                          command=lambda c=cmd, p=path: self.run_git_command(c, p))
            btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Commit section
        commit_frame = tk.Frame(frame, bg=BG_SECONDARY)
        commit_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(commit_frame, text="Message de commit:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR, anchor="w").pack(fill=tk.X, padx=15, pady=(15, 5))
        
        self.commit_msg = tk.Entry(commit_frame, bg=BG_TERTIARY, fg=TEXT_COLOR,
                                  insertbackground=TEXT_COLOR, font=("Consolas", 10),
                                  relief=tk.FLAT)
        self.commit_msg.pack(fill=tk.X, padx=15, ipady=6)
        
        self.create_button(commit_frame, "💾 Commit", self.git_commit)
        
        # Git output
        tk.Label(frame, text="Sortie:", font=("Segoe UI", 12, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(20, 10))
        
        self.git_output = scrolledtext.ScrolledText(frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                                   font=("Consolas", 10), relief=tk.FLAT,
                                                   wrap=tk.WORD, height=10)
        self.git_output.pack(fill=tk.BOTH, expand=True)
    
    def showTerminal(self):
        """Affiche un terminal intégré."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="💻 Terminal", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Terminal output
        self.terminal_output = scrolledtext.ScrolledText(frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                                        font=("Consolas", 10), relief=tk.FLAT,
                                                        wrap=tk.WORD)
        self.terminal_output.pack(fill=tk.BOTH, expand=True)
        self.terminal_output.insert(tk.END, f"{self.current_dir}>\n")
        
        # Input frame
        input_frame = tk.Frame(frame, bg=BG_SECONDARY)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(input_frame, text="$", font=("Consolas", 10),
                bg=BG_SECONDARY, fg=GREEN).pack(side=tk.LEFT, padx=(10, 5))
        
        self.terminal_input = tk.Entry(input_frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                      insertbackground=TEXT_COLOR, font=("Consolas", 10),
                                      relief=tk.FLAT)
        self.terminal_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.terminal_input.bind("<Return>", self.execute_terminal_command)
    
    def show_settings(self):
        """Affiche les paramètres."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="⚙ Paramètres", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        settings_frame = tk.Frame(frame, bg=BG_SECONDARY)
        settings_frame.pack(fill=tk.X)
        
        # Theme
        tk.Label(settings_frame, text="Thème:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR, anchor="w").pack(fill=tk.X, padx=15, pady=(15, 5))
        
        theme_frame = tk.Frame(settings_frame, bg=BG_SECONDARY)
        theme_frame.pack(fill=tk.X, padx=15)
        
        for theme in ["Sombre", "Clair", "Bleu"]:
            rb = tk.Radiobutton(theme_frame, text=theme, variable=tk.StringVar(),
                               value=theme, bg=BG_SECONDARY, fg=TEXT_COLOR,
                               selectcolor=BG_TERTIARY, font=("Segoe UI", 10))
            rb.pack(side=tk.LEFT, padx=(0, 15))
    
    # ═══════════════════════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════════════════════
    
    def action_read(self):
        """Action: Lire un fichier."""
        path = filedialog.askopenfilename(
            title="Ouvrir un fichier",
            filetypes=[("Python", "*.py"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if path:
            self.open_file(path)
    
    def open_file(self, path):
        """Ouvre et affiche un fichier."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.clear_main_area()
            
            frame = tk.Frame(self.main_area, bg=BG_COLOR)
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
            
            # Header
            header = tk.Frame(frame, bg=BG_SECONDARY)
            header.pack(fill=tk.X)
            
            tk.Label(header, text=f"📖 {os.path.basename(path)}", 
                    font=("Segoe UI", 12, "bold"), bg=BG_SECONDARY, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=10, pady=8)
            tk.Label(header, text=path, font=("Consolas", 9), 
                    bg=BG_SECONDARY, fg=DIM).pack(side=tk.RIGHT, padx=10)
            
            # Content
            text_widget = scrolledtext.ScrolledText(frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                                   font=("Consolas", 11), relief=tk.FLAT,
                                                   wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            
            # Stats
            lines = content.split('\n')
            words = len(content.split())
            self.status_label.config(text=f" ✓ {len(lines)} lignes | {words} mots | {os.path.getsize(path)} bytes")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier:\n{e}")
    
    def action_write(self):
        """Action: Écrire du code."""
        path = filedialog.asksaveasfilename(
            title="Sauvegarder le fichier",
            defaultextension=".py",
            filetypes=[("Python", "*.py"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if path:
            self.open_file_for_edit(path)
    
    def open_file_for_edit(self, path):
        """Ouvre un fichier pour édition."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Header
        header = tk.Frame(frame, bg=BG_SECONDARY)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"✏️ {os.path.basename(path)}", 
                font=("Segoe UI", 12, "bold"), bg=BG_SECONDARY, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=10, pady=8)
        
        # Editor
        self.editor = scrolledtext.ScrolledText(frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                               font=("Consolas", 11), relief=tk.FLAT,
                                               wrap=tk.WORD, undo=True)
        self.editor.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Try to load existing content
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.insert(tk.END, f.read())
            except:
                pass
        
        self.editor.current_file = path
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.create_button(btn_frame, "💾 Sauvegarder", self.save_file)
    
    def save_file(self):
        """Sauvegarde le fichier en cours d'édition."""
        if hasattr(self.editor, 'current_file'):
            try:
                content = self.editor.get("1.0", tk.END)
                with open(self.editor.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_label.config(text=f" ✓ Sauvegardé: {self.editor.current_file}")
                messagebox.showinfo("Succès", "Fichier sauvegardé!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de sauvegarde:\n{e}")
    
    def action_search(self):
        """Action: Rechercher."""
        self.clear_main_area()
        
        frame = tk.Frame(self.main_area, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(frame, text="🔎 Rechercher dans les fichiers", font=("Segoe UI", 18, "bold"),
                bg=BG_COLOR, fg=TEXT_COLOR).pack(anchor="w", pady=(0, 20))
        
        # Search input
        search_frame = tk.Frame(frame, bg=BG_SECONDARY)
        search_frame.pack(fill=tk.X)
        
        tk.Label(search_frame, text="Texte:", font=("Segoe UI", 10),
                bg=BG_SECONDARY, fg=TEXT_COLOR, anchor="w").pack(fill=tk.X, padx=15, pady=(15, 5))
        
        self.search_text = tk.Entry(search_frame, bg=BG_TERTIARY, fg=TEXT_COLOR,
                                   insertbackground=TEXT_COLOR, font=("Consolas", 10),
                                   relief=tk.FLAT)
        self.search_text.pack(fill=tk.X, padx=15, ipady=6)
        
        self.create_button(search_frame, "🔎 Rechercher", self.run_search)
        
        # Results
        self.search_results = scrolledtext.ScrolledText(frame, bg=BG_SECONDARY, fg=TEXT_COLOR,
                                                       font=("Consolas", 10), relief=tk.FLAT,
                                                       wrap=tk.WORD)
        self.search_results.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
    
    def action_analyze(self):
        """Action: Analyser un fichier."""
        self.showAnalysis()
    
    def action_run(self):
        """Action: Exécuter un script."""
        path = filedialog.askopenfilename(
            title="Sélectionner un script Python",
            filetypes=[("Python", "*.py")]
        )
        if path:
            self.run_script(path)
    
    def action_train(self):
        """Action: Entraîner le modèle."""
        self.showTraining()
    
    def action_download_model(self):
        """Action: Télécharger un modèle."""
        messagebox.showinfo("Téléchargement", "Utilisez Ollama pour télécharger des modèles:\n\nollama pull <model_name>")
    
    def browse_file(self):
        """Parcourt les fichiers."""
        path = filedialog.askopenfilename(
            title="Sélectionner un fichier",
            filetypes=[("Python", "*.py"), ("All", "*.*")]
        )
        if path:
            self.analysis_path.delete(0, tk.END)
            self.analysis_path.insert(0, path)
    
    # ═══════════════════════════════════════════════════════════
    # EXÉCUTION
    # ═══════════════════════════════════════════════════════════
    
    def run_analysis(self):
        """Exécute l'analyse d'un fichier."""
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
                       '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#'}
            lang = lang_map.get(ext, 'Inconnu')
            
            score = 100
            if funcs == 0 and len(lines) > 50: score -= 10
            if imports == 0 and len(lines) > 20: score -= 5
            if content.count('#') == 0 and len(lines) > 30: score -= 10
            
            result = f"""
╔══════════════════════════════════════════════════════════╗
║              RÉSULTATS DE L'ANALYSE                      ║
╚══════════════════════════════════════════════════════════╝

📁 Fichier: {os.path.basename(path)}
📁 Chemin:  {path}
🌐 Langage: {lang}

┌──────────────────────────────────────────────────────────┐
│ STATISTIQUES                                             │
├──────────────────────────────────────────────────────────┤
│  Lignes:      {len(lines):>8}                                   │
│  Mots:        {words:>8}                                   │
│  Fonctions:   {funcs:>8}                                   │
│  Classes:     {classes:>8}                                   │
│  Imports:     {imports:>8}                                   │
│  Complexité:  {complexity:>8}                                   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ SCORE DE QUALITÉ: {score}/100                                  │
└──────────────────────────────────────────────────────────┘
"""
            self.analysis_result.delete("1.0", tk.END)
            self.analysis_result.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def start_training(self):
        """Lance l'entraînement."""
        topic = self.topic_entry.get()
        pages = self.pages_spin.get()
        iterations = self.iter_spin.get()
        code_only = self.code_only_var.get()
        
        cmd = f'python orchestrator.py --topic "{topic}" --pages {pages} --iterations {iterations} --no-dashboard'
        if code_only:
            cmd += " --code-only"
        
        self.training_log.insert(tk.END, f"$ {cmd}\n\n")
        self.status_label.config(text=" ⏳ Entraînement en cours...")
        
        thread = threading.Thread(target=self.run_training_thread, args=(cmd,))
        thread.daemon = True
        thread.start()
    
    def run_training_thread(self, cmd):
        """Exécute l'entraînement dans un thread séparé."""
        try:
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                cwd=self.current_dir, text=True
            )
            
            for line in process.stdout:
                self.root.after(0, self.append_training_log, line)
            
            process.wait()
            
            self.root.after(0, lambda: self.status_label.config(text=" ✓ Entraînement terminé"))
        except Exception as e:
            self.root.after(0, lambda: self.training_log.insert(tk.END, f"\nErreur: {e}\n"))
    
    def append_training_log(self, text):
        """Ajoute du texte au journal d'entraînement."""
        self.training_log.insert(tk.END, text)
        self.training_log.see(tk.END)
    
    def run_script(self, path):
        """Exécute un script Python."""
        self.showTerminal()
        self.terminal_output.insert(tk.END, f"\n$ python {path}\n")
        
        thread = threading.Thread(target=self.run_script_thread, args=(path,))
        thread.daemon = True
        thread.start()
    
    def run_script_thread(self, path):
        """Exécute un script dans un thread."""
        try:
            process = subprocess.Popen(
                f'python "{path}"', shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, cwd=self.current_dir, text=True
            )
            
            for line in process.stdout:
                self.root.after(0, lambda l=line: self.terminal_output.insert(tk.END, l))
                self.root.after(0, lambda: self.terminal_output.see(tk.END))
            
            process.wait()
        except Exception as e:
            self.root.after(0, lambda: self.terminal_output.insert(tk.END, f"\nErreur: {e}\n"))
    
    def run_git_command(self, cmd, path):
        """Exécute une commande Git."""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=path)
            self.git_output.insert(tk.END, f"$ {cmd}\n{result.stdout}\n")
            if result.stderr:
                self.git_output.insert(tk.END, f"Erreur: {result.stderr}\n")
            self.git_output.see(tk.END)
        except Exception as e:
            self.git_output.insert(tk.END, f"Erreur: {e}\n")
    
    def git_commit(self):
        """Fait un commit Git."""
        msg = self.commit_msg.get()
        if not msg:
            messagebox.showerror("Erreur", "Entrez un message de commit")
            return
        
        self.run_git_command(f'git add .', self.current_dir)
        self.run_git_command(f'git commit -m "{msg}"', self.current_dir)
        self.commit_msg.delete(0, tk.END)
    
    def run_search(self):
        """Exécute une recherche."""
        pattern = self.search_text.get()
        if not pattern:
            return
        
        self.search_results.delete("1.0", tk.END)
        self.search_results.insert(tk.END, f"Recherche de '{pattern}'...\n\n")
        
        found = 0
        for root_dir, dirs, files in os.walk(self.current_dir):
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
            for file in files:
                filepath = os.path.join(root_dir, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, 1):
                            if pattern.lower() in line.lower():
                                self.search_results.insert(tk.END, 
                                    f"  {filepath}:{i} {line.rstrip()[:80]}\n")
                                found += 1
                                if found > 50:
                                    self.search_results.insert(tk.END, "\nArrêt après 50 résultats\n")
                                    return
                except:
                    pass
        
        self.search_results.insert(tk.END, f"\nTrouvé dans {found} ligne(s)")
    
    def execute_terminal_command(self, event):
        """Exécute une commande du terminal."""
        cmd = self.terminal_input.get()
        if not cmd:
            return
        
        self.terminal_input.delete(0, tk.END)
        self.terminal_output.insert(tk.END, f"$ {cmd}\n")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.current_dir)
            if result.stdout:
                self.terminal_output.insert(tk.END, result.stdout)
            if result.stderr:
                self.terminal_output.insert(tk.END, result.stderr)
        except Exception as e:
            self.terminal_output.insert(tk.END, f"Erreur: {e}\n")
        
        self.terminal_output.see(tk.END)
    
    def open_folder(self):
        """Ouvre un dossier."""
        path = filedialog.askdirectory(title="Sélectionner un dossier")
        if path:
            self.current_dir = path
            self.dir_label.config(text=f"📁 {path}")
            self.status_label.config(text=f" ✓ Dossier: {path}")
    
    def create_button(self, parent, text, command, large=False):
        """Crée un bouton stylisé."""
        font_size = 11 if large else 10
        btn = tk.Button(parent, text=text, font=("Segoe UI", font_size),
                       bg=ACCENT_COLOR, fg=BG_COLOR, activebackground=BLUE,
                       activeforeground=BG_COLOR, relief=tk.FLAT, cursor="hand2",
                       command=command, padx=15 if large else 10, pady=8 if large else 4)
        btn.pack(side=tk.LEFT if not large else tk.TOP, padx=5, pady=5)
        return btn


def main():
    root = tk.Tk()
    app = AgentCoderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
