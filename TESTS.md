# Exécuter les tests pytest

Ce fichier explique comment exécuter les tests unitaires pour le générateur de CV.

Pré-requis
- Accès réseau pour installer les dépendances (si non installées localement)

Étapes (Windows PowerShell)

1. (Prérequis) Avoir suivi le readMe.md

4. Lancer la suite de tests

```powershell
# lancer tous les tests du module
python -m pytest -q .\scripts\cv_generator\tests

# ou lancer un seul fichier de tests
python -m pytest -q .\scripts\cv_generator\tests\test_generator.py
```

Conseils
- Pour un affichage verbeux : `python -m pytest -v`.
- Si vous rencontrez des erreurs liées à `pip` ou aux paquets, exécutez `python -m pip install --upgrade pip setuptools wheel`.
