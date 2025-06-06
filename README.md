# 💊 Assistant Antibiothérapie – Infections Urinaires

Une application web interactive développée avec Streamlit pour aider les professionnels de santé à prendre des décisions thérapeutiques concernant les infections urinaires.

## 🚀 Fonctionnalités

- **Arbre décisionnel interactif** : Guide l'utilisateur à travers une série de questions cliniques
- **Recommandations personnalisées** : Fournit des recommandations d'antibiothérapie basées sur les réponses
- **Visualisation graphique** : Affichage de l'arbre décisionnel avec le chemin parcouru mis en évidence
- **Références cliniques** : Chaque recommandation inclut ses références bibliographiques

## 🏥 Types d'infections couvertes

- Colonisation asymptomatique
- Cystite aiguë (y compris pendant la grossesse)
- Cystite récidivante
- Pyélonéphrite aiguë
- Infections urinaires masculines

## 🛠️ Installation

1. Clonez ce repository :

```bash
git clone https://github.com/[votre-username]/TogoATB.git
cd TogoATB
```

2. Créez un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

Lancez l'application Streamlit :

```bash
streamlit run main.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

## 📋 Comment utiliser l'assistant

1. Répondez aux questions cliniques présentées
2. Suivez l'arbre décisionnel en sélectionnant les options appropriées
3. Obtenez une recommandation thérapeutique personnalisée
4. Consultez les références cliniques associées
5. Visualisez le chemin décisionnel parcouru

## 🔧 Structure du projet

```
TogoATB/
├── main.py              # Application principale Streamlit
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## 📚 Technologies utilisées

- **Streamlit** : Interface web interactive
- **Plotly** : Visualisation de l'arbre décisionnel
- **Python** : Langage de programmation

## ⚕️ Avertissement médical

Cette application est un outil d'aide à la décision et ne remplace pas le jugement clinique professionnel. Les recommandations doivent toujours être adaptées au contexte clinique spécifique du patient.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.
