# -*- coding: utf-8 -*-
"""Guide des pages (HTML autonome) : rôle de chaque page, pourquoi elle compte, ce qui reste à obtenir du client."""
import html, os

E = lambda s: html.escape(s, quote=True)

PAGES = [
    ('index.html', 'Accueil', 'Convaincre en cinq secondes, puis orienter.', [
        'C’est la première page vue : bouche-à-oreille, carte Google, nom tapé dans Google.',
        'Le visiteur décide ici s’il reste : promesse et téléphone en haut, logos des références juste dessous.',
        'Elle répond dans l’ordre aux questions du visiteur : qui, confiance, métiers, preuves, déroulé, devis.']),
    ('placo.html', 'Placo', 'Capter « faux plafond Genève », « cloison placo ».', [
        'Une page par métier : chaque métier est une recherche Google différente, une page dédiée se classe mieux.',
        'Page d’arrivée des annonces Google : le visiteur trouve exactement ce qu’il a cherché.',
        'Le formulaire arrive pré-coché sur « placo » : une étape de moins.']),
    ('peinture.html', 'Peinture', 'Capter les régies et les fins de bail.', [
        'Volume régulier : remises en état entre deux locataires, cages d’escalier.',
        'Le métier le plus concurrencé : la page doit rassurer sur la propreté et le délai.',
        'Il manque des photos de peinture : c’est la page la plus faible en preuve.']),
    ('isolation-acoustique.html', 'Isolation acoustique', 'Le métier qui vous différencie.', [
        'Peu d’artisans genevois le mettent en avant, alors que vous l’avez fait pour des bâtiments publics.',
        'Deux publics : salles et bureaux (correction de l’écho), particuliers gênés par le bruit.',
        'Recherches très ciblées (« bruit voisin du dessus ») : demandes déjà motivées.']),
    ('cloisons-isothermes.html', 'Cloisons isothermes', 'Prendre une niche presque sans concurrence.', [
        'Isoler une cave, un garage ou des combles : peu de pages en Suisse romande en parlent.',
        'Le nom reste à décider (« isothermes » ou « isolantes ») : il change les recherches captées.',
        'Complète les autres métiers : souvent vendue avec du placo.']),
    ('realisations.html', 'Réalisations', 'Prouver, avec des chantiers nommés.', [
        'Répond à la question n° 1 du client : « vous l’avez déjà fait ? ».',
        'Une photo avec un lieu et un type de travaux vaut plus qu’une promesse.',
        'Chaque chantier nommé ajoute un lieu que Google peut associer à l’entreprise.']),
    ('professionnels.html', 'Professionnels', 'Vendre aux régies, architectes et communes.', [
        'Les clients pros donnent du volume et reviennent.',
        'Ils cherchent des documents : attestations, assurance, normes SIA, lots CFC. Tout est à un clic.',
        'Sert aussi de dossier pour entrer dans les listes de fournisseurs et les appels d’offres.']),
    ('entreprise.html', 'L’entreprise', 'Montrer des personnes, pas un logo.', [
        'Un particulier achète quelqu’un d’honnête qui entre chez lui : visages, histoire depuis 2007, adresse.',
        'Google et les annuaires vérifient que l’entreprise est réelle et cohérente partout.',
        'C’est la page que l’on consulte juste avant d’appeler.']),
    ('contact.html', 'Contact', 'Transformer l’intérêt en demande.', [
        'Formulaire en trois étapes, ou simple demande de rappel : deux portes pour deux niveaux d’urgence.',
        'Chaque demande reçoit une note A, B ou C : les associés rappellent les meilleures en premier.',
        'Téléphone, horaires et zone d’intervention visibles : aucune question sans réponse.']),
    ('merci.html', 'Merci', 'Rassurer après l’envoi, et compter.', [
        'Dit ce qui se passe ensuite et quand : moins d’appels de relance.',
        'C’est le point de mesure des demandes (publicité Google, statistiques).']),
    ('mentions-legales.html', 'Mentions légales', 'Obligation légale et confiance.', [
        'Exigées par la loi suisse (LCD) et par Google Ads.',
        'Raison sociale, IDE, adresse : la même identité que partout ailleurs.']),
    ('confidentialite.html', 'Confidentialité', 'Conformité nLPD.', [
        'Obligatoire dès qu’un formulaire collecte des données.',
        'À faire relire par un juriste avant la mise en ligne.']),
    ('404.html', 'Page introuvable', 'Ne perdre personne.', [
        'Récupère les visiteurs arrivés par un lien cassé ou une ancienne adresse.',
        'Renvoie vers les métiers et le téléphone.']),
]


