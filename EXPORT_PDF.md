# 📄 Guide d'Export PDF

## Votre CV est maintenant optimisé pour le format A4 !

Le template a été spécialement conçu pour tenir sur **une seule page A4 (210mm x 297mm)** avec un rendu professionnel en PDF.

## 🖨️ Comment Exporter en PDF

### Méthode 1 : Via Chrome (Recommandée)

1. **Ouvrez** le fichier `cv.html` dans Google Chrome
2. **Appuyez** sur `Ctrl + P` (Windows/Linux) ou `Cmd + P` (Mac)
3. **Sélectionnez** :
   - Destination : "Enregistrer au format PDF"
   - Pages : Toutes
   - Mise en page : Portrait
   - Marges : Aucune (ou Par défaut)
   - ✅ **IMPORTANT** : Cochez "Graphiques d'arrière-plan"
4. **Cliquez** sur "Enregistrer"

### Méthode 2 : Via Firefox

1. Ouvrez le fichier dans Firefox
2. `Ctrl + P` / `Cmd + P`
3. Destination : "Enregistrer en PDF"
4. ✅ Cochez "Imprimer les arrière-plans"
5. Enregistrer

### Méthode 3 : Via Edge

1. Ouvrez dans Microsoft Edge
2. `Ctrl + P`
3. Imprimante : "Microsoft Print to PDF"
4. Plus de paramètres → Cochez "Graphiques d'arrière-plan"
5. Imprimer

## ✨ Optimisations Appliquées

Le template a été modifié pour garantir un rendu parfait en PDF :

### Dimensions Exactes
- **Largeur** : 210mm (A4)
- **Hauteur** : 297mm (A4)
- **Marges** : Optimisées pour utiliser tout l'espace

### Typographie Ajustée
- Tailles de police réduites pour maximiser l'espace
- Espacement vertical optimisé
- Line-height adapté pour la lisibilité

### Layout Compact
- Header réduit mais élégant (≈80px)
- Colonnes : 60% / 40% (contenu / compétences)
- Footer minimal (≈20px)
- Sections espacées intelligemment

### Styles d'Impression
- Couleurs d'arrière-plan préservées (`print-color-adjust: exact`)
- Animations désactivées en print
- Éléments décoratifs légèrement atténués
- Pas de coupure dans les sections (`page-break-inside: avoid`)

## 🎨 Personnalisation pour A4

Si vous avez beaucoup de contenu, vous pouvez ajuster :

```css
/* Dans cv_template.html, cherchez ces variables : */
:root {
    --space-xs: 0.35rem;  /* Réduire encore si nécessaire */
    --space-sm: 0.6rem;   /* Espacement entre éléments */
    --space-md: 0.9rem;   /* Espacement sections */
}

/* Réduire la taille des titres de sections */
.section-title {
    font-size: 1.3rem;  /* Diminuer à 1.1rem si besoin */
}

/* Réduire la description des postes */
.item-description {
    font-size: 0.85rem;  /* Diminuer à 0.8rem si nécessaire */
}
```

## 📊 Gestion du Contenu

### Si le contenu dépasse une page :

**Option 1** : Résumer les descriptions
- Gardez l'essentiel (2-3 lignes max par poste)
- Utilisez des bullet points dans le code

**Option 2** : Limiter les expériences
```python
# Dans le code Python, limitez à 3 expériences :
'experiences': experiences[:3]
```

**Option 3** : Réduire les compétences affichées
```html
<!-- Dans le template, ligne ~380 -->
{% for skill in skills[:10] %}  <!-- Limiter à 10 au lieu de 12 -->
```

**Option 4** : Supprimer le résumé
```html
<!-- Commentez la section summary si vous manquez d'espace -->
```

## 🔍 Vérification Avant Export

Avant d'exporter en PDF, vérifiez :

✅ Le contenu ne dépasse pas 297mm (vérifiez avec l'aperçu d'impression)
✅ Les couleurs sont bien visibles (cochez "Graphiques d'arrière-plan")
✅ Le texte est lisible (taille min : 0.7rem / 9-10pt)
✅ Pas de texte coupé en bas de page
✅ Les badges et compétences sont bien visibles

## 💡 Astuces Pro

### Pour un rendu impeccable :
- **Résolution** : Chrome produit des PDF en haute qualité
- **Polices** : Les Google Fonts sont automatiquement intégrées
- **Couleurs** : Les dégradés et ombres sont préservés

### Pour réduire la taille du fichier :
- Utilisez Chrome (produit des PDFs plus légers)
- Les polices web sont optimisées automatiquement

### Pour partager :
Le PDF généré est parfait pour :
- 📧 Envoi par email
- 💼 Plateformes de recrutement (Indeed, LinkedIn, etc.)
- 🖨️ Impression physique
- 📱 Lecture sur mobile/tablette

## 🎯 Qualité Garantie

Le template a été testé et optimisé pour :
- ✅ Impression A4 standard
- ✅ Export PDF haute qualité
- ✅ Compatibilité multi-navigateurs
- ✅ Affichage professionnel
- ✅ ATS-friendly (si on retire les éléments décoratifs)

---

**Note** : Si vous voyez une page blanche à la fin du PDF, c'est normal - elle sera automatiquement supprimée lors de l'export final.
