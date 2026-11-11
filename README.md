# CV Generator

Générateur de CV HTML ciblés sur une offre d'emploi. Le flux principal s'appuie sur des agents Copilot définis dans [`.github/agents/`](./.github/agents/) : ils analysent l'offre, importent un export PDF LinkedIn local, recherchent l'identité visuelle de l'entreprise, conçoivent le CV et vérifient l'alignement ATS à partir d'informations réelles. Le HTML généré peut être ouvert dans un navigateur puis imprimé en PDF.

Le projet ne consulte pas LinkedIn en ligne et ne demande ni URL de profil ni endpoint. Il lit localement le PDF exporté par LinkedIn placé dans `data/`. Si le PDF est absent ou ne correspond pas au format attendu, l'importeur utilise un profil JSON du même dossier. Aucune URL LinkedIn ni contenu invisible destiné à manipuler un système de tri n'est ajouté au CV.

## Prérequis

- Python 3.9 ou supérieur
- Visual Studio Code avec Copilot Chat pour utiliser les agents

Installer les dépendances Python :

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Structure du projet

- `scripts/` : commandes Python de génération HTML et d'import PDF LinkedIn.
- `tests/` : tests unitaires `pytest` et tests E2E Playwright.
- `templates/` : modèles HTML intégrés.
- `data/` : données locales de profil, PDF et photos ; leur contenu est ignoré par Git, sauf `.gitkeep`.
- `outputs/` : CV générés ; leur contenu est ignoré par Git, sauf `.gitkeep`.
- `.github/agents/` et `.github/skills/` : agents et instructions de travail Copilot.

## Utiliser le flux agentique

1. Ouvrir le dossier du projet dans VS Code et lancer Copilot Chat.
2. Sélectionner l'agent **CV Orchestrator** (ou lui demander directement de préparer un CV).
3. Fournir l'URL de l'offre ou coller son texte. L'agent peut demander le texte si l'URL n'est pas accessible.
4. L'orchestrateur cherche automatiquement un export LinkedIn PDF dans `data/`. S'il existe, l'importeur vérifie qu'il suit le format attendu et extrait ses informations. Si le PDF est absent ou invalide, il utilise `data.json` s'il existe, sinon l'unique JSON présent dans le dossier. En cas de plusieurs JSON sans `data.json`, l'orchestrateur demande lequel choisir.
5. L'orchestrateur coordonne l'analyse de l'offre, l'import du profil, la recherche d'identité visuelle, le design, la sélection d'expériences pertinentes, la relecture dans la langue de l'offre et le contrôle ATS. Les expériences sans rapport avec le poste sont écartées, sauf si leur description prouve une compétence transférable utile.
6. Après génération du HTML, `CV Playwright Reviewer` compare son rendu au template UX, exporte un PDF A4 avec les graphiques d'arrière-plan et vérifie le contenu et les pages blanches. `CV Workflow Improver` accepte ou rejette le rapport avant sa présentation.
7. Vérifier les informations et le rendu A4. Après génération et validation Playwright, l'orchestrateur demande un retour sur le contenu, le résumé, les compétences, les expériences, le design comparé au template et la mise en page. Indiquez vos corrections dans le chat ; l'agent régénère le HTML et relance les vérifications. Si tout vous convient, confirmez-le explicitement.
8. Ouvrir le HTML dans un navigateur et faire **Imprimer > Enregistrer au format PDF**.

Les agents échangent leurs fichiers intermédiaires dans `.cv-work/`, notamment `.cv-work/linkedin_profile.json`. L'importeur écrit le résultat du PDF reconnu ou du JSON de repli et relève les noms des photos locales candidates. Quand un PDF est valide, ses champs absents restent vides et ne sont pas complétés par un autre JSON. Pour la photo, la seule source est une image `.png`, `.jpg` ou `.jpeg` présente dans `data/` : le PDF LinkedIn ne contient pas de photo exploitable pour ce flux. Si aucune photo locale n'existe, le template est composé sans image ni espace vide réservé. S'il y a plusieurs photos locales, indiquez celle à utiliser. Les templates de [templates/](./templates/) sont les bases de design lorsque la recherche de marque n'aboutit pas.