def generer(out, resume):
    cartes = []
    for f, nom, role, pourquoi in PAGES:
        qs = []
        for p in resume.get(f, []):
            if p['question'] not in qs:
                qs.append(p['question'])
        n = len(resume.get(f, []))
        afaire = ('<div class="todo"><h4>À obtenir du client <span>%d passage%s en lorem ipsum</span></h4><ul>%s</ul></div>'
                  % (n, 's' if n > 1 else '', ''.join('<li>%s</li>' % E(q) for q in qs))) if qs else \
                 '<div class="todo ok"><h4>Complète</h4></div>'
        cartes.append('''<article id="%s"><header><h3>%s</h3><a href="site/%s">%s</a></header>
<p class="role">%s</p><ul class="why">%s</ul>%s</article>''' % (
            f[:-5], E(nom), f, f, E(role), ''.join('<li>%s</li>' % E(x) for x in pourquoi), afaire))
    nav = ''.join('<a href="#%s">%s</a>' % (f[:-5], E(n)) for f, n, _, _ in PAGES)
    total = sum(len(v) for v in resume.values())
    doc = TPL.replace('{{NAV}}', nav).replace('{{CARTES}}', '\n'.join(cartes)).replace('{{TOTAL}}', str(total))
    open(os.path.join(out, 'GUIDE-DES-PAGES.html'), 'w', encoding='utf-8').write(doc)


TPL = '''<!DOCTYPE html>
<html lang="fr-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Andy Construct · Guide des pages</title>
<style>
:root{--bg:#F4F5F6;--card:#fff;--ink:#1D1F22;--muted:#5F656C;--line:#DDE1E4;--red:#E8000F;--soft:#FDECEC;--ok:#13995A}
@media (prefers-color-scheme:dark){:root{--bg:#141517;--card:#1D1F22;--ink:#EEF0F1;--muted:#A3A9B0;--line:#33373C;--red:#FF3B47;--soft:#3A1A1C;--ok:#3CC985}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.top{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--line);padding:14px max(16px,4vw)}
h1{font-size:20px;margin:0 0 4px;letter-spacing:-.01em}
h1 b{color:var(--red)}
.sub{color:var(--muted);font-size:13px;margin:0 0 10px}
nav{display:flex;flex-wrap:wrap;gap:6px}
nav a{font-size:12.5px;color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:3px 10px}
nav a:hover{border-color:var(--red)}
main{padding:20px max(16px,4vw) 60px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;align-items:start}
.intro{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:10px 28px;color:var(--muted);font-size:13.5px}
.intro b{color:var(--ink)}
code{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-size:12.5px}
article{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;scroll-margin-top:110px}
article header{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
h3{margin:0;font-size:19px;letter-spacing:-.01em}
article header a{font-size:12px;color:var(--muted)}
.role{margin:6px 0 10px;font-weight:600;color:var(--red)}
.why{margin:0;padding-left:18px}
.why li{margin:0 0 5px}
.todo{margin-top:14px;border-top:1px dashed var(--line);padding-top:10px}
.todo h4{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);display:flex;justify-content:space-between;gap:8px}
.todo h4 span{text-transform:none;letter-spacing:0;font-weight:500}
.todo ul{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:5px}
.todo li{font-size:12.5px;background:var(--soft);border-radius:6px;padding:2px 8px}
.todo.ok h4{color:var(--ok)}
</style></head><body>
<div class="top"><h1>Andy Construct · <b>pourquoi chaque page compte</b></h1>
<p class="sub">Une carte par page : son rôle, pourquoi elle compte, ce qu’il manque. {{TOTAL}} passages sont en lorem ipsum en attendant les informations du client.</p>
<nav>{{NAV}}</nav></div>
<main>
<div class="intro"><span><b>Voir le site :</b> ouvrir <code>site/index.html</code></span>
<span><b>Tester les formulaires :</b> dans <code>site/</code>, lancer <code>php -S localhost:8000</code> puis ouvrir <code>http://localhost:8000</code></span>
<span><b>Lorem ipsum</b> = une information à obtenir du client (liste par page ci-dessous, détail dans <code>a-remplir.json</code>)</span></div>
{{CARTES}}
</main></body></html>
'''
