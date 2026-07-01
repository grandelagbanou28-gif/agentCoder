"""
Graden IA - Assistant CLI pour le développement logiciel.
Inspiré d'opencode : outils interactifs pour analyser, écrire et gérer du code.
"""

import os
import sys
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Couleurs ANSI
class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

def print_banner():
    """Affiche la bannière de Graden IA."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   ██████╗ ██████╗ ██████╗ ███████╗███████╗████████╗██╗   ██╗██████╗ 
  ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝╚══██╔╝██║   ██║██╔══██╗
  ██║     ██║   ██║██████╔╝█████╗  ███████╗   ██║  ██║   ██║██████╔╝
  ██║     ██║   ██║██╔══██╗██╔══╝  ╚════██║   ██║  ██║   ██║██╔═══╝ 
  ╚██████╗╚██████╔╝██║  ██║███████╗███████║   ██║  ╚██████╔╝██║     
   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═════╝ ╚═╝     
{Colors.RESET}
{Colors.DIM}  Assistant CLI pour le développement logiciel - Version 2.0{Colors.RESET}
"""
    print(banner)


def clear_screen():
    """Efface l'écran."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Affiche un en-tête formaté."""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{title.center(60)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")


def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")


def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")


def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")


# ═══════════════════════════════════════════════════════════════
# OUTILS DE FICHIERS
# ═══════════════════════════════════════════════════════════════

def read_file():
    """Lit un fichier."""
    path = input(f"\n{Colors.CYAN}Chemin du fichier: {Colors.RESET}").strip()
    if not path:
        print_error("Chemin vide")
        return
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        print(f"\n{Colors.GREEN}--- {path} ({len(lines)} lignes) ---{Colors.RESET}\n")
        
        for i, line in enumerate(lines[:200], 1):
            print(f"{Colors.DIM}{i:4d}{Colors.RESET} {line}")
        
        if len(lines) > 200:
            print(f"\n{Colors.YELLOW}... {len(lines) - 200} lignes supplémentaires{Colors.RESET}")
        
        # Stats
        words = len(content.split())
        chars = len(content)
        funcs = content.count('def ') + content.count('function ')
        classes = content.count('class ')
        
        print(f"\n{Colors.CYAN}Stats: {words} mots | {chars} caractères | {funcs} fonctions | {classes} classes{Colors.RESET}")
        
    except FileNotFoundError:
        print_error(f"Fichier non trouvé: {path}")
    except Exception as e:
        print_error(f"Erreur: {e}")


def write_file():
    """Écrit dans un fichier."""
    path = input(f"\n{Colors.CYAN}Chemin du fichier: {Colors.RESET}").strip()
    if not path:
        print_error("Chemin vide")
        return
    
    print(f"{Colors.DIM}Entrez le contenu (tapez 'FIN' sur une ligne pour terminer):{Colors.RESET}")
    lines = []
    while True:
        line = input()
        if line.strip() == 'FIN':
            break
        lines.append(line)
    
    content = '\n'.join(lines)
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"Fichier écrit: {path} ({len(content)} caractères)")
    except Exception as e:
        print_error(f"Erreur: {e}")


def edit_file():
    """Édite un fichier avec recherche/remplacement."""
    path = input(f"\n{Colors.CYAN}Chemin du fichier: {Colors.RESET}").strip()
    if not path or not os.path.exists(path):
        print_error("Fichier non trouvé")
        return
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"{Colors.DIM}Contenu actuel ({len(content.split(chr(10)))} lignes){Colors.RESET}")
        
        search = input(f"{Colors.CYAN}Texte à rechercher: {Colors.RESET}")
        if not search:
            return
        
        count = content.count(search)
        if count == 0:
            print_warning("Texte non trouvé")
            return
        
        print_info(f"Trouvé {count} occurrence(s)")
        replace = input(f"{Colors.CYAN}Remplacement: {Colors.RESET}")
        
        confirm = input(f"{Colors.YELLOW}Remplacer tous? (o/n): {Colors.RESET}")
        if confirm.lower() == 'o':
            new_content = content.replace(search, replace)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print_success(f"Remplacement effectué ({count} occurrences)")
        else:
            print_info("Annulé")
            
    except Exception as e:
        print_error(f"Erreur: {e}")


