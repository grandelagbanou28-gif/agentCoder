# agentCoder

Un système complet pour entraîner un modèle LLM libre spécialisé dans la génération de code.

## Démarrage rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'assistant CLI
python graden.py

# Ou lancer l'entraînement directement
python orchestrator.py --topic "Python best practices" --pages 3 --iterations 3
```

## Fonctionnalités principales

- 🤖 Système multi-agents (Coder A, Coder B, Arbitre)
- 🕷️ Web scraping gratuit (DuckDuckGo, GitHub, Stack Overflow)
- 📊 Métriques d'entraînement en temps réel
- 🚀 API HTTP pour l'inférence
- 💻 Assistant CLI interactif

## Documentation

- [Guide complet](COMPLETE_GUIDE.md)
- [Démarrage rapide](QUICK_START.md)
- [Configuration des modèles](MODELS_SETUP.md)
- [Contribuer](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Licence

MIT License
