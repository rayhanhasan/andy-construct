# -*- coding: utf-8 -*-
"""Fichiers techniques : sitemap.xml, robots.txt, llms.txt (copy deck §P), .htaccess (redirections 301, compression,
cache, en-têtes de sécurité). Le .htaccess de site/api/ n'est pas touché : il garde ses propres règles."""
import base64, hashlib, os
import ctx
from ctx import V, definitif, PROD
from common import AUJOURDHUI, PAGES_ECRITES, EARLY_JS, doc, mail


def ecrire(nom, texte):
    with open(os.path.join(ctx.OUT, nom), 'w', encoding='utf-8') as f:
        f.write(texte)
    print('  %-26s %6d octets' % (nom, len(texte.encode('utf-8'))))


def sitemap():
    urls = ''
    for fichier, indexable in PAGES_ECRITES:
        if not indexable:
            continue
        loc = PROD + ('' if fichier == 'index.html' else fichier)
        urls += '  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (loc, AUJOURDHUI.isoformat())
    ecrire('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)


def robots():
    if ctx.prod():
        txt = 'User-agent: *\nDisallow: /api/\nDisallow: /interne/\n\nSitemap: %ssitemap.xml\n' % PROD
    else:
        # Exploration permise : un robot bloqué ne lit pas le noindex (balise et en-tête X-Robots-Tag du .htaccess)
        # et peut indexer l'adresse nue. Le noindex suffit à tenir la version de validation hors des résultats.
        txt = ('# Version de validation (%s) : non indexée (balise robots noindex et en-tête X-Robots-Tag).\n'
               '# Exploration laissée ouverte pour que le noindex soit lu.\nUser-agent: *\nDisallow:\n' % ctx.MODE)
    ecrire('robots.txt', txt)


def llms():
    omc = V('C22', 'OMC ; ', '')
    hotel = V('C22', 'Everness Hotel & Resort, Chavannes-de-Bogis', 'hôtel à Chavannes-de-Bogis')
    methode = V('C06 C07', 'visite sur place, offre écrite détaillée poste par poste en CHF, chantier protégé et nettoyé, réception des finitions avec le client.',
                'visite sur place, offre écrite, chantier protégé, réception des finitions avec le client.')
    ne_fait_pas = V('C16', 'façades, carrelage, chambres froides', 'façades, carrelage')
    isol = V('C16', 'les cloisons isolantes, aussi appelées cloisons isothermes', 'les cloisons isothermes')
    lignes_docs = []
    for cle, titre in (('references', 'Dossier de références (PDF)'), ('guide-bruit', 'Guide : réduire le bruit chez soi (PDF)'),
                       ('checklist', 'Liste de contrôle : travaux en immeuble habité (PDF)')):
        d = doc(cle)
        if d:
            lignes_docs.append('- [%s](%s%s)' % (titre, PROD, d[0]))
    docs = ('\n## Documents\n\n%s\n' % '\n'.join(lignes_docs)) if lignes_docs else ''
    heures = V('C03', '- Horaires : du lundi au vendredi, 7 h – 18 h\n', '')
    txt = '''# Andy Construct

> Andy Construct est une entreprise de plâtrerie, de peinture et d'isolation intérieure basée à Carouge (Genève), active depuis 2007. Elle pose des cloisons, des doublages et des faux-plafonds en plaques de plâtre (placo), réalise la peinture intérieure, l'isolation acoustique (isolation phonique et correction de l'écho) et %(isol)s (isolation entre pièces chauffées et caves, garages ou combles). Elle travaille pour des particuliers, des régies et gérances, des architectes, des communes, des institutions et des entreprises, dans toute la Suisse romande.

Informations clés :

- Nom commercial : Andy Construct
- Raison sociale : Andy Construct, Chanton & Cie, société en nom collectif
- IDE : CHE-113.706.162 (registre du commerce du canton de Genève)
- Activité depuis le 1er juin 2007 (Perly-Certoux, puis Chêne-Bourg dès 2010, Carouge dès 2023)
- Adresse : Route des Acacias 48, 1227 Carouge (Genève), Suisse
- Téléphone : +41 22 771 20 15 ; %(mob)s : +41 78 631 14 34
- E-mail : %(mail)s
%(heures)s- Zone : cantons de Genève, Vaud, Neuchâtel, Fribourg et Jura, Valais romand, Jura bernois
- Langue : français
- Ce que l'entreprise ne fait pas : %(ne_fait_pas)s

Prestations (4) :

- Placo : cloisons, doublages, faux-plafonds, caissons en plaques de plâtre
- Peinture intérieure : logements, fins de bail, cages d'escalier, bureaux
- Isolation acoustique : doublages et faux-plafonds acoustiques, cloisons acoustiques, correction acoustique des salles
- %(nom_isol)s : cloisons et doublages isolants, isolation de plafonds de caves et de garages

Méthode : %(methode)s

Maîtres d'ouvrage qui ont confié des travaux à l'entreprise (liste publiée par l'entreprise) : Ville de Genève ; Mairie de Plan-les-Ouates ; salle communale de Collonge-Bellerive ; %(omc)sConservatoire de musique de Genève ; HEAD – Genève ; Salle de l'Alhambra ; Harmonie Nautique de Genève ; Piaget ; UBS ; J. Safra Sarasin (anciennement Bank Sarasin) ; de Grisogono ; Celgene ; Labcorp (anciennement Covance), Meyrin ; Dipan, Nyon ; Energestion, Les Acacias ; %(hotel)s ; Domaine des Perrières, Coppet.

## Pages principales

- [Accueil](%(p)s): présentation, prestations, méthode, questions fréquentes
- [Placo](%(p)splaco.html): cloisons, doublages, faux-plafonds et caissons en plaques de plâtre ; prix et délais ; accord de la régie ou de la PPE
- [Peinture](%(p)speinture.html): peinture intérieure des logements, fins de bail, cages d'escalier et bureaux
- [Isolation acoustique](%(p)sisolation-acoustique.html): bruit des voisins, différence entre isoler et corriger, doublage et faux-plafond acoustiques, correction de l'écho
- [%(nom_isol)s](%(p)scloisons-isothermes.html): cloisons isothermes, isolation de caves, garages et combles, subventions
- [Réalisations](%(p)srealisations.html): projets photographiés, avant / après
- [Professionnels](%(p)sprofessionnels.html): régies, architectes, communes ; méthode en immeuble habité ; lots CFC ; documents ; liste complète des références
- [L'entreprise](%(p)sentreprise.html): histoire depuis 2007, méthode, engagements, identité vérifiable
- [Contact](%(p)scontact.html): téléphones, horaires, adresse, formulaire de demande de devis, zone d'intervention
%(docs)s
## Optional

- [Mentions légales](%(p)smentions-legales.html)
- [Protection des données](%(p)sconfidentialite.html)
''' % dict(isol=isol, mob=V('C30', 'sur les chantiers', 'mobile'), mail=mail(), heures=heures, ne_fait_pas=ne_fait_pas,
           nom_isol=V('C16', 'Cloisons isolantes (isothermes)', 'Cloisons isothermes'), methode=methode, omc=omc, hotel=hotel,
           p=PROD, docs=docs)
    ecrire('llms.txt', txt)


def csp_hash():
    return "'sha256-%s'" % base64.b64encode(hashlib.sha256(EARLY_JS.encode('utf-8')).digest()).decode()


# Anciennes adresses (site Joomla, architecture §1.4) : avec ou sans « index.php/ »
REDIRECTIONS = [
    (r'presentation', 'entreprise.html'),
    (r'produits/plafonds/plafonds-en-(placoplatre|tissu-tendu-a-froid|fibre-de-bois|fibre-minerale|bac-metallique)', 'placo.html#faux-plafonds'),
    (r'produits/plafonds/plafonds-phoniques-et-acoustiques', 'isolation-acoustique.html'),
    (r'produits/cadres-acoustiques', 'isolation-acoustique.html#correction'),
    (r'produits/cloisons/cloisons-(legeres-en-placoplatre|mobiles-en-aluminium)', 'placo.html#cloisons'),
    (r'produits/cloisons/isolation-thermique-ou-phonique', 'cloisons-isothermes.html'),
    (r'realisations/photos-travaux-2014-2016', 'realisations.html'),
    (r'realisations/photos-travaux-avant-apres', 'realisations.html#avant-apres'),
    (r'realisations/references', 'professionnels.html#references'),
    (r'contact', 'contact.html'),
]


def htaccess():
    base = 'https://www.andyconstruct.ch/' if ctx.prod() else '/'
    regles = ''.join('RewriteRule ^(index\\.php/)?%s/?$ %s%s [R=301,L,NE]\n' % (motif, base, cible) for motif, cible in REDIRECTIONS)
    umami = ctx.CONFIG.get('umami_src', '') if ctx.CONFIG.get('umami_id') else ''
    origine_umami = ''
    if umami:
        from urllib.parse import urlsplit
        u = urlsplit(umami)
        origine_umami = ' %s://%s' % (u.scheme, u.netloc)
    csp = ("default-src 'self'; script-src 'self' %s%s; style-src 'self'; img-src 'self' data:; font-src 'self'; "
           "connect-src 'self'%s; form-action 'self'; frame-ancestors 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests"
           % (csp_hash(), origine_umami, origine_umami))
    hote = ('''# 2) Accueil : une seule adresse « / » (le lien direct vers /index.html est redirigé ; DirectoryIndex n'est pas concerné)
RewriteCond %{THE_REQUEST} \\s/index\\.html[\\s?]
RewriteRule ^index\\.html$ https://www.andyconstruct.ch/ [R=301,L]

# 3) Une seule adresse : https://www.andyconstruct.ch (en une seule redirection)
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\\.andyconstruct\\.ch$ [NC]
RewriteRule ^(.*)$ https://www.andyconstruct.ch/$1 [R=301,L]
''' if ctx.prod() else '''# 2) Adresse unique https://www.andyconstruct.ch : active seulement en production
# RewriteCond %{HTTPS} off [OR]
# RewriteCond %{HTTP_HOST} !^www\\.andyconstruct\\.ch$ [NC]
# RewriteRule ^(.*)$ https://www.andyconstruct.ch/$1 [R=301,L]
''')
    txt = '''# Andy Construct : configuration Apache / LiteSpeed (généré par tools/build, mode %(mode)s)
# Le dossier api/ garde son propre .htaccess (accès, en-têtes) : ses règles de réécriture remplacent celles-ci.

Options -Indexes
AddDefaultCharset utf-8
DirectoryIndex index.html
ErrorDocument 404 /404.html

<IfModule mod_mime.c>
  AddType image/webp .webp
  AddType image/svg+xml .svg
  AddType font/woff2 .woff2
  AddType application/manifest+json .webmanifest
  AddType text/plain .txt
  AddCharset utf-8 .html .css .js .txt .xml .json .webmanifest
</IfModule>

<IfModule mod_rewrite.c>
RewriteEngine On

# 1) Anciennes adresses (site Joomla et maquette) : 301 en une seule étape
RewriteRule ^index\\.php/?$ %(base)s [R=301,L]
%(regles)sRewriteRule ^prestations\\.html$ %(base)s [R=301,L]

%(hote)s</IfModule>

# Compression : Brotli si le module existe, sinon Deflate
<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/css text/plain text/xml application/javascript application/json application/xml application/ld+json application/manifest+json image/svg+xml
</IfModule>
<IfModule !mod_brotli.c>
  <IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/javascript application/json application/xml application/ld+json application/manifest+json image/svg+xml
  </IfModule>
</IfModule>

# Cache : CSS et JS sont versionnés (?v=empreinte) ; polices stables ; images 30 jours ; HTML toujours revalidé
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresDefault "access plus 1 hour"
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType application/javascript "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType image/webp "access plus 30 days"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/svg+xml "access plus 30 days"
  ExpiresByType image/x-icon "access plus 30 days"
  ExpiresByType application/pdf "access plus 7 days"
</IfModule>
<IfModule mod_headers.c>
  <FilesMatch "\\.(css|js|woff2)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\\.(html|xml|txt)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>

  # En-têtes de sécurité
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
  Header always set X-Frame-Options "SAMEORIGIN"
  # CSP stricte : aucun script ni style en ligne, sauf le script d'amorçage (empreinte ci-dessous).
  # Umami : renseigner umami_src et umami_id dans tools/build/donnees/config.json, puis regénérer.
  <If "%%{REQUEST_URI} !~ m#^/api/#">
    Header always set Content-Security-Policy "%(csp)s"
  </If>
  # HSTS : à activer en production une fois HTTPS vérifié sur www et sans www (puis ne plus revenir en arrière).
  # Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
%(xrobots)s</IfModule>

# Fichiers sensibles ou inutiles en ligne
<FilesMatch "(^\\.|\\.(md|py|json\\.bak|log|sh)$)">
  <IfModule mod_authz_core.c>
    Require all denied
  </IfModule>
</FilesMatch>
''' % dict(mode=ctx.MODE, base=base, regles=regles, hote=hote, csp=csp,
           xrobots='' if ctx.prod() else ('  # Version de validation : jamais indexée, y compris les PDF, les images et les fichiers texte\n'
                                         '  Header always set X-Robots-Tag "noindex, nofollow"\n'))
    ecrire('.htaccess', txt)


def build():
    sitemap()
    robots()
    llms()
    htaccess()
