# sunupay-api — dépôt de labs DevSecOps Foundation

Application **volontairement vulnérable** utilisée pendant la formation DevSecOps Foundation (WeLearnIT).
Ne jamais la déployer ni réutiliser son code.

## Contenu

| Élément | Rôle |
|---|---|
| `app/app.py` | API Flask avec secrets en dur, injection SQL, injection de commande, etc. |
| `requirements.txt` | Dépendances anciennes et vulnérables |
| `Dockerfile` | Image ancienne, exécution en root |
| `infra/main.tf` | Terraform mal configuré (jamais appliqué) |
| `labs/*.yml` | Workflows GitHub Actions à activer un par un |

## Activer un lab

Copier le fichier du lab depuis `labs/` vers `.github/workflows/` (bouton **Add file > Create new file** de GitHub,
nom `.github/workflows/01-secrets.yml`, coller le contenu, **Commit changes**), puis ouvrir l'onglet **Actions**.

Tous les labs se font dans le navigateur : aucune installation locale.