def list_directory():
    """Liste le contenu d'un répertoire."""
    path = input(f"\n{Colors.CYAN}Chemin (vide = répertoire courant): {Colors.RESET}").strip()
    if not path:
        path = "."
    
    try:
        items = os.listdir(path)
        dirs = []
        files = []
        
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                dirs.append(item)
            else:
                size = os.path.getsize(full_path)
                files.append((item, size))
        
        print(f"\n{Colors.CYAN}📁 {path}/{Colors.RESET}\n")
        
        for d in sorted(dirs):
            print(f"  {Colors.BLUE}📁 {d}/{Colors.RESET}")
        
        for f, size in sorted(files):
            if size > 1024*1024:
                size_str = f"{size/1024/1024:.1f} MB"
            elif size > 1024:
                size_str = f"{size/1024:.1f} KB"
            else:
                size_str = f"{size} B"
            print(f"  📄 {f} ({Colors.DIM}{size_str}{Colors.RESET})")
        
        print(f"\n{Colors.DIM}{len(dirs)} dossier(s), {len(files)} fichier(s){Colors.RESET}")
        
    except Exception as e:
        print_error(f"Erreur: {e}")


def search_in_files():
    """Recherche un texte dans les fichiers."""
    pattern = input(f"\n{Colors.CYAN}Texte à rechercher: {Colors.RESET}").strip()
    if not pattern:
        return
    
    ext = input(f"{Colors.CYAN}Extension (vide = tous, ex: .py): {Colors.RESET}").strip()
    
    print(f"\n{Colors.DIM}Recherche en cours...{Colors.RESET}\n")
    
    found = 0
    for root, dirs, files in os.walk('.'):
        # Ignorer .git et __pycache__
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
        
        for file in files:
            if ext and not file.endswith(ext):
                continue
            
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if pattern.lower() in line.lower():
                            print(f"  {Colors.GREEN}{filepath}:{i}{Colors.RESET} {line.rstrip()[:80]}")
                            found += 1
                            if found > 50:
                                print_warning("Arrêt après 50 résultats")
                                return
            except:
                pass
    
    print(f"\n{Colors.CYAN}Trouvé dans {found} ligne(s){Colors.RESET}")


# ═══════════════════════════════════════════════════════════════
# OUTILS GIT
# ═══════════════════════════════════════════════════════════════

def git_status():
    """Affiche le statut Git."""
    print(f"\n{Colors.CYAN}--- Git Status ---{Colors.RESET}\n")
    result = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print_error(result.stderr)


