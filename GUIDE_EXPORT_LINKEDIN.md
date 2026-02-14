# 📥 Guide d'Export des Données LinkedIn

## Pourquoi exporter vos données ?

L'API LinkedIn n'étant plus accessible pour les profils personnels, LinkedIn propose une fonctionnalité officielle pour télécharger **toutes vos données de profil** en CSV.

## 📋 Étapes pour Exporter vos Données

### 1. Accéder aux Paramètres

1. Connectez-vous sur [LinkedIn.com](https://www.linkedin.com)
2. Cliquez sur votre **photo de profil** (en haut à droite)
3. Sélectionnez **Paramètres et confidentialité**

### 2. Demander vos Données

1. Dans le menu de gauche, allez dans **Confidentialité des données**
2. Cherchez la section **"Obtenir une copie de vos données"**
3. Cliquez sur **"Demander une archive"**

### 3. Sélectionner les Données

Vous pouvez choisir entre :

**Option rapide (Recommandé)** :
- Cochez **"Sélection rapide"**
- Choisissez **"Profil"** (contient tout ce qu'il faut)

**Option personnalisée** :
Cochez au minimum :
- ✅ Profile (informations de base)
- ✅ Positions (expériences)
- ✅ Education (formation)
- ✅ Skills (compétences)

### 4. Télécharger l'Archive

1. Cliquez sur **"Demander l'archive"**
2. LinkedIn va préparer vos données (10 minutes à quelques heures)
3. Vous recevrez un **email** quand c'est prêt
4. Retournez sur la même page et cliquez sur **"Télécharger"**

### 5. Extraire le ZIP

1. Téléchargez le fichier `.zip`
2. **Extrayez-le** dans un dossier de votre choix
3. Vous verrez des fichiers CSV : `Profile.csv`, `Positions.csv`, `Education.csv`, `Skills.csv`

## 🚀 Utiliser l'Export avec le Générateur

### Méthode 1 : Via le Menu Interactif

```bash
python linkedin_cv_generator.py
# Choisissez l'option 2
# Entrez le chemin vers le dossier extrait
```

### Méthode 2 : Via Python

```python
from linkedin_cv_generator import LinkedInCVGenerator

generator = LinkedInCVGenerator(template_dir="templates")

# Remplacez par le chemin de votre dossier extrait
data = generator.parse_linkedin_export("/chemin/vers/dossier/Basic_LinkedInDataExport")

# Générer le CV
generator.generate_cv(data, "mon_cv.html")
```

## 📂 Structure de l'Archive LinkedIn

Après extraction, vous aurez :

```
Basic_LinkedInDataExport_12-31-2024/
├── Profile.csv          ← Nom, titre, résumé, localisation
├── Positions.csv        ← Expériences professionnelles
├── Education.csv        ← Formations et diplômes
├── Skills.csv           ← Compétences
├── Certifications.csv   (optionnel)
├── Languages.csv        (optionnel)
└── ... autres fichiers
```

## 🔍 Fichiers Importants

### Profile.csv
Contient : Prénom, Nom, Titre, Résumé, Localisation, Email

### Positions.csv
Contient : Titre du poste, Entreprise, Dates, Description, Localisation

### Education.csv
Contient : École, Diplôme, Domaine d'études, Dates

### Skills.csv
Contient : Nom de la compétence

## ⚠️ Points d'Attention

### Encoding
Les fichiers CSV utilisent l'encodage **UTF-8**. Si vous voyez des caractères étranges :
- Ouvrez avec un éditeur UTF-8 (VS Code, Sublime Text)
- Évitez Excel qui peut mal gérer l'encodage

### Format des Dates
LinkedIn utilise le format **YYYY-MM-DD** ou parfois juste **YYYY**
Le générateur convertit automatiquement en français (ex: "Janvier 2020")

### Descriptions Vides
Si certaines descriptions sont vides dans le CSV, c'est normal si vous ne les aviez pas remplies sur LinkedIn.

## 💡 Astuces

### Modifier l'Export
Avant d'importer, vous pouvez éditer les CSV pour :
- Corriger des fautes
- Améliorer les descriptions
- Ajouter des informations manquantes

**Attention** : Gardez la structure du CSV (même nombre de colonnes)

### Plusieurs Versions
Vous pouvez demander plusieurs exports LinkedIn et garder différentes versions de votre CV.

### Confidentialité
L'export contient vos données personnelles. **Ne le partagez pas** et supprimez-le après utilisation.

## 🆘 Problèmes Courants

### "Fichier Profile.csv introuvable"
- Vérifiez que vous avez bien extrait le ZIP
- Pointez vers le bon dossier (celui qui contient les .csv)
- Le nom du dossier peut varier : `Basic_LinkedInDataExport_DATE`

### "Erreur d'encodage"
```python
# Si vous avez une erreur, essayez d'ouvrir avec 'latin-1'
with open(file, 'r', encoding='latin-1') as f:
```

### "Données manquantes"
Si des champs sont vides :
1. Vérifiez votre profil LinkedIn
2. Complétez les informations manquantes
3. Redemandez un export
4. Ou utilisez la méthode interactive pour compléter

## 🔄 Fréquence de Mise à Jour

LinkedIn vous permet de demander vos données **une fois toutes les 24 heures**.

Si vous avez mis à jour votre profil :
1. Attendez 24h depuis le dernier export
2. Redemandez un nouvel export
3. Régénérez votre CV

## 📧 Email de Notification

Vous recevrez un email de LinkedIn avec :
- **Sujet** : "Your LinkedIn data export is ready"
- **Délai** : Généralement 10-30 minutes
- **Validité** : Le lien de téléchargement expire après 72 heures

## ✅ Checklist Avant d'Exporter

Avant de demander votre export, assurez-vous que votre profil LinkedIn est à jour :

- [ ] Photo de profil professionnelle
- [ ] Titre accrocheur
- [ ] Résumé convaincant
- [ ] Expériences complètes avec descriptions
- [ ] Formations ajoutées
- [ ] Compétences listées
- [ ] Localisation précise
- [ ] Email de contact

---

**Une fois votre export prêt, lancez le générateur et créez votre CV en quelques minutes !** 🚀
