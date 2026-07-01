"""
Grden IA v4.0 - Application GUI Professionnelle
Chat IA comme ChatGPT avec support projet direct
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk
import os
import subprocess
import threading
import time
import re
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

APP_NAME = "Grden IA"
APP_VERSION = "4.0.0"
APP_SUBTITLE = "Intelligence Artificielle pour Développeurs"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

C = {
    "bg": "#0a0a12", "bg2": "#12121e", "bg3": "#1a1a2e", "bg4": "#222240",
    "card": "#16162a", "border": "#2a2a4a", "text": "#f0f0ff", "text2": "#9090b0",
    "text3": "#606080", "accent": "#6c5ce7", "accent2": "#a29bfe", "accent3": "#5a4bd1",
    "green": "#00d68f", "green2": "#00b377", "red": "#ff4757", "yellow": "#ffc048",
    "blue": "#339af0", "cyan": "#22d3ee", "orange": "#ff922b", "pink": "#f06595",
    "purple": "#9775fa", "code_bg": "#0d1117", "code_border": "#30363d",
}

F = {
    "logo": ("Segoe UI", 36, "bold"), "title": ("Segoe UI", 24, "bold"),
    "h1": ("Segoe UI", 18, "bold"), "h2": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 12), "small": ("Segoe UI", 10), "tiny": ("Segoe UI", 9),
    "mono": ("Cascadia Code", 12), "mono_s": ("Cascadia Code", 10),
    "mono_t": ("Cascadia Code", 9), "code": ("Cascadia Code", 11),
}


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
        self.project_files = []
        self.current_file = None
        self.chat_history = []
        self.conversations = [{"title": "Nouvelle conversation", "messages": []}]
        self.current_conv = 0
        
        self.build_ui()
        self.show_chat()
    
    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.build_sidebar()
        self.build_main()
    
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=C["bg2"], width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=15, pady=(20, 10))
        
        logo = ctk.CTkFrame(logo_frame, fg_color=C["accent"], width=42, height=42, corner_radius=12)
        logo.pack(side="left")
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 18, "bold"), text_color="white").pack(expand=True)
        
        name = ctk.CTkFrame(logo_frame, fg_color="transparent")
        name.pack(side="left", padx=(12, 0))
        ctk.CTkLabel(name, text=APP_NAME, font=F["h2"], text_color=C["text"]).pack(anchor="w")
        ctk.CTkLabel(name, text=f"v{APP_VERSION}", font=F["tiny"], text_color=C["accent2"]).pack(anchor="w")
        
        # New chat button
        ctk.CTkButton(self.sidebar, text="＋  Nouvelle Conversation", font=F["h2"],
                     fg_color=C["accent"], text_color="white", hover_color=C["accent2"],
                     height=48, corner_radius=12, command=self.new_chat).pack(fill="x", padx=15, pady=(20, 10))
        
        # Search
        self.search_var = ctk.StringVar()
        search = ctk.CTkEntry(self.sidebar, placeholder_text="🔍 Rechercher...",
                             textvariable=self.search_var, fg_color=C["bg3"],
                             border_color=C["border"], text_color=C["text"],
                             font=F["body"], height=40, corner_radius=10)
        search.pack(fill="x", padx=15, pady=(0, 10))
        
        # Conversations list
        self.conv_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.conv_frame.pack(fill="both", expand=True, padx=10)
        
        self.update_conv_list()
        
        # Project section
        ctk.CTkFrame(self.sidebar, fg_color=C["border"], height=1).pack(fill="x", padx=15, pady=10)
        
        proj_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        proj_header.pack(fill="x", padx=15)
        
        ctk.CTkLabel(proj_header, text="📁  PROJET", font=F["small"],
                    text_color=C["text3"]).pack(side="left")
        
        ctk.CTkButton(proj_header, text="📂 Ouvrir", font=F["tiny"],
                     fg_color=C["bg3"], text_color=C["text2"], hover_color=C["border"],
                     width=70, height=28, command=self.open_project).pack(side="right")
        
        self.proj_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", height=150)
        self.proj_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        # Nav buttons at bottom
        ctk.CTkFrame(self.sidebar, fg_color=C["border"], height=1).pack(fill="x", padx=15, pady=(5, 10))
        
        nav = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav.pack(fill="x", padx=15, pady=(0, 15))
        nav.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        for i, (icon, cmd) in enumerate([
            ("🏠", self.show_home), ("📊", self.show_dashboard),
            ("📝", self.show_editor), ("⚙", self.show_settings)
        ]):
            btn = ctk.CTkButton(nav, text=icon, font=("Segoe UI", 16),
                               fg_color=C["bg3"], text_color=C["text2"],
                               hover_color=C["border"], width=50, height=40,
                               corner_radius=10, command=cmd)
            btn.grid(row=0, column=i, padx=3, sticky="nsew")
    
    def update_conv_list(self):
        for w in self.conv_frame.winfo_children():
            w.destroy()
        
        for i, conv in enumerate(self.conversations):
            frame = ctk.CTkFrame(self.conv_frame, fg_color="transparent", height=42, corner_radius=8)
            frame.pack(fill="x", pady=2)
            frame.pack_propagate(False)
            
            btn = ctk.CTkButton(frame, text=f"💬  {conv['title'][:25]}",
                               font=F["body"], fg_color="transparent",
                               text_color=C["text2"], hover_color=C["bg3"],
                               anchor="w", command=lambda idx=i: self.switch_conv(idx))
            btn.pack(fill="x", padx=5)
            
            if i == self.current_conv:
                btn.configure(fg_color=C["bg3"], text_color=C["text"])
    
    def switch_conv(self, idx):
        self.current_conv = idx
        self.update_conv_list()
        self.render_chat()
    
    def new_chat(self):
        self.conversations.append({"title": "Nouvelle conversation", "messages": []})
        self.current_conv = len(self.conversations) - 1
        self.update_conv_list()
        self.render_chat()
    
    def build_main(self):
        self.main = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)
        
        self.page = ctk.CTkFrame(self.main, fg_color="transparent")
        self.page.grid(row=0, column=0, sticky="nsew")
    
    def clear_page(self):
        for w in self.page.winfo_children():
            w.destroy()
    
    # ═══════════════════════════════════════════════════════════════
    # CHAT - Interface professionnelle type ChatGPT
    # ═══════════════════════════════════════════════════════════════
    
    def show_chat(self):
        self.clear_page()
        
        # Main chat container
        chat = ctk.CTkFrame(self.page, fg_color="transparent")
        chat.grid(row=0, column=0, sticky="nsew")
        chat.grid_rowconfigure(0, weight=1)
        chat.grid_columnconfigure(0, weight=1)
        
        # Messages area (scrollable)
        self.msg_area = ctk.CTkScrollableFrame(chat, fg_color=C["bg"],
                                               scrollbar_button_color=C["border"],
                                               scrollbar_button_hover_color=C["text3"])
        self.msg_area.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Input area
        input_frame = ctk.CTkFrame(chat, fg_color=C["bg"], height=120)
        input_frame.grid(row=1, column=0, sticky="sew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Centered input container
        center = ctk.CTkFrame(input_frame, fg_color="transparent")
        center.grid(row=0, column=0, sticky="ew", padx=100, pady=(0, 20))
        center.grid_columnconfigure(0, weight=1)
        
        # Input box
        inp_box = ctk.CTkFrame(center, fg_color=C["card"], corner_radius=16,
                               border_width=1, border_color=C["border"])
        inp_box.grid(row=0, column=0, sticky="ew")
        inp_box.grid_columnconfigure(0, weight=1)
        
        # Text input
        self.chat_input = ctk.CTkTextbox(inp_box, fg_color="transparent",
                                         text_color=C["text"], font=F["body"],
                                         height=50, wrap="word", corner_radius=12)
        self.chat_input.grid(row=0, column=0, sticky="ew", padx=(15, 60), pady=10)
        self.chat_input.bind("<Return>", lambda e: self.send_message() if not e.state & 0x1 else None)
        
        # Send button
        send = ctk.CTkButton(inp_box, text="↑", font=("Segoe UI", 18, "bold"),
                            fg_color=C["accent"], text_color="white",
                            hover_color=C["accent2"], width=40, height=40,
                            corner_radius=20, command=self.send_message)
        send.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Bottom bar
        bottom = ctk.CTkFrame(center, fg_color="transparent")
        bottom.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        
        # Quick actions
        for text, cmd in [("📁 Ouvrir fichier", self.attach_file),
                         ("📊 Analyser", self.quick_analyze),
                         ("⚡ Terminal", self.quick_terminal)]:
            ctk.CTkButton(bottom, text=text, font=F["tiny"],
                         fg_color=C["bg3"], text_color=C["text3"],
                         hover_color=C["border"], height=28,
                         command=cmd).pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(bottom, text="⇧Entrée pour une nouvelle ligne",
                    font=F["tiny"], text_color=C["text3"]).pack(side="right")
        
        # Render existing messages
        self.render_chat()
    
    def render_chat(self):
        for w in self.msg_area.winfo_children():
            w.destroy()
        
        conv = self.conversations[self.current_conv]
        
        if not conv["messages"]:
            # Welcome screen
            self.show_welcome()
            return
        
        for msg in conv["messages"]:
            if msg["role"] == "user":
                self.render_user_msg(msg["content"], msg.get("file"))
            else:
                self.render_ai_msg(msg["content"])
    
    def show_welcome(self):
        welcome = ctk.CTkFrame(self.msg_area, fg_color="transparent")
        welcome.pack(fill="both", expand=True, pady=100)
        
        logo = ctk.CTkFrame(welcome, fg_color=C["accent"], width=80, height=80, corner_radius=22)
        logo.pack(pady=(0, 20))
        logo.pack_propagate(False)
        ctk.CTkLabel(logo, text="G", font=("Segoe UI", 36, "bold"), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(welcome, text=f"Bonjour, comment puis-je vous aider ?", font=F["title"],
                    text_color=C["text"]).pack()
        
        # Suggestion cards
        suggestions = ctk.CTkFrame(welcome, fg_color="transparent")
        suggestions.pack(pady=30)
        suggestions.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, (icon, title, desc) in enumerate([
            ("💡", "Générer du code", "Créer des fonctions, classes..."),
            ("🔍", "Analyser un fichier", "Évaluer la qualité du code"),
            ("🐛", "Corriger une erreur", "Debug et résolution de bugs"),
        ]):
            card = ctk.CTkFrame(suggestions, fg_color=C["card"], corner_radius=14,
                               cursor="hand2", height=120)
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            card.grid_propagate(False)
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=15, pady=15)
            
            ctk.CTkLabel(inner, text=icon, font=("Segoe UI", 24)).pack(anchor="w")
            ctk.CTkLabel(inner, text=title, font=F["h2"], text_color=C["text"]).pack(anchor="w", pady=(8, 4))
            ctk.CTkLabel(inner, text=desc, font=F["tiny"], text_color=C["text3"]).pack(anchor="w")
            
            card.bind("<Button-1>", lambda e, t=title: self.quick_suggestion(t))
    
    def quick_suggestion(self, title):
        suggestions = {
            "Générer du code": "Génère une fonction Python pour trier une liste",
            "Analyser un fichier": "Analyse le fichier ouvert en ce moment",
            "Corriger une erreur": "J'ai une erreur dans mon code, peux-tu m'aider ?",
        }
        if title in suggestions:
            self.chat_input.delete("1.0", "end")
            self.chat_input.insert("1.0", suggestions[title])
            self.send_message()
    
    def render_user_msg(self, content, file=None):
        frame = ctk.CTkFrame(self.msg_area, fg_color="transparent")
        frame.pack(fill="x", pady=(15, 0), padx=100)
        
        # User avatar
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))
        
        av = ctk.CTkFrame(header, fg_color=C["blue"], width=28, height=28, corner_radius=8)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text="V", font=("Segoe UI", 11, "bold"), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(header, text="Vous", font=F["h2"], text_color=C["text"]).pack(side="left", padx=(10, 0))
        ctk.CTkLabel(header, text=datetime.now().strftime("%H:%M"), font=F["tiny"],
                    text_color=C["text3"]).pack(side="right")
        
        # File attachment
        if file:
            file_box = ctk.CTkFrame(frame, fg_color=C["bg3"], corner_radius=10)
            file_box.pack(fill="x", pady=(0, 8))
            
            ctk.CTkLabel(file_box, text=f"📎  {os.path.basename(file)}",
                        font=F["small"], text_color=C["accent2"]).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(file_box, text=f"{os.path.getsize(file)} bytes",
                        font=F["tiny"], text_color=C["text3"]).pack(side="right", padx=12)
        
        # Message content
        msg = ctk.CTkFrame(frame, fg_color=C["bg3"], corner_radius=14)
        msg.pack(anchor="e", fill="x")
        
        ctk.CTkLabel(msg, text=content, font=F["body"], text_color=C["text"],
                    wraplength=600, justify="left", anchor="w").pack(fill="x", padx=15, pady=12)
    
    def render_ai_msg(self, content):
        frame = ctk.CTkFrame(self.msg_area, fg_color="transparent")
        frame.pack(fill="x", pady=(15, 0), padx=100)
        
        # AI Avatar
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))
        
        av = ctk.CTkFrame(header, fg_color=C["accent"], width=28, height=28, corner_radius=8)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text="G", font=("Segoe UI", 11, "bold"), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(header, text="Grden IA", font=F["h2"], text_color=C["accent2"]).pack(side="left", padx=(10, 0))
        ctk.CTkLabel(header, text=datetime.now().strftime("%H:%M"), font=F["tiny"],
                    text_color=C["text3"]).pack(side="right")
        
        # Parse and render content
        self.render_markdown(frame, content)
        
        # Action buttons
        actions = ctk.CTkFrame(frame, fg_color="transparent")
        actions.pack(fill="x", pady=(10, 0))
        
        for icon, text in [("📋", "Copier"), ("🔄", "Régénérer"), ("👍", "")]:
            ctk.CTkButton(actions, text=f"{icon} {text}", font=F["tiny"],
                         fg_color=C["bg3"], text_color=C["text3"],
                         hover_color=C["border"], height=28, width=80,
                         command=lambda: None).pack(side="left", padx=(0, 5))
    
    def render_markdown(self, parent, text):
        """Rendu markdown simplifié avec blocs de code."""
        # Split by code blocks
        parts = re.split(r'```(\w+)?\n(.*?)```', text, flags=re.DOTALL)
        
        i = 0
        while i < len(parts):
            part = parts[i]
            
            if i + 2 < len(parts) and parts[i + 1] is not None:
                # Code block
                lang = parts[i + 1]
                code = parts[i + 2]
                
                # Code block container
                code_frame = ctk.CTkFrame(parent, fg_color=C["code_bg"],
                                         corner_radius=10, border_width=1,
                                         border_color=C["code_border"])
                code_frame.pack(fill="x", pady=(10, 5))
                
                # Code header
                code_header = ctk.CTkFrame(code_frame, fg_color=C["code_border"],
                                          corner_radius=0)
                code_header.pack(fill="x")
                
                ctk.CTkLabel(code_header, text=f"  {lang or 'code'}",
                            font=F["mono_t"], text_color=C["text2"]).pack(side="left", padx=10, pady=5)
                
                ctk.CTkButton(code_header, text="📋 Copier", font=F["tiny"],
                             fg_color="transparent", text_color=C["text3"],
                             hover_color=C["bg3"], width=70, height=24,
                             command=lambda c=code: self.copy_code(c)).pack(side="right", padx=5, pady=3)
                
                # Code content
                code_text = ctk.CTkTextbox(code_frame, fg_color=C["code_bg"],
                                          text_color=C["green"], font=F["code"],
                                          height=min(len(code.split('\n')) * 18 + 20, 300),
                                          wrap="word")
                code_text.pack(fill="x", padx=5, pady=(0, 5))
                code_text.insert("1.0", code.strip())
                code_text.configure(state="disabled")
                
                # Run button if python
                if lang in ["python", "py", ""]:
                    btn_frame = ctk.CTkFrame(code_frame, fg_color="transparent")
                    btn_frame.pack(fill="x", padx=5, pady=(0, 5))
                    
                    ctk.CTkButton(btn_frame, text="▶ Exécuter", font=F["tiny"],
                                 fg_color=C["green"], text_color="white",
                                 hover_color=C["green2"], height=24, width=90,
                                 command=lambda c=code: self.run_code(c)).pack(side="left")
                
                i += 3
            else:
                # Regular text
                if part.strip():
                    # Handle bold
                    display = part.replace("**", "").replace("• ", "  • ")
                    ctk.CTkLabel(parent, text=display, font=F["body"], text_color=C["text"],
                                wraplength=600, justify="left", anchor="w").pack(fill="x", pady=5)
                i += 1
    
    def copy_code(self, code):
        self.clipboard_clear()
        self.clipboard_append(code)
    
    def run_code(self, code):
        """Exécute du code dans le terminal."""
        # Save to temp file
        temp = os.path.join(self.dir, "_temp_run.py")
        with open(temp, 'w') as f:
            f.write(code)
        
        # Open terminal and run
        self.show_terminal()
        self.term_in.delete(0, "end")
        self.term_in.insert(0, f"python {temp}")
        self.exec_cmd(None)
    
    def send_message(self):
        content = self.chat_input.get("1.0", "end-1c").strip()
        if not content:
            return
        
        conv = self.conversations[self.current_conv]
        
        # Add user message
        conv["messages"].append({"role": "user", "content": content})
        
        # Update title if first message
        if len(conv["messages"]) == 1:
            conv["title"] = content[:30]
            self.update_conv_list()
        
        self.chat_input.delete("1.0", "end")
        
        # Render user message
        self.render_user_msg(content)
        
        # Show typing
        typing = self.show_typing()
        
        # Generate response in thread
        threading.Thread(target=self.generate_response, args=(content, typing), daemon=True).start()
    
    def show_typing(self):
        frame = ctk.CTkFrame(self.msg_area, fg_color="transparent")
        frame.pack(fill="x", pady=(15, 0), padx=100)
        
        av = ctk.CTkFrame(frame, fg_color=C["accent"], width=28, height=28, corner_radius=8)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text="G", font=("Segoe UI", 11, "bold"), text_color="white").pack(expand=True)
        
        dots = ctk.CTkLabel(frame, text="  ● ● ●", font=F["body"], text_color=C["text3"])
        dots.pack(side="left", padx=(10, 0))
        
        self.msg_area._parent_canvas.yview_moveto(1.0)
        return frame
    
    def generate_response(self, user_msg, typing_frame):
        time.sleep(0.5)
        
        response = self.get_response(user_msg)
        
        self.after(100, lambda: typing_frame.destroy())
        self.after(200, lambda: self.add_ai_response(response))
    
    def add_ai_response(self, content):
        conv = self.conversations[self.current_conv]
        conv["messages"].append({"role": "ai", "content": content})
        self.render_ai_msg(content)
        self.msg_area._parent_canvas.yview_moveto(1.0)
    
    def get_response(self, msg):
        ml = msg.lower()
        
        # Check if referring to current file
        if self.current_file and any(w in ml for w in ["ce fichier", "ce code", "ici", "mon code"]):
            return self.analyze_current_file()
        
        # Code generation
        if any(w in ml for w in ["génère", "créer", "écrire", "code", "fonction", "classe"]):
            return self.gen_code_response(ml)
        
        # Analysis
        if any(w in ml for w in ["analyser", "analyse", "review", "vérifier"]):
            return self.analyze_response(ml)
        
        # Debug
        if any(w in ml for w in ["debug", "erreur", "bug", "problème", "error"]):
            return self.debug_response(ml)
        
        # Explanation
        if any(w in ml for w in ["explique", "comment", "pourquoi", "quoi"]):
            return self.explain_response(ml)
        
        # Project
        if any(w in ml for w in ["projet", "fichier", "dossier", "ouvrir"]):
            return self.project_response(ml)
        
        # Greeting
        if any(w in ml for w in ["bonjour", "salut", "hello", "hey"]):
            return "Bonjour ! 👋\n\nJe suis **Grden IA**, votre assistant de développement.\n\nJe peux vous aider avec :\n• 💻 Génération de code\n• 🔍 Analyse de fichiers\n• 🐛 Debug d'erreurs\n• 📚 Explications\n• 📁 Gestion de projet\n\n**Astuce** : Ouvrez un fichier avec le bouton 📁 pour que je puisse travailler directement dessus !"
        
        # Thanks
        if any(w in ml for w in ["merci", "thanks"]):
            return "De rien ! 😊\n\nN'hésitez pas si vous avez d'autres questions. Je suis toujours là pour vous aider !"
        
        # Help
        if any(w in ml for w in ["aide", "help", "peux"]):
            return "## Comment puis-je vous aider ?\n\n### 💻 Génération de code\n> \"Génère une fonction pour trier une liste\"\n> \"Crée une classe Python pour gérer une base de données\"\n\n### 🔍 Analyse\n> \"Analyse ce fichier\"\n> \"Vérifie la qualité de mon code\"\n\n### 🐛 Debug\n> \"J'ai une erreur TypeError\"\n> \"Mon code ne fonctionne pas\"\n\n### 📁 Projet\n> \"Ouvre le fichier main.py\"\n> \"Liste les fichiers du projet\"\n\n### 💡 Astuce\n> Cliquez sur 📁 **Ouvrir fichier** pour attacher un fichier à votre message !"
        
        return f"J'ai bien reçu votre message :\n\n> {msg}\n\nPour mieux vous aider, pouvez-vous me donner plus de détails ?\n\n• **Que voulez-vous faire ?**\n• **Quel est le contexte ?**\n• **Y a-t-il des erreurs ?**\n\nOu utilisez les boutons ci-dessous pour une action rapide !"
    
    def gen_code_response(self, ml):
        if "tri" in ml or "sort" in ml:
            return """## Fonction de tri en Python