Un téléphone absent n'est pas affiché et ne réserve aucun espace dans le header.

Le PDF d'export peut ne pas contenir de hobbies. Dans ce cas, l'importeur peut rechercher quatre idées adaptées au poste et les enregistrer séparément avec leurs sources dans `.cv-work/hobby_suggestions.json`. Ces idées ne sont jamais présentées comme les hobbies du candidat : confirmez uniquement celles que vous pratiquez réellement. Sans confirmation, la rubrique reste absente du CV.

Pour lancer uniquement l'import du profil :

```powershell
python .\scripts\linkedin_pdf_importer.py --data-dir .\data --output .\.cv-work\linkedin_profile.json
```

Le format PDF attendu est celui de l'export LinkedIn standard en français. Si les sections ne sont pas reconnues, l'importeur indique le repli JSON dans `source_notes` au lieu d'interpréter le document comme un profil valide.

Les agents conservent les catégories non vides du profil, dont Compétences et Hobbies. Les hobbies et compétences sourcés ne sont pas supprimés pour raccourcir le CV ; les éléments les plus pertinents peuvent être placés en premier et la mise en page peut continuer sur plusieurs pages.

### Prioriser les templates en l'absence de charte

Quand aucune direction visuelle fiable n'est trouvée, le skill [cv-template-fallback](./.github/skills/cv-template-fallback/SKILL.md) classe les templates par poids : **plus le poids est élevé, moins le template est préféré**. La sélection prend le poids le plus bas parmi les designs capables de présenter le contenu de façon lisible et imprimable.

| Template | Poids actuel |
| --- | ---: |
| `cv_template_1.html` | 1 |
| `cv_template_2.html` | 8 |
| `cv_template_3.html` | 3 |
| `cv_template_4.html` | 7 |

Pour changer cette préférence, modifiez les valeurs dans la section **Template preference weights** du fichier [`.github/skills/cv-template-fallback/SKILL.md`](./.github/skills/cv-template-fallback/SKILL.md), puis mettez à jour ce tableau dans le README. Il n'est pas nécessaire de modifier le code Python. Une identité visuelle vérifiée reste prioritaire sur ces poids ; ceux-ci s'appliquent au fallback sans charte exploitable.

## Génération Python directe

Pour rendre un profil JSON déjà adapté (par exemple préparé par les agents) avec l'un des quatre templates :

```powershell
python .\scripts\cv_generator.py --data .\data\data.json --template 1 --output .\outputs\cv.html
```

Choix intégrés : `1` (moderne), `2` (Swiss), `3` (corporate), `4` (éditorial). Pour un template créé par l'agent UX :

```powershell
python .\scripts\cv_generator.py --data .\.cv-work\cv_profile.json --template-file .\.cv-work\cv_template.html --output .\outputs\cv-cible.html
```

Vous pouvez forcer une photo si plusieurs sont présentes :

```powershell
python .\scripts\cv_generator.py --data .\.cv-work\cv_profile.json --photo .\data\portrait.jpg --template-file .\.cv-work\cv_template.html --output .\outputs\cv-cible.html
```

La photo est intégrée au HTML pour éviter les liens locaux cassés lors de son déplacement.

Le JSON utilise la structure déjà présente dans `data/data.json` (`personal_info`, `experiences`, `education`, `skills`, `hobbies`). Les éléments d'expérience restent factuels ; seul le titre ciblé, le résumé et l'ordre des éléments peuvent être adaptés sans inventer d'expérience ni de compétence.

## Agents