def git_diff():
    """Affiche les différences Git."""
    print(f"\n{Colors.CYAN}--- Git Diff ---{Colors.RESET}\n")
    result = subprocess.run(['git', 'diff'], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print_error(result.stderr)


def git_log():
    """Affiche l'historique Git."""
    print(f"\n{Colors.CYAN}--- Git Log (10 derniers) ---{Colors.RESET}\n")
    result = subprocess.run(['git', 'log', '--oneline', '-10'], capture_output=True, text=True)
    print(result.stdout)


def git_commit():
    """Crée un commit Git."""
    msg = input(f"\n{Colors.CYAN}Message de commit: {Colors.RESET}").strip()
    if not msg:
        print_error("Message vide")
        return
    
    print_info("git add .")
    subprocess.run(['git', 'add', '.'], capture_output=True)
    
    print_info(f"git commit -m \"{msg}\"")
    result = subprocess.run(['git', 'commit', '-m', msg], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print_error(result.stderr)


# ═══════════════════════════════════════════════════════════════
# OUTILS DE CODE
# ═══════════════════════════════════════════════════════════════

def analyze_code():
    """Analyse un fichier de code."""
    path = input(f"\n{Colors.CYAN}Chemin du fichier: {Colors.RESET}").strip()
    if not path or not os.path.exists(path):
        print_error("Fichier non trouvé")
        return
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        words = content.split()
        
        # Détection de langue
        ext = os.path.splitext(path)[1].lower()
        lang_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
            '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP',
            '.html': 'HTML', '.css': 'CSS', '.json': 'JSON', '.md': 'Markdown'
        }
        lang = lang_map.get(ext, 'Inconnu')
        
        # Analyse
        functions = content.count('def ') + content.count('function ')
        classes = content.count('class ')
        imports = content.count('import ') + content.count('from ')
        comments = content.count('#') + content.count('//')
        
        # Complexité cyclomatique simple
        complexity = content.count('if ') + content.count('elif ') + content.count('else:')
        complexity += content.count('for ') + content.count('while ')
        complexity += content.count('try:') + content.count('except')
        
        print(f"\n{Colors.GREEN}--- Analyse de {path} ---{Colors.RESET}\n")
        print(f"  {Colors.CYAN}Langage:{Colors.RESET}      {lang}")
        print(f"  {Colors.CYAN}Lignes:{Colors.RESET}       {len(lines)}")
        print(f"  {Colors.CYAN}Mots:{Colors.RESET}         {len(words)}")
        print(f"  {Colors.CYAN}Caractères:{Colors.RESET}   {len(content)}")
        print(f"  {Colors.CYAN}Fonctions:{Colors.RESET}    {functions}")
        print(f"  {Colors.CYAN}Classes:{Colors.RESET}      {classes}")
        print(f"  {Colors.CYAN}Imports:{Colors.RESET}      {imports}")
        print(f"  {Colors.CYAN}Commentaires:{Colors.RESET} {comments}")
        print(f"  {Colors.CYAN}Complexité:{Colors.RESET}   {complexity}")
        
        # Score de qualité
        score = 100
        if functions == 0 and len(lines) > 50:
            score -= 10
        if imports == 0 and len(lines) > 20:
            score -= 5
        if comments == 0 and len(lines) > 30:
            score -= 10
        if complexity > 20:
            score -= 15
        
        color = Colors.GREEN if score >= 80 else Colors.YELLOW if score >= 60 else Colors.RED
        print(f"\n  {color}Score de qualité: {score}/100{Colors.RESET}")
        
    except Exception as e:
        print_error(f"Erreur: {e}")


def run_code():
    """Exécute un fichier Python."""
    path = input(f"\n{Colors.CYAN}Chemin du fichier Python: {Colors.RESET}").strip()
    if not path or not os.path.exists(path):
        print_error("Fichier non trouvé")
        return
    
    args = input(f"{Colors.CYAN}Arguments (optionnel): {Colors.RESET}").strip()
    
    cmd = f'python "{path}"'
    if args:
        cmd += f" {args}"
    
    print(f"\n{Colors.DIM}Exécution: {cmd}{Colors.RESET}\n")
    os.system(cmd)


def create_project():
    """Crée un template de projet."""
    name = input(f"\n{Colors.CYAN}Nom du projet: {Colors.RESET}").strip()
    if not name:
        return
    
    template = input(f"{Colors.CYAN}Template (python/node/simple): {Colors.RESET}").strip()
    
    os.makedirs(name, exist_ok=True)
    
    if template == 'python':
        with open(os.path.join(name, 'main.py'), 'w') as f:
            f.write('#!/usr/bin/env python3\n"""Main module."""\n\n\ndef main():\n    print("Hello from ' + name + '!")\n\n\nif __name__ == "__main__":\n    main()\n')
        with open(os.path.join(name, 'requirements.txt'), 'w') as f:
            f.write('# Dependencies\n')
        with open(os.path.join(name, 'README.md'), 'w') as f:
            f.write(f'# {name}\n\nDescription du projet.\n')
    
    elif template == 'node':
        with open(os.path.join(name, 'package.json'), 'w') as f:
            json.dump({"name": name, "version": "1.0.0", "main": "index.js"}, f, indent=2)
        with open(os.path.join(name, 'index.js'), 'w') as f:
            f.write('console.log("Hello from ' + name + '!");\n')
    
    else:
        with open(os.path.join(name, 'README.md'), 'w') as f:
            f.write(f'# {name}\n\nDescription du projet.\n')
    
    print_success(f"Projet créé: {name}/")


# ═══════════════════════════════════════════════════════════════
# OUTILS SYSTÈME
# ═══════════════════════════════════════════════════════════════

def system_info():
    """Affiche les informations système."""
    import platform
    
    print(f"\n{Colors.GREEN}--- Informations Système ---{Colors.RESET}\n")
    print(f"  {Colors.CYAN}OS:{Colors.RESET}         {platform.system()} {platform.release()}")
    print(f"  {Colors.CYAN}Python:{Colors.RESET}     {platform.python_version()}")
    print(f"  {Colors.CYAN}Machine:{Colors.RESET}    {platform.machine()}")
    print(f"  {Colors.CYAN}Processeur:{Colors.RESET} {platform.processor()}")
    
    # Espace disque
    disk = os.statvfs('.') if os.name != 'nt' else None
    if disk:
        free = disk.f_bavail * disk.f_frsize / (1024**3)
        print(f"  {Colors.CYAN}Disque libre:{Colors.RESET} {free:.1f} GB")
    
    # Python packages
    print(f"\n  {Colors.CYAN}Packages installés:{Colors.RESET}")
    result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=columns'], 
                          capture_output=True, text=True)
    for line in result.stdout.split('\n')[:20]:
        if line.strip():
            print(f"    {line}")


