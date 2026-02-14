# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Tester avec des données de démonstration

```bash
python linkedin_cv_generator.py
```

Un fichier `cv.html` sera généré avec des données d'exemple. Ouvrez-le dans votre navigateur !

### 3️⃣ Utiliser vos vraies données LinkedIn

#### Option A : Authentification automatique

```bash
python linkedin_oauth.py
```

Suivez les instructions à l'écran pour obtenir votre access token.

#### Option B : Configuration manuelle

1. Copiez `config.example.py` vers `config.py`
2. Ajoutez vos credentials LinkedIn
3. Modifiez `linkedin_cv_generator.py` pour utiliser votre config

```python
# Dans linkedin_cv_generator.py, fonction main()
from config import LINKEDIN_ACCESS_TOKEN

access_token = LINKEDIN_ACCESS_TOKEN
raw_data = generator.fetch_linkedin_data(access_token)
parsed_data = generator.parse_linkedin_data(raw_data)
output_file = generator.generate_cv(parsed_data, "mon_cv.html")
```

## 📱 Export en PDF

1. Ouvrez le fichier HTML généré
2. `Ctrl + P` (Windows) ou `Cmd + P` (Mac)
3. Sélectionnez "Enregistrer en PDF"

## 🎨 Personnalisation Rapide

Éditez `templates/cv_template.html` et modifiez les variables CSS :

```css
:root {
    --color-primary: #1a1a2e;     /* Votre couleur principale */
    --color-accent: #c7956d;      /* Couleur d'accent */
    --font-serif: 'Crimson Pro';  /* Police pour les titres */
}
```

## 🆘 Problèmes Courants

### Erreur d'import Jinja2
```bash
pip install jinja2 --upgrade
```

### Erreur d'API LinkedIn
- Vérifiez que votre token est valide
- Assurez-vous d'avoir les bonnes permissions OAuth
- Le token expire après un certain temps

### Le design ne s'affiche pas correctement
- Vérifiez votre connexion Internet (polices Google Fonts)
- Essayez un autre navigateur (Chrome/Firefox recommandés)

## 💡 Astuces

- **Thème sombre** : Changez `--color-background` vers une couleur foncée
- **Impression parfaite** : Utilisez Chrome pour l'export PDF
- **Multi-langues** : Modifiez les labels dans le template HTML

## 📧 Besoin d'aide ?

Consultez le `README.md` complet pour plus de détails !