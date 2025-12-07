# Application de Téléchargement Musical

Une application Streamlit légère pour télécharger l'audio des playlists YouTube.

## Fonctionnalités

- Téléchargement de toutes les pistes audio d'une playlist YouTube publique
- Organisation automatique des dossiers (`downloads/[nom-playlist]/`)
- Format de sortie MP3 (192kbps)
- Suivi de progression simple par piste
- Gestion des erreurs (ignore les pistes échouées et continue)
- Sanitisation automatique des noms de fichiers
- Téléchargement individuel de chaque piste
- Téléchargement groupé en fichier ZIP
- Interface entièrement en français

## Prérequis

- Python 3.8+
- ffmpeg (requis pour la conversion audio en MP3)

### Installation de ffmpeg

- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg` (ou le gestionnaire de paquets de votre distribution)
- **Windows**: Télécharger depuis [ffmpeg.org](https://ffmpeg.org/download.html)

## Installation

1. Cloner le dépôt
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. S'assurer que ffmpeg est installé sur votre système

## Utilisation

Lancer l'application Streamlit :
```bash
streamlit run app.py
```

Ensuite :
1. Entrer une URL de playlist YouTube
2. Cliquer sur "Télécharger la playlist" et attendre la fin du téléchargement
3. Les fichiers seront enregistrés dans le dossier `downloads/[nom-playlist]/`
4. Télécharger les fichiers individuellement ou en un seul fichier ZIP

## Déploiement sur Streamlit Cloud

Cette application est prête pour le déploiement sur Streamlit Community Cloud (niveau gratuit). Le fichier `packages.txt` assure l'installation automatique de ffmpeg lors du déploiement.

1. Pousser le code sur GitHub
2. Connecter votre dépôt à [Streamlit Cloud](https://streamlit.io/cloud)
3. L'application installera automatiquement :
   - Les dépendances Python depuis `requirements.txt`
   - Les dépendances système (ffmpeg) depuis `packages.txt`
   - Déploiera votre application

### Fonctionnement sur Streamlit Cloud

✅ **Fonctionne sur le niveau gratuit :**
- Installation de ffmpeg via `packages.txt` ✅
- Téléchargement et conversion de l'audio YouTube ✅
- Téléchargement de fichiers via les boutons Streamlit ✅

⚠️ **Limitations :**
- **Stockage éphémère** : Les fichiers sont stockés temporairement sur le serveur. Ils seront perdus lorsque :
  - L'application redémarre (après inactivité)
  - L'application est redéployée
  - Le serveur est recyclé
- **Limites de ressources** : Le niveau gratuit a des limites CPU/mémoire. Les très grandes playlists peuvent expirer ou être lentes
- **Accès aux fichiers** : Les utilisateurs doivent télécharger les fichiers immédiatement après la conversion (des boutons de téléchargement sont fournis)

**Astuce :** Pour un stockage persistant, envisagez d'intégrer des services de stockage cloud (S3, Google Drive, etc.) ou utilisez l'application localement pour un stockage permanent des fichiers.

## License

MIT

