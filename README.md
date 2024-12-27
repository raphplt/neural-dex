## Installer tesseract
https://github.com/UB-Mannheim/tesseract/wiki

## Installer les dépendances
```bash
pip install -r requirements.txt
```

## Configurer le fichier .env
```bash
cp .env.example .env
```

## Lancer le programme
```bash
uvicorn main:app --reload
```