Voici plusieurs méthodes de tri :

```python
def tri_rapide(arr):
    '''Tri rapide (Quick Sort) - O(n log n) moyen'''
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    gauche = [x for x in arr if x < pivot]
    milieu = [x for x in arr if x == pivot]
    droite = [x for x in arr if x > pivot]
    return tri_rapide(gauche) + milieu + tri_rapide(droite)

# Utilisation
liste = [64, 34, 25, 12, 22, 11, 90]
resultat = tri_rapide(liste)
print(resultat)  # [11, 12, 22, 25, 34, 64, 90]
```

**Autres options :**
- `sorted(liste)` - Retourne une nouvelle liste triée
- `liste.sort()` - Trie en place

Voulez-vous une autre variante ?"""
        
        if "classe" in ml:
            return """## Classe Python

```python
class MonProjet:
    '''Classe de base pour un projet'''
    
    def __init__(self, nom, description=""):
        self.nom = nom
        self.description = description
        self.fichiers = []
        self.cree_le = datetime.now()
    
    def ajouter_fichier(self, fichier):
        '''Ajoute un fichier au projet'''
        self.fichiers.append(fichier)
        print(f"✓ {fichier} ajouté")
    
    def lister_fichiers(self):
        '''Liste tous les fichiers'''
        return self.fichiers
    
    def __repr__(self):
        return f"Projet({self.nom}, {len(self.fichiers)} fichiers)"

# Utilisation
projet = MonProjet("Mon Application", "Une app cool")
projet.ajouter_fichier("main.py")
```

