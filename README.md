# YouTube Title Generator 
![ain](https://github.com/user-attachments/assets/b17a713e-17c8-4217-bc1a-bda59410a204)

##  Description
Un générateur intelligent de titres YouTube utilisant le Machine Learning pour aider les créateurs de contenu à produire des titres accrocheurs.

##  Objectif du Projet
Développer un modèle NLP capable de générer des titres de vidéos pertinents et attractifs en exploitant des données de tendances YouTube.

##  Fonctionnalités
- Interface utilisateur moderne avec Tkinter
- Génération de titres basée sur un modèle LSTM
- Copie facile des titres générés
- Compteur de caractères en temps réel

## **Données**
Les données utilisées pour ce projet sont tirées des ensembles de données des vidéos tendances sur YouTube pour les régions suivantes :
- **États-Unis** (`USvideos.csv`)
- **Canada** (`CAvideos.csv`)
- **Royaume-Uni** (`GBvideos.csv`)

Les fichiers JSON associés (`US_category_id.json`, etc.) contiennent les noms des catégories des vidéos.

## **Étapes de Prétraitement des Données**
1. Nettoyage des titres (suppression des ponctuations, conversion en minuscules).
2. Mapping des catégories de vidéos à leurs noms.
3. Extraction des titres pour une catégorie spécifique (ex. : "Entertainment").
4. Tokenisation et génération de séquences n-grams.

## **Environnement et Bibliothèques**

### **Bibliothèques Utilisées :**
- `Pandas` : Chargement et manipulation des données.
- `NumPy` : Calculs numériques.
- `TensorFlow/Keras` : Modélisation du réseau LSTM.
- `JSON` : Lecture des fichiers de catégories
- `Tkinter` : Interface Graphique

### Prérequis
- Python 3.7+
- Jupyter Notebook
- pip

### Étapes d'Installation
1. Clonez le dépôt
```bash
git clone https://github.com/votre-utilisateur/YouTube_Title_Generator.git
cd YouTube_Title_Generator
```

2. Installez les dépendances
```bash
pip install -r requirements.txt
```

3. Lancez l'application
```bash
python gui_app.py
```


## 📂 Structure du Projet
![archi](https://github.com/user-attachments/assets/6988dcb0-03b6-4eb6-ac8e-bc504c932baf)


##  Modèle Machine Learning
Architecture LSTM comprenant :
- **Couche d'Embedding** : Transforme les mots en vecteurs numériques.
- **Couche LSTM** : Garde en mémoire le contexte des séquences.
- **Couche Dropout** : Réduit l'overfitting.
- **Couche Dense** : Prédit le mot suivant avec une activation softmax.

## **Démonstration de projet**
  
https://github.com/user-attachments/assets/8b1f0d76-2b51-49d1-a882-018de00e9cc0



## **Conclusion**
les étapes présentées dans les captures permettent de charger, nettoyer, et préparer les données des vidéos YouTube tendances pour un traitement efficace. En extrayant les catégories, en nettoyant les titres, et en combinant les ensembles de données, cette préparation offre une base solide pour des analyses ou traitements NLP (Natural Language Processing) plus approfondis.


## 👥 Équipe
- Zakaria ZINAOUI
- Salma DAIGHAM
- Imane TAHRI
- Nabil HAMDI
