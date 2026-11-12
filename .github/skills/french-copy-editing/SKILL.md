---
name: french-copy-editing
description: Rédiger et réviser un CV en français professionnel, idiomatique, clair et fidèle aux faits du profil.
---

# Rédaction professionnelle en français

Applique ce skill lorsque la langue principale de l'offre est le français.

## Procédure de révision

1. Lire l'offre et le profil source avant de réviser le résumé, les expériences ou les libellés du CV.
2. Employer un français professionnel naturel, précis et concis. Éviter les traductions littérales, le jargon gratuit, les formulations creuses, les répétitions et les phrases excessivement longues.
3. Corriger syntaxe, grammaire, orthographe, accords, conjugaison, ponctuation, espaces typographiques et cohérence des temps.
4. Utiliser des verbes d'action adaptés aux faits du profil. Garder les intitulés d'emplois, dates, diplômes, outils et responsabilités vérifiables.
5. Reformuler pour la lisibilité sans ajouter de résultats, de métriques, de responsabilités ou de niveaux de maîtrise absents des sources.
6. Harmoniser le vocabulaire du CV et les libellés visibles du template en français. Préserver les noms officiels de technologies et d'entreprises.
7. Ne jamais ajouter une date de génération, une signature automatique, ni la mention « (poste visé) ».
8. Relire le headline comme un vrai intitulé professionnel : éviter d'assembler le poste actuel et le poste ciblé avec un tiret ou une barre oblique. Garder le poste ciblé seul dans le titre et laisser le résumé présenter le parcours.

## Résumé : soft skills et intérêt pour le poste

- Ouvrir le résumé sur une ou deux soft skills pertinentes et étayées, puis exprimer la motivation personnelle du candidat si elle a été fournie ou confirmée. Garder les hard skills comme preuves d'appui, sans transformer le résumé en inventaire technique.
- Comparer les qualités recherchées dans l'offre avec les déclarations et actions concrètes du profil. Les attentes de l'employeur et les recherches Web sur l'entreprise servent à comprendre le contexte, pas à attribuer des qualités au candidat.
- Ne pas inférer un leadership, une aisance relationnelle, une organisation ou une motivation à partir d'un poste, d'une technologie ou d'un hobby. Si les éléments manquent, demander à l'utilisateur ce qu'il souhaite mettre en avant et ce qui l'attire dans le poste ; attendre sa confirmation avant d'ajouter ces affirmations.
- Si l'utilisateur ne précise pas sa motivation, conserver un résumé factuel et signaler que son intérêt personnel n'a pas pu être établi.

## Scénario : adapter une expérience DevOps à une offre française

À partir d'une source telle que « Création de modèle CI/CD. Automatisation de processus métier. Mise en place de norme pour l'observabilité », produire une phrase lisible qui conserve exactement ces faits, par exemple :

> Conçu des modèles CI/CD, automatisé des processus métier et contribué à la mise en place de normes d'observabilité.

Ne pas ajouter d'impact chiffré, de technologie ou de responsabilité managériale sans preuve dans le profil.

## Sortie

Pour une tâche de CV, réviser les champs textuels dans `.cv-work/cv_profile.json` et les textes d'interface visibles dans `.cv-work/cv_template.html`. Signaler à l'agent HTML Builder que les fichiers sont prêts à rendre et résumer les changements rédactionnels importants.

Lorsque Cover Letter Writer confie une lettre, appliquer les mêmes règles de langue et de fidélité aux faits au fichier de lettre indiqué. Préserver sa structure en trois parties, ne modifier que la lettre et la renvoyer à l'orchestrateur pour relecture ; ne pas modifier le profil ni le template du CV dans le cadre de cette tâche.
