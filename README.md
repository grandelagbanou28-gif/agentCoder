# Graden IA - Intelligence Artificielle pour Développeurs

Un système complet pour entraîner un modèle LLM libre (Llama, Mistral, etc.) spécialisé dans la génération de code, utilisant un système multi-agents qui scrape automatiquement internet.

## 🎯 Fonctionnalités

### 🕷️ Web Scraping Gratuit
- **Scrape automatique** depuis DuckDuckGo, GitHub et Stack Overflow
- **Sans API payante** - utilise BeautifulSoup et requests
- **Au plus rapide** - pas de délais inutiles
- **Option code-only** - scrape uniquement du code pour un modèle full codage

### 🤖 Système Multi-Agents
- **Coder A** : Génère une première solution
- **Coder B** : Génère une solution alternative
- **Arbitre** : Compare et choisit la meilleure approche
- **Feedback** : Les agents apprennent de chaque itération

### 📊 Entraînement du Modèle
- **Fine-tuning** automatique avec les données scrapées
- **Métriques** de performance en temps réel
- **Persistance** des décisions et apprentissages
- **Export au format Ollama** (GGUF) pour utilisation directe

### 🔗 Intégration UnityIAPro
- **Synchronisation en temps réel** avec le dashboard
- **Visualisation** des conversations et décisions
- **Alertes** automatiques en cas d'erreur
- **Logs** complètes de toutes les interactions

### 🚀 API HTTP Locale
- **Génération de code** indépendante
- **Analyse de code** (qualité, sécurité, performance)
- **Comparaison** de solutions
- **Entraînement** du modèle
- **Export au format Ollama** (GGUF) pour utilisation directe

### 💻 Assistant CLI Interactif
- **Lire/éditer/écrire** des fichiers
- **Rechercher** dans les fichiers
- **Analyser** le code (langage, complexité, score)
- **Exécuter** du Python
- **Créer** des projets (templates)
- **Git** (status, diff, log, commit)
- **Gestion des modèles**
- **Entraînement** du modèle

## 📦 Installation

### Prérequis
- Python 3.8+
- pip ou conda

### Setup
```bash
# Cloner le repository
git clone https://github.com/grandelagbanou28-gif/agentCoder.git
cd agentCoder

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation

### Lancer l'assistant CLI
```bash
python graden.py
```

### Lancer l'entraînement
```bash
# Entraînement basique
python orchestrator.py --topic "Unity game development" --pages 3 --iterations 3

# Entraînement code-only
python orchestrator.py --topic "Python best practices" --code-only --pages 5

# Avec choix interactif du modèle
python orchestrator.py --choose-model
```

### Lancer l'API HTTP
```bash
python model_api.py
# ou
python -m uvicorn model_api:app --host 127.0.0.1 --port 8000
```

## 📁 Structure du Projet

```
agentCoder/
├── graden.py              # Point d'entrée principal CLI
├── orchestrator.py        # Orchestrateur d'entraînement
├── scraper.py             # Web scraper gratuit
├── multi_agent_system.py  # Système multi-agents
├── model_manager.py       # Gestionnaire de modèles
├── model_analyzer.py      # Analyseur de modèles
├── training_visualizer.py # Visualiseur d'entraînement
├── model_api.py           # API HTTP FastAPI
├── trpc_client.py         # Client tRPC UnityIAPro
├── setup_models.py        # Script de setup
├── requirements.txt       # Dépendances Python
├── GradenIA.bat           # Lanceur Windows
├── launch.vbs             # Lanceur VBScript
├── IAtrainer.ico          # Icône de l'application
└── models/                # Modèles stockés
    ├── .GradenModels/     # Données de cache
    └── ollama/            # Modèles Ollama
```

## 🛠️ Configuration

### Variables d'environnement
Créez un fichier `.env` :
```env
# Dashboard UnityIAPro
DASHBOARD_URL=http://localhost:3000/api/trpc

# Configuration du modèle
MODEL_NAME=llama2-unity
MAX_TOKENS=512
TEMPERATURE=0.7
```

### Configuration API
L'API peut être configurée via le menu interactif ou les arguments en ligne de commande.

## 📚 Documentation

- [QUICK_START.md](QUICK_START.md) - Tutoriel pas à pas
- [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) - Guide complet avec fonctionnalités avancées
- [MODELS_SETUP.md](MODELS_SETUP.md) - Configuration des modèles

## 🤝 Contribuer

Les contributions sont bienvenues ! Veuillez créer un ticket ou une pull request.

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- **Ollama** pour l'exécution locale des modèles
- **UnityIAPro** pour l'intégration du dashboard
- **BeautifulSoup** pour le web scraping
- **FastAPI** pour l'API HTTP
