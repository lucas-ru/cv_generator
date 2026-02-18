import os
import json
import io
import sys
import pytest
import importlib.util

ROOT = os.path.dirname(os.path.dirname(__file__))
TEMPLATES = os.path.join(ROOT, 'templates')
OUTPUTS = os.path.join(ROOT, 'outputs')

spec = importlib.util.spec_from_file_location('linkedin_cv_generator', os.path.join(ROOT, 'linkedin_cv_generator.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Generator = mod.LinkedInCVGenerator


@pytest.fixture(autouse=True)
def ensure_outputs_dir(tmp_path, monkeypatch):
    # Use a temporary outputs dir for tests
    tmp_outputs = tmp_path / "outputs"
    tmp_outputs.mkdir()
    monkeypatch.setenv('CV_OUTPUTS', str(tmp_outputs))
    return tmp_outputs


def load_template(generator, choice, data, out_path):
    # Helper to generate one CV and assert file created
    path = generator.generate_from_mock_data(choice, out_path) if data is None else generator.generate_cv(choice, data, out_path)
    assert os.path.exists(path)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<html' in content.lower()
    return content


def test_templates_generate_mock(tmp_path):
    gen = Generator(template_dir=TEMPLATES)
    out_dir = tmp_path
    # test templates 1..4
    for choice in ['1', '2', '3', '4']:
        out_file = os.path.join(out_dir, f'mock_cv_{choice}.html')
        path = gen.generate_from_mock_data(choice, out_file)
        assert os.path.exists(path)
        with open(path, encoding='utf-8') as f:
            data = f.read()
        assert '<html' in data.lower()


def test_generate_from_json_load(tmp_path):
    gen = Generator(template_dir=TEMPLATES)
    # create a minimal json data
    sample = {
        'personal_info': {'name': 'Test User', 'headline': 'Engineer', 'location': 'Nowhere'},
        'experiences': [],
        'education': [],
        'skills': [],
        'hobbies': []
    }
    json_path = tmp_path / 'data.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, ensure_ascii=False)

    # load and render
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    out_file = os.path.join(tmp_path, 'cv_from_json.html')
    path = gen.generate_cv('1', data, out_file)
    assert os.path.exists(path)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    assert 'Test User' in html


def test_photo_rendering_in_output(tmp_path):
    gen = Generator(template_dir=TEMPLATES)
    # create a minimal json data and a tiny image file
    sample = {
        'personal_info': {'name': 'Photo User', 'headline': 'With Photo', 'location': 'Here'},
        'experiences': [],
        'education': [],
        'skills': [],
        'hobbies': []
    }
    # create a tiny PNG file
    img_path = tmp_path / 'avatar.png'
    img_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x02\x00\x01E\x1d\x1b\x1b\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    with open(img_path, 'wb') as f:
        f.write(img_bytes)

    # use relative filename so HTML references it from same folder as output
    sample['personal_info']['photo'] = os.path.basename(str(img_path))

    out_file = os.path.join(tmp_path, 'cv_with_photo.html')
    # ensure image and html live in same directory
    path = gen.generate_cv('1', sample, out_file)
    assert os.path.exists(path)
    with open(path, encoding='utf-8') as f:
        html = f.read()
    assert '<img' in html.lower()
    assert sample['personal_info']['photo'] in html


def test_generate_interactive_simulated(monkeypatch, tmp_path):
    gen = Generator(template_dir=TEMPLATES)
    # Prepare simulated stdin responses for interactive input
    inputs = [
        'Jean Dupont',            # name
        'Dev',                    # headline
        'jd@example.com',         # email
        '',                       # phone
        'Paris',                  # location
        'linkedin.com/in/jdupont',# linkedin_url
        'Résumé court',           # summary
        '',                       # photo (optional)
        # experiences: provide one then blank to stop
        'DevOps Engineer',        # exp title
        'ACME',                   # company
        'Paris',                  # location
        'Janvier 2020',           # start_date
        'Présent',                # end_date
        'Faire des choses',       # description
        'n',                      # add another experience
        # education: provide blank to stop
        '',
        # skills
        'Python,Docker',
        # hobbies
        'Randonnée,Musique'
    ]
    monkeypatch.setattr('sys.stdin', io.StringIO('\n'.join(inputs) + '\n'))
    out_file = os.path.join(tmp_path, 'cv_interactive.html')
    data = gen.generate_from_manual_input(str(out_file))
    # ensure hobbies present
    assert 'hobbies' in data
    assert 'Randonnée' in data['hobbies'][0] or 'Randonnée' in ','.join(data['hobbies'])
    # render
    path = gen.generate_cv('1', data, out_file)
    assert os.path.exists(path)