def run_shell():
    """Exécute une commande shell."""
    cmd = input(f"\n{Colors.CYAN}Commande: {Colors.RESET}").strip()
    if not cmd:
        return
    
    print(f"\n{Colors.DIM}$ {cmd}{Colors.RESET}\n")
    os.system(cmd)


# ═══════════════════════════════════════════════════════════════
# OUTILS MODÈLES
# ═══════════════════════════════════════════════════════════════

def list_models():
    """Liste les modèles disponibles."""
    print(f"\n{Colors.GREEN}--- Modèles Disponibles ---{Colors.RESET}\n")
    
    models_dir = "models"
    if os.path.exists(models_dir):
        for root, dirs, files in os.walk(models_dir):
            level = root.replace(models_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{Colors.BLUE}{indent}{os.path.basename(root)}/{Colors.RESET}")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:
                size = os.path.getsize(os.path.join(root, file))
                if size > 1024*1024:
                    size_str = f"{size/1024/1024:.1f} MB"
                else:
                    size_str = f"{size/1024:.1f} KB"
                print(f"{subindent}📄 {file} ({Colors.DIM}{size_str}{Colors.RESET})")
    else:
        print_warning("Dossier models/ non trouvé")


def train_model():
    """Lance l'entraînement du modèle."""
    print(f"\n{Colors.GREEN}--- Entraînement du Modèle ---{Colors.RESET}\n")
    
    topic = input(f"{Colors.CYAN}Sujet d'entraînement: {Colors.RESET}").strip()
    if not topic:
        topic = "Unity game development best practices"
    
    pages = input(f"{Colors.CYAN}Nombre de pages (défaut: 3): {Colors.RESET}").strip()
    pages = int(pages) if pages.isdigit() else 3
    
    iterations = input(f"{Colors.CYAN}Nombre d'itérations (défaut: 3): {Colors.RESET}").strip()
    iterations = int(iterations) if iterations.isdigit() else 3
    
    print_info(f"Lancement: python orchestrator.py --topic \"{topic}\" --pages {pages} --iterations {iterations} --no-dashboard")
    os.system(f'python orchestrator.py --topic "{topic}" --pages {pages} --iterations {iterations} --no-dashboard')


# ═══════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def show_menu():
    """Affiche le menu principal."""
    print(f"""
{Colors.BOLD}{Colors.WHITE}  Outils:{Colors.RESET}
    {Colors.GREEN}1{Colors.RESET}  📖 Lire un fichier          {Colors.DIM}  read{Colors.RESET}
    {Colors.GREEN}2{Colors.RESET}  ✏️  Écrire un fichier         {Colors.DIM}  write{Colors.RESET}
    {Colors.GREEN}3{Colors.RESET}  🔍 Éditer un fichier         {Colors.DIM}  edit{Colors.RESET}
    {Colors.GREEN}4{Colors.RESET}  📁 Lister un dossier         {Colors.DIM}  ls{Colors.RESET}
    {Colors.GREEN}5{Colors.RESET}  🔎 Rechercher dans les fichiers {Colors.DIM}  grep{Colors.RESET}
    
{Colors.BOLD}{Colors.WHITE}  Code:{Colors.RESET}
    {Colors.GREEN}6{Colors.RESET}  📊 Analyser un fichier       {Colors.DIM}  analyze{Colors.RESET}
    {Colors.GREEN}7{Colors.RESET}  ▶️  Exécuter du Python        {Colors.DIM}  run{Colors.RESET}
    {Colors.GREEN}8{Colors.RESET}  🆕 Créer un projet           {Colors.DIM}  create{Colors.RESET}
    
{Colors.BOLD}{Colors.WHITE}  Git:{Colors.RESET}
    {Colors.GREEN}9{Colors.RESET}  📋 Statut Git                {Colors.DIM}  git status{Colors.RESET}
    {Colors.GREEN}10{Colors.RESET} 📝 Diff Git                  {Colors.DIM}  git diff{Colors.RESET}
    {Colors.GREEN}11{Colors.RESET} 📜 Log Git                   {Colors.DIM}  git log{Colors.RESET}
    {Colors.GREEN}12{Colors.RESET} 💾 Commit Git                {Colors.DIM}  commit{Colors.RESET}
    
{Colors.BOLD}{Colors.WHITE}  Modèles:{Colors.RESET}
    {Colors.GREEN}13{Colors.RESET} 🤖 Lister les modèles        {Colors.DIM}  models{Colors.RESET}
    {Colors.GREEN}14{Colors.RESET} 🎯 Entraîner un modèle       {Colors.DIM}  train{Colors.RESET}
    
{Colors.BOLD}{Colors.WHITE}  Système:{Colors.RESET}
    {Colors.GREEN}15{Colors.RESET} 💻 Info système              {Colors.DIM}  sysinfo{Colors.RESET}
    {Colors.GREEN}16{Colors.RESET} ⚡ Shell                     {Colors.DIM}  shell{Colors.RESET}
    {Colors.GREEN}0{Colors.RESET}  🚪 Quitter                   {Colors.DIM}  exit{Colors.RESET}
""")


def main():
    """Point d'entrée principal."""
    clear_screen()
    print_banner()
    
    while True:
        try:
            show_menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}graden ❯ {Colors.RESET}").strip()
            
            if choice in ['1', 'read']:
                read_file()
            elif choice in ['2', 'write']:
                write_file()
            elif choice in ['3', 'edit']:
                edit_file()
            elif choice in ['4', 'ls']:
                list_directory()
            elif choice in ['5', 'grep']:
                search_in_files()
            elif choice in ['6', 'analyze']:
                analyze_code()
            elif choice in ['7', 'run']:
                run_code()
            elif choice in ['8', 'create']:
                create_project()
            elif choice in ['9', 'git status']:
                git_status()
            elif choice in ['10', 'git diff']:
                git_diff()
            elif choice in ['11', 'git log']:
                git_log()
            elif choice in ['12', 'commit']:
                git_commit()
            elif choice in ['13', 'models']:
                list_models()
            elif choice in ['14', 'train']:
                train_model()
            elif choice in ['15', 'sysinfo']:
                system_info()
            elif choice in ['16', 'shell']:
                run_shell()
            elif choice in ['0', 'exit', 'quit', 'q']:
                print(f"\n{Colors.GREEN}Au revoir ! 👋{Colors.RESET}\n")
                break
            else:
                print_warning("Option invalide")
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Ctrl+C détecté. Au revoir !{Colors.RESET}\n")
            break
        except Exception as e:
            print_error(f"Erreur inattendue: {e}")


if __name__ == "__main__":
    main()