Voulez-vous une classe spécifique ?"""
        
        return """## Code généré

```python
# Votre code ici
def ma_fonction():
    '''Description de la fonction'''
    # Implémentation
    pass
```

Décrivez-moi ce que vous voulez créer et je générerai le code correspondant !"""
    
    def analyze_response(self, ml):
        if self.current_file:
            return self.analyze_current_file()
        
        return """## 🔍 Analyse de Code

Je peux analyser votre code sous plusieurs angles :

### 📊 Statistiques
- Nombre de lignes, fonctions, classes
- Complexité cyclomatique
- Dette technique

### ⚡ Performance
- Optimisations possibles
- Gestion mémoire
- Points d'amélioration

### 🛡️ Sécurité
- Vulnérabilités
- Bonnes pratiques

**Pour analyser un fichier :**
1. Cliquez sur 📁 **Ouvrir fichier**
2. Sélectionnez votre fichier
3. Demandez-moi de l'analyser !"""
    
    def analyze_current_file(self):
        if not self.current_file:
            return "Aucun fichier n'est ouvert. Utilisez 📁 **Ouvrir fichier** d'abord."
        
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            words = len(content.split())
            funcs = content.count('def ') + content.count('function ')
            classes = content.count('class ')
            imports = content.count('import ')
            complexity = content.count('if ') + content.count('for ') + content.count('while ')
            
            ext = os.path.splitext(self.current_file)[1]
            lang = {'.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.cs': 'C#'}.get(ext, 'Inconnu')
            
            score = min(100, max(0, 100 - (complexity * 2)))
            
            return f"""## 📊 Analyse de {os.path.basename(self.current_file)}

### Informations
| Propriété | Valeur |
|-----------|--------|
| Langage | {lang} |
| Taille | {os.path.getsize(self.current_file)} bytes |
| Lignes | {len(lines)} |
| Mots | {words} |

### Métriques
| Métrique | Nombre |
|----------|--------|
| Fonctions | {funcs} |
| Classes | {classes} |
| Imports | {imports} |
| Complexité | {complexity} |

### Score : {score}/100

{'✅ Bon score !' if score >= 80 else '⚠️ Peut être amélioré' if score >= 60 else '🔴 Nécessite des améliorations'}

### Recommandations
{'• Le code est bien structuré' if funcs > 0 else '• Ajoutez des fonctions pour mieux organiser'}
{'• Les imports sont présents' if imports > 0 else '• Ajoutez des imports si nécessaire'}
{'• Bonne complexité' if complexity < 15 else '• Complexité élevée, à simplifier'}"""
        except Exception as e:
            return f"Erreur lors de la lecture du fichier : {e}"
    
    def debug_response(self, ml):
        return """## 🐛 Assistant Debug

Décrivez-moi votre problème et je vous aiderai !

### Informations utiles :
- **Message d'erreur** complet
- **Le code** qui pose problème
- **Les étapes** pour reproduire
- **Ce que vous avez déjà essayé**

### Exemples de réponses que je peux donner :

```python
# Si vous avez une TypeError :
# Vérifiez les types de vos variables

# Si vous avez une IndexError :
# Vérifiez la taille de votre liste

# Si vous avez une AttributeError :
# Vérifiez que l'attribut existe
```

**Collez votre erreur ici** et je vous guiderai !"""
    
    def explain_response(self, ml):
        if "récursion" in ml:
            return """## 📚 La Récursion

La récursion est une fonction qui **s'appelle elle-même**.

### Principe
```python
def factorielle(n):
    '''Cas de base : arrêt de la récursion'''
    if n <= 1:
        return 1
    '''Cas récursif : appel à la fonction'''
    return n * factorielle(n - 1)

# Exécution :
# factorielle(5)
# = 5 * factorielle(4)
# = 5 * 4 * factorielle(3)
# = 5 * 4 * 3 * factorielle(2)
# = 5 * 4 * 3 * 2 * factorielle(1)
# = 5 * 4 * 3 * 2 * 1
# = 120
```

### Points clés
1. **Cas de base** : Condition d'arrêt
2. **Cas récursif** : L'appel à soi-même
3. **Progression** : Se rapproche du cas de base

### Attention
- Trop de récursion = **stack overflow**
- Préférez les boucles pour les gros volumes

Voulez-vous un autre concept expliqué ?"""
        
        return """## 📚 Explication

Je peux expliquer :

- **Concepts** de programmation
- **Algorithmes** (tri, recherche, etc.)
- **Design Patterns** (singleton, factory, etc.)
- **Syntaxe** de langages
- **Bonnes pratiques**

Posez-moi une question précise !"""
    
    def project_response(self, ml):
        files = [f for f in os.listdir(self.dir) if f.endswith('.py')]
        
        file_list = "\n".join([f"- 📄 {f}" for f in files[:10]])
        
        return f"""## 📁 Projet Actuel

**Dossier :** `{self.dir}`

### Fichiers Python :
{file_list}

### Actions disponibles :
- 📁 **Ouvrir un fichier** - Bouton dans la barre d'outis
- 📊 **Analyser** - Demandez-moi d'analyser un fichier
- ✏️ **Modifier** - Je peux vous aider à modifier le code
- ▶️ **Exécuter** - Lancez des scripts directement

**Que souhaitez-vous faire ?**"""
    
    def attach_file(self):
        path = filedialog.askopenfilename(
            title="Ouvrir un fichier",
            filetypes=[("Python", "*.py"), ("Text", "*.txt"), ("All", "*.*")]
        )
        if path:
            self.current_file = path
            self.chat_input.delete("1.0", "end")
            self.chat_input.insert("1.0", f"J'ai ouvert le fichier {os.path.basename(path)}. Analyse-le pour moi.")
            self.send_message()
    
    def quick_analyze(self):
        if self.current_file:
            self.chat_input.delete("1.0", "end")
            self.chat_input.insert("1.0", "Analyse ce fichier en détail")
            self.send_message()
        else:
            self.attach_file()
    
    def quick_terminal(self):
        self.show_terminal()
    
    def open_project(self):
        path = filedialog.askdirectory(title="Sélectionner un dossier")
        if path:
            self.dir = path
            self.load_project_files()
    
    def load_project_files(self):
        for w in self.proj_frame.winfo_children():
            w.destroy()
        
        try:
            files = [f for f in os.listdir(self.dir) if f.endswith('.py')][:8]
            for f in files:
                item = ctk.CTkFrame(self.proj_frame, fg_color="transparent", height=30)
                item.pack(fill="x", pady=1)
                item.pack_propagate(False)
                
                btn = ctk.CTkButton(item, text=f"🐍 {f}", font=F["mono_t"],
                                   fg_color="transparent", text_color=C["text2"],
                                   hover_color=C["bg3"], anchor="w", height=28,
                                   command=lambda f=f: self.open_file(os.path.join(self.dir, f)))
                btn.pack(fill="x", padx=5)
        except:
            pass
    
    def open_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.current_file = path
            self.load_project_files()
            
            # Add to chat
            self.chat_input.delete("1.0", "end")
            self.chat_input.insert("1.0", f"J'ai ouvert {os.path.basename(path)}. Voici le contenu :\n\n```python\n{content[:1000]}\n```\n\nPeux-tu l'analyser ?")
            self.send_message()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    # ═══════════════════════════════════════════════════════════════
    # OTHER PAGES
    # ═══════════════════════════════════════════════════════════════
    
    def show_home(self):
        self.clear_page()
        
        s = ctk.CTkScrollableFrame(self.page, fg_color="transparent")
        s.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(s, text="🏠  Accueil", font=F["title"], text_color=C["text"]).pack(anchor="w", pady=(0, 25))
        
        # Stats
        stats = ctk.CTkFrame(s, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 20))
        stats.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        py_count = len([f for f in os.listdir(self.dir) if f.endswith('.py')])
        models_dir = os.path.join(self.dir, 'models')
        model_count = len([d for d in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, d))]) if os.path.exists(models_dir) else 0
        
        for i, (val, lbl, color) in enumerate([
            (py_count, "Fichiers", C["blue"]),
            (model_count, "Modèles", C["purple"]),
            (len(self.conversations), "Conversations", C["accent2"]),
            (len(self.chat_history), "Messages", C["green"]),
        ]):
            card = ctk.CTkFrame(stats, fg_color=C["card"], corner_radius=14)
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            
            ctk.CTkLabel(card, text=str(val), font=("Segoe UI", 28, "bold"),
                        text_color=color).pack(padx=20, pady=(15, 5), anchor="w")
            ctk.CTkLabel(card, text=lbl, font=F["small"],
                        text_color=C["text2"]).pack(padx=20, pady=(0, 15), anchor="w")
        
        # Quick actions
        ctk.CTkLabel(s, text="⚡  Actions Rapides", font=F["h1"], text_color=C["text"]).pack(anchor="w", pady=(0, 15))
        
        grid = ctk.CTkFrame(s, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        for i, (icon, title, cmd, color) in enumerate([
            ("💬", "Chat IA", self.show_chat, C["accent"]),
            ("📊", "Dashboard", self.show_dashboard, C["blue"]),
            ("📝", "Éditeur", self.show_editor, C["green"]),
        ]):
            card = ctk.CTkFrame(grid, fg_color=C["card"], corner_radius=14, height=100, cursor="hand2")
            card.grid(row=0, column=i, padx=8, sticky="nsew")
            card.grid_propagate(False)
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=20, pady=15)
            
            ctk.CTkLabel(inner, text=icon, font=("Segoe UI", 28), text_color=color).pack(anchor="w")
            ctk.CTkLabel(inner, text=title, font=F["h2"], text_color=C["text"]).pack(anchor="w", pady=(8, 0))
            
            card.bind("<Button-1>", lambda e, c=cmd: c())
    
    def show_dashboard(self):
        self.clear_page()
        
        s = ctk.CTkScrollableFrame(self.page, fg_color="transparent")
        s.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(s, text="📊  Dashboard", font=F["title"], text_color=C["text"]).pack(anchor="w", pady=(0, 25))
        
        # Recent files
        ctk.CTkLabel(s, text="📄  Fichiers Récents", font=F["h1"], text_color=C["text"]).pack(anchor="w", pady=(0, 15))
        
        files_card = ctk.CTkFrame(s, fg_color=C["card"], corner_radius=14)
        files_card.pack(fill="x")
        
        py_files = [f for f in os.listdir(self.dir) if f.endswith('.py')][:8]
        for f in py_files:
            item = ctk.CTkFrame(files_card, fg_color="transparent", height=42)
            item.pack(fill="x", padx=2, pady=1)
            
            ctk.CTkLabel(item, text=f"  🐍  {f}", font=F["mono_s"], text_color=C["text2"]).pack(side="left", padx=12)
            
            ctk.CTkButton(item, text="→", font=F["small"], fg_color=C["bg3"], text_color=C["text2"],
                         hover_color=C["border"], width=35, height=26,
                         command=lambda f=f: self.open_file(os.path.join(self.dir, f))).pack(side="right", padx=12)
    
    def show_editor(self):
        self.clear_page()
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        # Toolbar
        tb = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=12)
        tb.pack(fill="x", pady=(0, 12))
        
        ctk.CTkButton(tb, text="📂  Ouvrir", font=F["small"], fg_color=C["bg3"],
                     text_color=C["text2"], hover_color=C["border"],
                     command=lambda: self.open_file(filedialog.askopenfilename(filetypes=[("Python", "*.py")]))).pack(side="left", padx=10, pady=10)
        
        self.file_lbl = ctk.CTkLabel(tb, text="Aucun fichier", font=F["small"], text_color=C["text2"])
        self.file_lbl.pack(side="right", padx=12)
        
        # Editor
        ed = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        ed.pack(fill="both", expand=True)
        
        self.editor = ctk.CTkTextbox(ed, fg_color=C["bg3"], text_color=C["text"],
                                    font=F["mono"], corner_radius=12)
        self.editor.pack(fill="both", expand=True, padx=10, pady=10)
        
        if self.current_file:
            try:
                with open(self.current_file, 'r') as file:
                    self.editor.insert("1.0", file.read())
                self.file_lbl.configure(text=os.path.basename(self.current_file))
            except:
                pass
    
    def show_terminal(self):
        self.clear_page()
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="⚡  Terminal", font=F["title"], text_color=C["text"]).pack(anchor="w", pady=(0, 20))
        
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
    
    def show_settings(self):
        self.clear_page()
        
        f = ctk.CTkFrame(self.page, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=35, pady=25)
        
        ctk.CTkLabel(f, text="⚙  Paramètres", font=F["title"], text_color=C["text"]).pack(anchor="w", pady=(0, 25))
        
        card = ctk.CTkFrame(f, fg_color=C["card"], corner_radius=16)
        card.pack(fill="x")
        
        ctk.CTkLabel(card, text="  ℹ️  À propos", font=F["h1"], text_color=C["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        ctk.CTkLabel(card, text=f"Application : {APP_NAME}", font=F["body"], text_color=C["text2"]).pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=f"Version    : {APP_VERSION}", font=F["body"], text_color=C["text2"]).pack(anchor="w", padx=15, pady=3)
        ctk.CTkLabel(card, text=f"Dossier    : {self.dir}", font=F["mono_s"], text_color=C["text2"]).pack(anchor="w", padx=15, pady=3)


def main():
    app = GrdenIA()
    app.mainloop()


if __name__ == "__main__":
    main()
