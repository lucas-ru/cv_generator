# 🎨 LinkedIn CV Generator

Un générateur de CV élégant et professionnel qui transforme vos données LinkedIn en un magnifique document HTML/CSS optimisé pour le format A4.

## ⚠️ Important - API LinkedIn

**L'API LinkedIn officielle n'est plus accessible pour les profils personnels.** Les anciennes routes API v2 sont obsolètes et nécessitent maintenant une application d'entreprise approuvée par LinkedIn.

Pour les profils personnels, voici les **3 méthodes disponibles** :

## ✨ Méthodes Disponibles

### 1️⃣ Saisie Interactive (Recommandé) ⭐

La méthode la plus simple et rapide pour créer votre CV.

```bash
python linkedin_cv_generator.py
# Choisissez l'option 1
```

Le script vous guidera pour saisir :
- Informations personnelles
- Expériences professionnelles
- Formation
- Compétences

### 2️⃣ Import depuis Export LinkedIn

LinkedIn vous permet de télécharger toutes vos données.

**Étapes :**
1. Allez sur [LinkedIn](https://www.linkedin.com)
2. **Paramètres et confidentialité** > **Confidentialité des données**
3. **Obtenir une copie de vos données**
4. Sélectionnez : Profile, Positions, Education, Skills
5. Téléchargez l'archive ZIP
6. Extrayez le ZIP

**Utilisation :**
```python
from linkedin_cv_generator import LinkedInCVGenerator

generator = LinkedInCVGenerator(template_dir="templates")
data = generator.parse_linkedin_export("/chemin/vers/dossier/extrait")
generator.generate_cv(data, "mon_cv.html")
```
### 3️⃣ Import d'un JSON

Pour utiliser un JSON quelques parts en local (il faut qu'il match avec celui généré en saisie intéractive).
Un json est généré apres la saisie intéractive(1️⃣) pour faciliter les modifications

```bash
python linkedin_cv_generator.py
# Choisissez l'option 3
```

### 4️⃣ Données de Démonstration

Pour tester le template rapidement.

```bash
python linkedin_cv_generator.py
# Choisissez l'option 4
```

## 🚀 Installation

```bash
# Installer les dépendances Python
pip install -r requirements.txt
```

## 💻 Utilisation Rapide

```bash
# Méthode interactive (la plus simple)
python linkedin_cv_generator.py
```

Suivez les instructions à l'écran, remplissez vos informations, et votre CV sera généré en quelques minutes !

## 📄 Export en PDF

Une fois votre CV généré :

1. **Ouvrez** `cv.html` dans **Google Chrome**
2. **Appuyez** sur `Ctrl + P` (Windows) ou `Cmd + P` (Mac)
3. **Configurez** :
   - Destination : "Enregistrer au format PDF"
   - Mise en page : Portrait
   - Marges : Aucune
   - ✅ **Cochez "Graphiques d'arrière-plan"** (très important !)
4. **Enregistrez**

Votre CV A4 professionnel est prêt ! 🎉

## 🎨 Caractéristiques du Design

- **Format A4 exact** : 210mm × 297mm, optimisé pour tenir sur une page
- **Design original et sophistiqué** : Palette de couleurs raffinée inspirée de l'art contemporain
- **Animations fluides** : Transitions CSS élégantes (désactivées en print)
- **Typographie raffinée** : Crimson Pro (serif) + DM Sans (sans-serif)
- **Optimisé PDF** : Couleurs préservées, pas de coupure de sections
- **Template Jinja2** : Facilement personnalisable et extensible
- **Responsive** : S'adapte aux écrans mobile, tablette et desktop

## 📁 Structure du Projet

```
linkedin-cv-generator/
│
├── linkedin_cv_generator.py    # Application principale avec menu interactif
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── QUICKSTART.md              # Guide de démarrage rapide
├── EXPORT_PDF.md              # Guide d'export PDF détaillé
│
└── templates/
    └── cv_template.html        # Template Jinja2 HTML/CSS optimisé A4
```

## 🎯 Fonctionnalités du Template

### Design Elements

- **Header sophistiqué** : Fond dégradé avec motif géométrique subtil
- **Typographie raffinée** : Combinaison de polices serif/sans-serif
- **Éléments décoratifs** : Formes abstraites en arrière-plan
- **Badges de dates** : Mise en valeur des périodes professionnelles
- **Grid moderne** : Layout à deux colonnes pour organisation optimale
- **Animations** : Fade-in et slide-in au chargement

### Sections Incluses

1. **En-tête** : Nom, titre professionnel, coordonnées
2. **Résumé** : Présentation professionnelle
3. **Expériences** : Historique professionnel détaillé
4. **Formation** : Parcours académique
5. **Compétences** : Skills avec nombre d'endorsements

## 🎯 Personnalisation

### Changer les couleurs

Éditez `templates/cv_template.html` :

```css
:root {
    --color-primary: #1a1a2e;        /* Couleur principale */
    --color-accent: #c7956d;         /* Couleur d'accent */
    --color-accent-light: #e8d5c4;   /* Accent clair */
}
```

### Ajuster l'espacement

```css
:root {
    --space-xs: 0.35rem;  /* Espace minimal */
    --space-sm: 0.6rem;   /* Espace petit */
    --space-md: 0.9rem;   /* Espace moyen */
}
```

### Limiter le nombre de compétences affichées

Dans le template HTML (ligne ~380) :

```html
{% for skill in skills[:10] %}  <!-- Limiter à 10 compétences -->
```

## 📝 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer le design
- Ajouter de nouveaux templates

## 📞 Support

Pour toute question ou problème :

- Ouvrez une issue sur GitHub
- Consultez la documentation de l'API LinkedIn
- Vérifiez que vos tokens d'accès sont valides

## 🌟 Fonctionnalités

✅ **Saisie interactive** pour création rapide  
✅ **Import depuis export LinkedIn** (CSV)  
✅ **Format A4 exact** (210mm × 297mm)  
✅ **Export PDF optimisé** avec préservation des couleurs  
✅ **Template élégant** avec design professionnel  
✅ **Responsive** pour tous les écrans  

## 💡 Améliorations Futures

- [ ] Templates multiples au choix (moderne, classique, créatif)
- [ ] Thèmes de couleurs prédéfinis
- [ ] Support multilingue (EN, ES, DE)
- [ ] Export direct en PDF depuis Python
- [ ] Interface web Flask/Streamlit
- [ ] Intégration avec d'autres sources (GitHub, Portfolio)

---

**Créé avec ❤️ pour des CV professionnels qui se démarquent**