- `cv-orchestrator.agent.md` : pilote les étapes et contrôle leurs livrables.
- `cv-workflow-improver.agent.md` : partage les leçons durables et corrige les consignes uniquement à partir de problèmes vérifiés et récurrents.
- `linkedin-pdf-profile-importer.agent.md` : importe l'export PDF LinkedIn local et utilise un JSON de `data/` si le PDF manque ou n'est pas au bon format.
- `job-offer-analyst.agent.md` : extrait les exigences et relie les missions à des compétences justifiées.
- `company-researcher.agent.md` : documente l'entreprise et sa direction visuelle.
- `cv-ux-designer.agent.md` : crée le template HTML imprimable et s'appuie sur le skill de fallback si la charte est inconnue.
- `cv-html-builder.agent.md` : expert Python/pytest, adapte les données, génère le HTML et teste les modifications du code ou du template.
- `cv-playwright-reviewer.agent.md` : vérifie après génération le HTML, la correspondance visuelle avec le template et l'export PDF A4.
- `cv-copy-editor.agent.md` : relit le profil et le template selon la langue réelle de l'offre.
- `ats-keyword-reviewer.agent.md` : repère les mots-clés pertinents à faire apparaître explicitement et honnêtement.

Skills du projet : [qualité Python](./.github/skills/python-quality/SKILL.md) et [workflow pytest](./.github/skills/pytest-workflow/SKILL.md) s'appliquent aux scripts `scripts/cv_generator.py` et `scripts/linkedin_pdf_importer.py` ; [Playwright CV E2E](./.github/skills/cv-playwright-e2e/SKILL.md) définit le contrôle du HTML, de la comparaison au template et du PDF. Les autres skills couvrent le [design de fallback](./.github/skills/cv-template-fallback/SKILL.md), la [mise en page A4](./.github/skills/cv-print-layout/SKILL.md), la [rédaction française](./.github/skills/french-copy-editing/SKILL.md) et la [rédaction anglaise](./.github/skills/english-copy-editing/SKILL.md). [CV Workflow Improver](./.github/agents/cv-workflow-improver.agent.md) transmet les leçons issues de problèmes confirmés et récurrents à l'orchestrateur et aux agents concernés.

Le registre [agent-feedback.json](./.github/agent-feedback.json) conserve uniquement des résumés techniques anonymisés ; il ne doit jamais contenir de données de profil ou de contenu d'offre.

## Tests

```powershell
python -m pytest -q .\tests
```

Après la finalisation d'un CV, l'orchestrateur lance aussi le scénario E2E ciblé (le test complet est également inclus dans la suite lorsqu'il trouve les fichiers générés) :

```powershell
$env:CV_E2E_HTML = ".\outputs\cv-cible.html"
$env:CV_E2E_TEMPLATE = ".\.cv-work\cv_template.html"
$env:CV_E2E_PROFILE = ".\.cv-work\cv_profile.json"
$env:CV_E2E_EVIDENCE_DIR = ".\.cv-work\playwright-review"
python -m pytest -q -s .\tests\e2e\test_final_cv_playwright.py
```

Les captures comparatives, le PDF de prévisualisation et le rapport sont conservés localement dans `.cv-work/playwright-review/` et ne doivent pas être partagés ni ajoutés au dépôt.

## Exporter en PDF

1. Ouvrir le fichier HTML généré dans Chrome, Edge ou Firefox.
2. Lancer l'impression avec `Ctrl + P`, puis choisir **Enregistrer au format PDF**.
3. Sélectionner le format A4, l'orientation portrait et activer les graphiques d'arrière-plan.
4. Garder l'échelle à 100 % et activer les graphiques d'arrière-plan : le bandeau de marque et les accents du template en dépendent. Vérifier l'aperçu ; un CV assez court doit tenir sur une page sans page blanche ajoutée.
5. Si le contenu dépasse réellement une page, vérifier que le saut de page intervient au milieu d'une section cohérente, puis enregistrer.

Le contenu peut dépasser une page selon la longueur du CV. Dans ce cas, synthétiser les descriptions plutôt que de réduire le texte au point de nuire à sa lisibilité.
