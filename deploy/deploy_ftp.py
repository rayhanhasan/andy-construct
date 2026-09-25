#!/usr/bin/env python3
"""Deploie le dossier site/ dans harbor-digital.fr/res/<sous-dossier> par FTP.

Garde-fous :
- les identifiants sont lus dans les variables d'environnement, jamais dans le code ;
- toute ecriture est refusee hors du dossier distant « res » ;
- le script n'efface rien (envoi et remplacement de fichiers uniquement).

Usage :
    export FTP_HOST=46.202.172.2 FTP_USER='...' FTP_PASS='...'
    python3 deploy/deploy_ftp.py --dry-run      # liste ce qui serait envoye
    python3 deploy/deploy_ftp.py                # envoie dans res/andy-construct/
    python3 deploy/deploy_ftp.py --subdir ""    # envoie directement dans res/ (remplace les fichiers de meme nom)
"""
import argparse
import ftplib
import os
import posixpath
import sys
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent / "site"
RES_CANDIDATES = ["/res", "/public_html/res", "/domains/harbor-digital.fr/public_html/res"]


def connect():
    host = os.environ.get("FTP_HOST")
    user = os.environ.get("FTP_USER")
    password = os.environ.get("FTP_PASS")
    port = int(os.environ.get("FTP_PORT", "21"))
    if not (host and user and password):
        sys.exit("Variables FTP_HOST, FTP_USER et FTP_PASS requises.")
    try:
        ftp = ftplib.FTP_TLS()
        ftp.connect(host, port, timeout=30)
        ftp.login(user, password)
        ftp.prot_p()
        print("Connexion FTPS (chiffree) etablie.")
    except ftplib.all_errors as exc:
        print(f"FTPS indisponible ({exc}), repli sur FTP simple.")
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=30)
        ftp.login(user, password)
    ftp.set_pasv(True)
    return ftp


def find_res_dir(ftp):
    forced = os.environ.get("FTP_REMOTE_RES")
    for candidate in [forced] if forced else RES_CANDIDATES:
        try:
            ftp.cwd(candidate)
            return ftp.pwd()
        except ftplib.error_perm:
            continue
    sys.exit("Dossier distant « res » introuvable. Indiquez-le avec FTP_REMOTE_RES.")


def inside(path, root):
    path, root = posixpath.normpath(path), posixpath.normpath(root)
    return path == root or path.startswith(root + "/")


def ensure_dir(ftp, path, res_root, dry_run):
    if not inside(path, res_root):
        sys.exit(f"Refuse : {path} est hors de {res_root}")
    try:
        ftp.cwd(path)
    except ftplib.error_perm:
        ensure_dir(ftp, posixpath.dirname(path), res_root, dry_run)
        print(f"  mkdir {path}")
        if not dry_run:
            ftp.mkd(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdir", default="andy-construct", help="sous-dossier de res/ (defaut : andy-construct)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if ".." in Path(args.subdir).parts or args.subdir.startswith("/"):
        sys.exit("Sous-dossier invalide.")

    ftp = connect()
    res_root = find_res_dir(ftp)
    target = posixpath.normpath(posixpath.join(res_root, args.subdir)) if args.subdir else res_root
    if not inside(target, res_root):
        sys.exit(f"Refuse : {target} est hors de {res_root}")
    print(f"Dossier res : {res_root}\nCible       : {target}\n")

    files = sorted(p for p in SITE_DIR.rglob("*") if p.is_file() and p.name != ".DS_Store")
    for local in files:
        rel = local.relative_to(SITE_DIR).as_posix()
        remote = posixpath.join(target, rel)
        ensure_dir(ftp, posixpath.dirname(remote), res_root, args.dry_run)
        print(f"  put {rel}")
        if not args.dry_run:
            with open(local, "rb") as fh:
                ftp.storbinary(f"STOR {remote}", fh)

    ftp.quit()
    print(f"\n{len(files)} fichiers {'a envoyer' if args.dry_run else 'envoyes'}.")


if __name__ == "__main__":
    main()
