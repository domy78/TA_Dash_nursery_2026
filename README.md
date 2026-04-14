# Tableau de Bord - Pépinières

Application Flask pour la gestion et la visualisation des données de pépinières.

## Description

Ce projet est un tableau de bord interactif pour surveiller :
- Semis et germination
- Distribution de plants
- Problèmes et causes de mortalité
- Tendances par pays, région et organisation

## Technologies

- **Backend** : Flask
- **Frontend** : HTML/CSS/JavaScript
- **Visualisation** : Chart.js, Plotly.js
- **Données** : Pandas, Excel

## Installation

1. Cloner le dépôt
```bash
git clone https://github.com/domy78/TA_Dash_nursery_2026.git
cd TA_Dash_nursery_2026
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install flask pandas numpy openpyxl
```

## Utilisation

Lancer l'application :
```bash
python App_nursery.py
```

Accéder au tableau de bord : http://127.0.0.1:8051

## Structure du projet

- `App_nursery.py` - Application principale Flask
- `pepiniereq_26_Dash.ipynb` - Notebook d'analyse
- `Tableau_de_bord_pepinieres (version 1).xlsx` - Données

## Auteur

Domynic Pépin

## License

MIT
