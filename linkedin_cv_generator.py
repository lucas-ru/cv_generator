"""
LinkedIn CV Generator
Génère un CV élégant à partir de vos données LinkedIn
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader
import json

ROOT = os.path.dirname(__file__)
TEMPLATES = os.path.join(ROOT, 'templates')
OUTPUTS = os.path.join(ROOT, 'outputs')
DATA = os.path.join(ROOT, 'data')

class LinkedInCVGenerator:
    """Générateur de CV à partir des données LinkedIn"""
    
    def __init__(self, template_dir: str = "templates"):
        """
        Initialise le générateur avec le répertoire des templates
        
        Args:
            template_dir: Chemin vers le dossier contenant les templates Jinja2
        """
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def parse_linkedin_export(self, export_dir: str) -> Dict:
        """
        Parse l'archive d'export de données LinkedIn
        
        Pour obtenir votre archive:
        1. LinkedIn > Paramètres et confidentialité
        2. Confidentialité des données > Obtenir une copie de vos données
        3. Sélectionnez tout ou "Profil", "Positions", "Education", "Skills"
        4. Téléchargez et extrayez l'archive ZIP
        
        Args:
            export_dir: Chemin vers le dossier extrait de l'archive LinkedIn
            
        Returns:
            Dictionnaire structuré pour le template
        """
        import csv
        
        data = {
            'personal_info': {},
            'experiences': [],
            'education': [],
            'skills': [],
            'hobbies': []
        }
        
        try:
            # Profile.csv - Informations personnelles
            profile_file = os.path.join(export_dir, 'Profile.csv')
            if os.path.exists(profile_file):
                with open(profile_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    profile = next(reader)
                    data['personal_info'] = {
                        'name': f"{profile.get('First Name', '')} {profile.get('Last Name', '')}",
                        'headline': profile.get('Headline', ''),
                        'summary': profile.get('Summary', ''),
                        'location': profile.get('Location', ''),
                        'email': profile.get('Email Address', ''),
                        'phone': '',
                        'linkedin_url': f"linkedin.com/in/{profile.get('Public Profile URL', '').split('/')[-1]}"
                    }
            
            # Positions.csv - Expériences professionnelles
            positions_file = os.path.join(export_dir, 'Positions.csv')
            if os.path.exists(positions_file):
                with open(positions_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        exp = {
                            'title': row.get('Title', ''),
                            'company': row.get('Company Name', ''),
                            'location': row.get('Location', ''),
                            'start_date': self._format_linkedin_export_date(row.get('Started On', '')),
                            'end_date': self._format_linkedin_export_date(row.get('Finished On', '')) or 'Présent',
                            'description': row.get('Description', ''),
                            'is_current': not row.get('Finished On')
                        }
                        data['experiences'].append(exp)
            
            # Education.csv - Formation
            education_file = os.path.join(export_dir, 'Education.csv')
            if os.path.exists(education_file):
                with open(education_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        edu = {
                            'school': row.get('School Name', ''),
                            'degree': row.get('Degree Name', ''),
                            'field': row.get('Notes', ''),
                            'start_date': self._format_linkedin_export_date(row.get('Start Date', '')),
                            'end_date': self._format_linkedin_export_date(row.get('End Date', '')),
                            'description': row.get('Activities', '')
                        }
                        data['education'].append(edu)
            
            # Skills.csv - Compétences
            skills_file = os.path.join(export_dir, 'Skills.csv')
            if os.path.exists(skills_file):
                with open(skills_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data['skills'].append({
                            'name': row.get('Name', ''),
                            'endorsements': 0
                        })
            
            data['generated_date'] = datetime.now().strftime('%d/%m/%Y')
            return data
            
        except Exception as e:
            print(f"❌ Erreur lors de la lecture de l'export LinkedIn: {e}")
            print("Assurez-vous d'avoir extrait l'archive ZIP et de pointer vers le bon dossier.")
            return None
    
    def _format_linkedin_export_date(self, date_str: str) -> Optional[str]:
        """
        Formate une date de l'export LinkedIn (format: YYYY-MM-DD ou YYYY)
        
        Args:
            date_str: Date au format de l'export
            
        Returns:
            Date formatée en français
        """
        if not date_str:
            return None
        
        months_fr = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        
        try:
            # Format YYYY-MM-DD
            if '-' in date_str:
                parts = date_str.split('-')
                year = parts[0]
                if len(parts) > 1 and parts[1]:
                    month = int(parts[1])
                    return f"{months_fr[month-1]} {year}"
                return year
            # Format YYYY uniquement
            return date_str
        except:
            return date_str
    
    def generate_from_manual_input(self, output_path: str = "data.json") -> Dict:
        """
        Génère un CV via saisie interactive
        Méthode recommandée pour les profils personnels LinkedIn
        
        Returns:
            Dictionnaire structuré pour le template
        """
        print("\n" + "="*60)
        print("CRÉATION DE CV - SAISIE INTERACTIVE")
        print("="*60)
        
        data = {
            'personal_info': {},
            'experiences': [],
            'education': [],
            'skills': [],
            'hobbies': [],
            'generated_date': datetime.now().strftime('%d/%m/%Y')
        }
        
        # Informations personnelles
        print("\n📝 INFORMATIONS PERSONNELLES")
        print("-" * 60)
        data['personal_info']['name'] = input("Nom complet: ").strip()
        data['personal_info']['headline'] = input("Titre professionnel: ").strip()
        data['personal_info']['email'] = input("Email: ").strip()
        data['personal_info']['phone'] = input("Téléphone (optionnel): ").strip()
        data['personal_info']['location'] = input("Localisation: ").strip()
        data['personal_info']['linkedin_url'] = input("URL LinkedIn (ex: linkedin.com/in/lucas-plume): ").strip()
        data['personal_info']['summary'] = input("Résumé professionnel (2-3 phrases): ").strip()
        # Lire et normaliser le chemin de la photo pour l'utiliser en HTML
        photo_input = input("Chemin vers la photo (optionnel): ").strip()
        if photo_input:
            # Permet d'expanser ~ et les variables d'environnement
            photo_expanded = os.path.expanduser(os.path.expandvars(photo_input))
            # Normaliser les séparateurs en slash pour HTML
            photo_normalized = photo_expanded.replace('\\', '/')
            # Si chemin absolu, convertir en URI file:/// pour que le navigateur le charge
            try:
                from pathlib import Path
                p = Path(photo_expanded)
                if p.is_absolute():
                    photo_url = p.as_uri()
                else:
                    photo_url = photo_normalized
            except Exception:
                photo_url = photo_normalized
        else:
            photo_url = ''
        data['personal_info']['photo'] = photo_url
        
        # Expériences
        print("\n💼 EXPÉRIENCES PROFESSIONNELLES")
        print("-" * 60)
        while True:
            print(f"\nExpérience #{len(data['experiences']) + 1}")
            exp = {}
            exp['title'] = input("  Poste: ").strip()
            if not exp['title']:
                break
            exp['company'] = input("  Entreprise: ").strip()
            exp['location'] = input("  Lieu: ").strip()
            exp['start_date'] = input("  Date de début (ex: Janvier 2020): ").strip()
            exp['end_date'] = input("  Date de fin (ou 'Présent'): ").strip()
            exp['is_current'] = exp['end_date'].lower() == 'présent'
            exp['description'] = input("  Description (2-3 lignes): ").strip()
            data['experiences'].append(exp)
            
            if input("\nAjouter une autre expérience? (o/n): ").lower() != 'o':
                break
        
        # Formation
        print("\n🎓 FORMATION")
        print("-" * 60)
        while True:
            print(f"\nFormation #{len(data['education']) + 1}")
            edu = {}
            edu['school'] = input("  École/Université: ").strip()
            if not edu['school']:
                break
            edu['degree'] = input("  Diplôme: ").strip()
            edu['field'] = input("  Spécialité: ").strip()
            edu['start_date'] = input("  Année de début: ").strip()
            edu['end_date'] = input("  Année de fin: ").strip()
            edu['description'] = input("  Description (optionnel): ").strip()
            data['education'].append(edu)
            
            if input("\nAjouter une autre formation? (o/n): ").lower() != 'o':
                break
        
        # Compétences
        print("\n🎯 COMPÉTENCES")
        print("-" * 60)
        print("Entrez vos compétences séparées par des virgules:")
        skills_input = input("Compétences: ").strip()
        if skills_input:
            for skill in skills_input.split(','):
                data['skills'].append({
                    'name': skill.strip(),
                    'endorsements': 0
                })

        # Hobbies (optionnel)
        print("\n🎲 HOBBIES (OPTIONNEL)")
        print("Entrez vos hobbies séparés par des virgules (laisser vide si aucun):")
        hobbies_input = input("Hobbies: ").strip()
        if hobbies_input:
            for h in hobbies_input.split(','):
                item = h.strip()
                if item:
                    data['hobbies'].append(item)
        
        print("\n✅ Saisie terminée!")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data
    
    def generate_cv(self, choix: str, data: Dict, output_path: str = "cv.html") -> str:
        """
        Génère le CV HTML à partir des données
        
        Args:
            data: Données structurées du profil
            output_path: Chemin du fichier HTML de sortie
            
        Returns:
            Chemin du fichier généré
        """
        template = self.env.get_template(f'cv_template_{choix}.html')
        html_content = template.render(**data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def generate_from_mock_data(self, choix: str, output_path: str = "cv.html") -> str:
        """
        Génère un CV à partir de données de démonstration
        Utile pour tester le template
        
        Args:
            output_path: Chemin du fichier HTML de sortie
            
        Returns:
            Chemin du fichier généré
        """
        mock_data = {
            'personal_info': {
                'name': 'Lucas Plume',
                'headline': 'Data Scientist | Expert en Machine Learning & IA',
                'location': 'Paris, Île-de-France, France',
                'email': 'lucas.plume@example.com',
                'phone': '+33 6 12 34 56 78',
                'linkedin_url': 'linkedin.com/in/lucas-plume',
                'summary': 'Data Scientist passionné avec 5 ans d\'expérience dans l\'analyse de données massives et le développement de modèles d\'apprentissage automatique. Spécialisé en NLP et Computer Vision, j\'accompagne les entreprises dans leur transformation data-driven.',
                'photo': ''
            },
            'experiences': [
                {
                    'title': 'Senior Data Scientist',
                    'company': 'Tech Innovation Lab',
                    'location': 'Paris, France',
                    'start_date': 'Mars 2021',
                    'end_date': 'Présent',
                    'description': 'Développement de modèles ML pour la détection de fraude (99.2% de précision). Direction d\'une équipe de 4 data scientists. Mise en production de 12 modèles sur AWS SageMaker.',
                    'is_current': True
                },
                {
                    'title': 'Data Scientist',
                    'company': 'DataCorp France',
                    'location': 'Lyon, France',
                    'start_date': 'Juin 2019',
                    'end_date': 'Février 2021',
                    'description': 'Analyse prédictive pour l\'optimisation des stocks. Développement d\'APIs de prédiction avec FastAPI. Création de dashboards interactifs avec Plotly et Streamlit.',
                    'is_current': False
                },
                {
                    'title': 'Data Analyst',
                    'company': 'Analytics Solutions',
                    'location': 'Paris, France',
                    'start_date': 'Septembre 2018',
                    'end_date': 'Mai 2019',
                    'description': 'Analyse de données clients et segmentation RFM. Création de rapports automatisés avec Python et Power BI. A/B testing et optimisation des campagnes marketing.',
                    'is_current': False
                }
            ],
            'education': [
                {
                    'school': 'CentraleSupélec',
                    'degree': 'Diplôme d\'Ingénieur',
                    'field': 'Data Science & Intelligence Artificielle',
                    'start_date': '2015',
                    'end_date': '2018',
                    'description': 'Major de promotion - Spécialisation Machine Learning & Big Data'
                },
                {
                    'school': 'Université Paris-Saclay',
                    'degree': 'Master',
                    'field': 'Mathématiques Appliquées',
                    'start_date': '2017',
                    'end_date': '2018',
                    'description': 'Double diplôme - Recherche en optimisation stochastique'
                }
            ],
            'skills': [
                {'name': 'Python', 'endorsements': 52},
                {'name': 'Machine Learning', 'endorsements': 48},
                {'name': 'Deep Learning (TensorFlow, PyTorch)', 'endorsements': 41},
                {'name': 'SQL / NoSQL', 'endorsements': 38},
                {'name': 'NLP (spaCy, Transformers)', 'endorsements': 35},
                {'name': 'Computer Vision (OpenCV)', 'endorsements': 32},
                {'name': 'AWS / GCP', 'endorsements': 30},
                {'name': 'Docker / Kubernetes', 'endorsements': 28},
                {'name': 'Scikit-learn / XGBoost', 'endorsements': 26},
                {'name': 'Spark / Hadoop', 'endorsements': 24},
                {'name': 'MLOps / MLflow', 'endorsements': 22},
                {'name': 'Data Visualization (Tableau, Plotly)', 'endorsements': 20}
            ],
            'hobbies': ['Photographie', 'Randonnée', 'Lecture'],
            'generated_date': datetime.now().strftime('%d/%m/%Y')
        }
        
        return self.generate_cv(choix, mock_data, output_path)


def main():
    """Fonction principale avec menu interactif"""
    generator = LinkedInCVGenerator(template_dir=TEMPLATES)
    
    print("\n" + "="*70)
    print(" 🎨 GÉNÉRATEUR DE CV LINKEDIN - FORMAT A4")
    print("="*70)
    print("\n⚠️  NOTE IMPORTANTE:")
    print("L'API LinkedIn officielle n'est plus accessible pour les profils personnels.")
    print("Choisissez l'une des méthodes ci-dessous pour créer votre CV.\n")

    print("💡 CONSEIL:")
    print("   - Pour un CV professionnel, utilisez l'option 1 (saisie interactive)")
    print("   - Pour un CV rapide, utilisez l'option 4 (données de démonstration)")

    print("\nVous avez le choix du template.")
    print("  1. Design épuré et moderne (par défaut)")
    print("  2. Minimal brutaliste, typographie géométrique, noir/blanc/bleu électrique")
    print("  3. Moderne premium, gradients subtils, vert émeraude/gris anthracite")
    print("  4. Layout asymétrique, serif élégant, bordeaux/beige/or")

    type_template = input("\nVotre choix (1-4): ").strip()

    if type_template not in ['1', '2', '3', '4']:
        print("Choix de template invalide, utilisation du template par défaut (1).")
        type_template = '1'
    
    
    print("OPTIONS DISPONIBLES:")
    print("  1. Saisie interactive (Recommandé)")
    print("  2. Importer depuis export LinkedIn")
    print("  3. Charger un json")
    print("  4. Générer avec données de démonstration")
    print("  0. Quitter")
    
    choice = input("\nVotre choix (1-4): ").strip()
    
    if choice == '1':
        # Saisie interactive
        print("\n📝 Vous allez créer votre CV de manière interactive...")
        data = generator.generate_from_manual_input(os.path.join(DATA, "data.json"))
        if data:
            output_file = generator.generate_cv(choice, data, os.path.join(OUTPUTS, f"cv_{type_template}.html"))
            print(f"\n✅ CV généré avec succès: {output_file}")
            print("\n💡 Pour l'exporter en PDF:")
            print("   1. Ouvrez cv.html dans Chrome")
            print("   2. Ctrl+P puis 'Enregistrer en PDF'")
            print("   3. Cochez 'Graphiques d'arrière-plan'")
    
    elif choice == '2':
        # Import depuis export LinkedIn
        print("\n📦 IMPORT DEPUIS EXPORT LINKEDIN")
        print("\nPour obtenir votre archive:")
        print("  1. LinkedIn > Paramètres > Confidentialité des données (lien : https://www.linkedin.com/mypreferences/d/download-my-data)")
        print("  2. 'Obtenir une copie de vos données'")
        print("  3. Téléchargez et extrayez le ZIP")
        print()
        export_path = input("Chemin vers le dossier extrait: ").strip()
        
        if os.path.exists(export_path):
            data = generator.parse_linkedin_export(export_path)
            if data:
                output_file = generator.generate_cv(type_template, data, os.path.join(OUTPUTS, f"cv_{type_template}.html"))
                print(f"\n✅ CV généré avec succès: {output_file}")
        else:
            print(f"❌ Le dossier '{export_path}' n'existe pas.")
    elif choice == '3':
        # loading
        print("\n📦 IMPORT de json en local")
        export_path = input("Chemin vers le dossier extrait: ").strip()
        if os.path.exists(export_path):
            with open(export_path, encoding='utf-8') as json_data:
                output_file = generator.generate_cv(type_template, json.load(json_data), os.path.join(OUTPUTS, f"cv_{type_template}.html"))
        print(f"✅ CV de démo généré: {output_file}")
        print("\n💡 Vous pouvez maintenant:")
        print("   - Ouvrir le CV et le modifier manuellement")
        print("   - Ou relancer avec l'option 1 pour vos vraies données")
    elif choice == '4':
        # Données de démonstration
        print("\n🎯 Génération avec données de démonstration...")
        output_file = generator.generate_from_mock_data(type_template, os.path.join(OUTPUTS, f"cv_{type_template}.html"))
        print(f"✅ CV de démo généré: {output_file}")
        print("\n💡 Vous pouvez maintenant:")
        print("   - Ouvrir le CV et le modifier manuellement")
        print("   - Ou relancer avec l'option 1 pour vos vraies données")
    
    else:
        print("\n👋 Au revoir!")


if __name__ == "__main__":
    main()