# -*- coding: utf-8 -*-
"""Composants partagés (architecture §3) : références, méthode, FAQ, formulaire en 3 étapes, rappel,
bloc de demande, bande d'appel, cartes projets, avant / après, témoignages."""
import json, os, re, struct
import ctx
from ctx import e, T, V, definitif, marque, insec, M
from common import (TEL, TEL_URI, MOB, MOB_URI, tel_link, horaires, mob_label, mail, svc_nom, svc_url, SERVICES,
                    devis_btn, ICON_PHONE)
from icons import ICONS, INFO

# ---------------------------------------------------------------- références et logos
LOGOS_DIR = os.path.join(ctx.SITE, 'assets/img/references')
LOGOS = {l['id']: l for l in json.load(open(os.path.join(LOGOS_DIR, 'logos.json'), encoding='utf-8'))}
TEXTE_SEUL = {'de-grisogono'}   # logos-references.md §4.4 : nom en texte seulement


def _dims(fichier):
    chemin = os.path.join(LOGOS_DIR, fichier)
    if fichier.endswith('.png'):
        with open(chemin, 'rb') as f:
            w, h = struct.unpack('>II', f.read(24)[16:24])
        return w, h
    vb = re.search(r'viewBox="([\d.\s-]+)"', open(chemin, encoding='utf-8').read()).group(1).split()
    w, h = float(vb[2]), float(vb[3])
    return round(w * 100 / h), 100


def echelle_cls(v):
    return 'e%03d' % round(v * 100)


def echelles():
    """Classes CSS des échelles optiques (pas d'attribut style : CSP stricte)."""
    vals = sorted({l['echelle'] for l in LOGOS.values()})
    return ''.join('.%s{--e:%s}' % (echelle_cls(v), ('%g' % v)) for v in vals)


def logo_affiche(rid):
    l = LOGOS[rid]
    if rid in TEXTE_SEUL or not l.get('fichier'):
        return False
    if l['statut'] == 'autorise':
        return True
    return l['statut'] == 'a_autoriser' and not ctx.prod()


def ref_item(rid, blanc=False, nom=None):
    """Logo (si autorisé dans ce mode) ou nom typographique."""
    l = LOGOS[rid]
    nom = nom or l['nom_affiche']
    if logo_affiche(rid):
        f = l['fichier_blanc'] if blanc else l['fichier']
        w, h = _dims(f)
        return ('<li class="ref ref--logo %s"><img src="assets/img/references/%s" width="%d" height="%d" alt="%s" loading="lazy"></li>'
                % (echelle_cls(l['echelle']), f, w, h, e(nom)))
    return '<li class="ref ref--nom">%s</li>' % insec(e(nom))


BANDEAU = ['ville-de-geneve', 'conservatoire-musique-geneve', 'head-geneve', 'omc', 'ubs', 'piaget', 'plan-les-ouates', 'collonge-bellerive']


def _liste_bandeau(blanc=False):
    items = []
    for rid in BANDEAU:
        if rid == 'omc' and not definitif('C22'):
            items.append(ref_item('alhambra', blanc))      # décision D4
        else:
            items.append(ref_item(rid, blanc))
    return ''.join(items)


def refs_bandeau(p):
    """Bandeau sous le héro (accueil) : 8 références, phrase « particuliers », lien."""
    particuliers = T('C04', 'Et des particuliers, pour une cloison, un plafond ou une pièce à repeindre.',
                     'Et des particuliers, à Genève et dans toute la région.')
    accords = ('<p class="refs-band__accord">Références citées avec l\'accord des maîtres d\'ouvrage.</p>'
               if ctx.prod() and ctx.confirme('C22') else '')
    return '''    <section class="refs-band" aria-labelledby="refs-titre">
      <div class="container">
        <h2 id="refs-titre" class="refs-band__title">Ils nous ont confié des travaux</h2>
        %s
        <div class="refs-band__foot"><p>%s</p><a class="link-arrow" href="professionnels.html#references">Voir toutes nos références</a></div>%s
      </div>
    </section>
''' % (marque('C22', '<ul class="refs refs--band">%s</ul>' % _liste_bandeau(), bloc=True), particuliers, accords)


def refs_ligne(cls=''):
    """Ligne courte (près des formulaires, contact) : texte du copy deck §A.6."""
    return ('<p class="refs-line%s"><b>Ils nous ont confié des travaux :</b> Ville de Genève · Conservatoire de musique de Genève · '
            'HEAD – Genève · Mairie de <span class="nowrap">Plan-les-Ouates</span> · Salle communale de <span class="nowrap">Collonge-Bellerive</span> · '
            'et des particuliers de toute la région.</p>' % ((' ' + cls) if cls else ''))


def refs_pied():
    return ('<p class="footer-refs__title">Ils nous ont confié des travaux</p>'
            '<ul class="refs refs--pied">%s<li class="ref ref--nom">et des particuliers de toute la région</li></ul>' % _liste_bandeau(blanc=True))


def refs_service(ids):
    """« Réalisé notamment pour » : petite rangée de logos ou de noms."""
    return '<ul class="refs refs--svc">%s</ul>' % ''.join(ref_item(r) for r in ids)


SECTEURS = [
    ('Collectivités et institutions', ['ville-de-geneve', 'plan-les-ouates', 'collonge-bellerive', 'omc']),
    ('Culture et formation', ['conservatoire-musique-geneve', 'head-geneve', 'alhambra', 'harmonie-nautique']),
    ('Entreprises', ['piaget', 'ubs', 'j-safra-sarasin', 'de-grisogono', 'celgene', 'labcorp', 'dipan', 'energestion']),
    ('Hôtellerie et domaines', ['everness', 'domaine-des-perrieres']),
]
NOMS_GRILLE = {'j-safra-sarasin': 'J. Safra Sarasin (anciennement Bank Sarasin)', 'labcorp': 'Labcorp (anciennement Covance), Meyrin',
               'dipan': 'Dipan, Nyon', 'energestion': 'Energestion, ingénieurs-conseils, Les Acacias',
               'everness': 'Everness Hotel & Resort, Chavannes-de-Bogis', 'domaine-des-perrieres': 'Domaine des Perrières, Coppet'}


def refs_grille():
    """Grille complète des 18 références par secteur (professionnels.html#references)."""
    cols = ''
    for titre, ids in SECTEURS:
        items = ''
        for rid in ids:
            if rid == 'omc':
                if definitif('C22'):
                    items += marque('C22', ref_item(rid)) if ctx.MODE == 'verification' else ref_item(rid)
                continue
            if rid == 'everness' and not definitif('C22'):
                items += ref_item(rid, nom='Hôtel à Chavannes-de-Bogis')
                continue
            nom = NOMS_GRILLE.get(rid)
            if logo_affiche(rid):
                items += ref_item(rid).replace('</li>', '<span class="ref__legende">%s</span></li>' % insec(e(nom or LOGOS[rid]['nom_affiche'])))
            else:
                items += ref_item(rid, nom=nom)
        cols += '<div class="refs-grid__col"><h3>%s</h3><ul class="refs refs--grid">%s</ul></div>' % (titre, items)
    return '<div class="refs-grid">%s</div>' % cols


# ---------------------------------------------------------------- méthode en 4 étapes (texte unique)
def methode(complete=True, titre_id='methode-titre', h2=None, lien=True, surtitre=True):
    if complete:
        etapes = [
            ('Visite', 'Nous venons voir les lieux, prenons les mesures et écoutons votre besoin.'),
            ('Offre écrite', T('C06', 'Détaillée poste par poste, en CHF, avec la durée des travaux et ce qui n\'est pas compris.',
                               'Nous vous remettons une offre écrite.')),
            ('Chantier protégé', T('C07', 'Sols, meubles et passages protégés. Nettoyage chaque soir, et à fond le dernier jour.',
                                   'Les lieux sont protégés pendant les travaux.')),
            ('Réception', T('C32', 'Nous faisons le tour des finitions avec vous. Une retouche ? Nous revenons.',
                            'Nous contrôlons les finitions avec vous.')),
        ]
        lis = ''.join('<li><h3>%s</h3><p>%s</p></li>' % (t, d) for t, d in etapes)
        eng = T('C06', 'Aucun travail supplémentaire sans votre accord écrit et chiffré.', '')
        eng = ('<p class="engagement">%s</p>' % eng) if eng else ''
        return '<ol class="steps">%s</ol>%s' % (lis, eng)
    etapes = ['Visite : mesures et conseils sur place.',
              T('C06', 'Offre écrite : poste par poste, en CHF.', 'Offre écrite.'),
              T('C07', 'Chantier protégé, nettoyé chaque soir.', 'Chantier protégé.'),
              'Réception : le tour des finitions, ensemble.']
    return '<ol class="steps steps--short">%s</ol>' % ''.join('<li><p>%s</p></li>' % x for x in etapes)


def section_methode_courte(cls='section'):
    return '''    <section class="%s" aria-labelledby="chantier-titre">
      <div class="container">
        <h2 id="chantier-titre">Comment se passe un chantier</h2>
        %s
        <p class="section-foot"><a class="link-arrow" href="entreprise.html#methode">Notre méthode en détail</a></p>
      </div>
    </section>
''' % (cls, methode(False))


# ---------------------------------------------------------------- FAQ
def faq_items(questions):
    """questions : liste de (question, réponse_html, réponse_texte). Renvoie (html, entités JSON-LD)."""
    html = ''.join('<details><summary>%s</summary><div><p>%s</p></div></details>' % (q, a) for q, a, _ in questions)
    ld = [{'@type': 'Question', 'name': ctx.fr(q), 'acceptedAnswer': {'@type': 'Answer', 'text': ctx.fr(t)}} for q, _, t in questions]
    return html, ld


def faq_ld(url, ld):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': url + '#faq', 'inLanguage': 'fr-CH', 'mainEntity': ld}


def Q(codes, question, definitive, repli=None):
    """Question de FAQ soumise à confirmation. repli None : question masquée en production."""
    if codes is None:
        return (question, definitive, re.sub(r'<[^>]+>', '', definitive))
    if definitif(codes):
        return (question, marque(codes, definitive), re.sub(r'<[^>]+>', '', definitive))
    if repli is None:
        return None
    return (question, repli, re.sub(r'<[^>]+>', '', repli))


# ---------------------------------------------------------------- photos (manifeste du portfolio)
MANIFEST = {m['id']: m for m in json.load(open(os.path.join(ctx.SITE, 'assets/img/portfolio/manifest.json'), encoding='utf-8'))}
AA = {m['id']: m for m in json.load(open(os.path.join(ctx.SITE, 'assets/img/avant-apres/manifest.json'), encoding='utf-8'))}


def pic(pid, sizes, alt, eager=False, cls=''):
    it = MANIFEST[pid]
    if it.get('recadre'):
        r = it['recadre']
        b, w, h = r['base'], r['largeur_1200'], r['hauteur_1200']
        srcset = '%s-400.webp 400w, %s-800.webp 800w, %s-1200.webp 1200w' % (b, b, b)
    else:
        b, w, h = it['base'], it['largeur_1600'], it['hauteur_1600']
        srcset = '%s-400.webp %dw, %s-800.webp %dw, %s-1600.webp %dw' % (b, it['largeur_400'], b, it['largeur_800'], b, it['largeur_1600'])
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return ('<picture%s><source type="image/webp" srcset="%s" sizes="%s"><img src="%s-800.jpg" width="%d" height="%d" alt="%s" %s decoding="async"></picture>'
            % ((' class="%s"' % cls) if cls else '', srcset, sizes, b, w, h, e(alt), load))


def pic_data(pid):
    """Attributs de la visionneuse (grande image) pour une photo."""
    it = MANIFEST[pid]
    if it.get('recadre'):
        r = it['recadre']
        return r['base'] + '-1200.webp', r['base'] + '-800.jpg', r['largeur_1200'], r['hauteur_1200']
    return it['base'] + '-1600.webp', it['base'] + '-800.jpg', it['largeur_1600'], it['hauteur_1600']


def aa_pic(paire, etat, sizes, alt):
    m = AA[paire][etat]
    b = m['base']
    srcset = ', '.join('%s-%d.webp %dw' % (b, w, w) for w in m['largeurs'])
    return ('<picture><source type="image/webp" srcset="%s" sizes="%s"><img src="%s-%d.jpg" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"></picture>'
            % (srcset, sizes, b, m['largeurs'][-1], m['largeur'], m['hauteur'], e(alt)))


# ---------------------------------------------------------------- formulaire de demande en 3 étapes (architecture §6)
TRAVAUX = [('placo', 'Placo', 'Cloisons, doublages, faux-plafonds'),
           ('peinture', 'Peinture', 'Murs et plafonds, à l\'intérieur'),
           ('isolation-acoustique', 'Isolation acoustique', 'Contre le bruit ou l\'écho'),
           ('cloisons-isothermes', None, 'Caves, garages, combles'),
           ('ne-sait-pas', 'Autre chose, ou je ne sais pas encore', 'Décrivez-le à l\'étape 3')]
TYPE_CLIENT = [('proprietaire', 'Propriétaire (maison, appartement, PPE)'), ('locataire', 'Locataire'),
               ('regie', 'Régie, gérance ou coopérative'), ('architecte', 'Architecte, bureau d\'études ou entreprise générale'),
               ('commune', 'Commune ou institution'), ('entreprise', 'Entreprise, bureau ou commerce')]
DELAI = [('moins-1-mois', 'Dès que possible (moins d\'un mois)'), ('1-3-mois', 'Dans 1 à 3 mois'),
         ('3-6-mois', 'Dans 3 à 6 mois'), ('non-defini', 'Pas encore défini')]
SURFACE = [('moins-15', 'Moins de 15 m² (une réparation)'), ('15-50', '15 à 50 m² (une ou deux pièces)'),
           ('50-200', '50 à 200 m² (un appartement, un étage)'), ('plus-200', 'Plus de 200 m², ou plusieurs logements'),
           ('ne-sait-pas', 'Je ne sais pas')]
PREF = [('appel', 'Par téléphone'), ('email', 'Par e-mail'), ('indifferent', 'Peu importe')]
CRENEAU = [('matin', 'Le matin'), ('apres-midi', 'L\'après-midi'), ('indifferent', 'Peu importe')]
CONNU = [('recherche-google', 'Recherche sur Google'), ('carte-google', 'Carte Google'),
         ('recommandation', 'Recommandation d\'un proche ou d\'un voisin'), ('regie-architecte', 'Une régie ou un architecte'),
         ('panneau-vehicule', 'Un panneau de chantier ou un véhicule'), ('facebook', 'Facebook'), ('linkedin', 'LinkedIn'),
         ('autre', 'Autre')]
OBL = ' <span class="req">(obligatoire)</span>'
FAC = ' <span class="opt">(facultatif)</span>'


def cachés(formulaire, source):
    champs = ['page', 'page_entree', 'referent', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']
    return ('<input type="hidden" name="formulaire" value="%s"><input type="hidden" name="canal" value="site">'
            '<input type="hidden" name="source" value="%s"><input type="hidden" name="form_t0" value="">%s'
            '<div class="hp" aria-hidden="true"><label>Ne pas remplir ce champ <input name="site_web" type="text" tabindex="-1" autocomplete="off"></label></div>'
            % (formulaire, source, ''.join('<input type="hidden" name="%s" value="">' % c for c in champs)))


def erreur(fid):
    return '<p class="error" id="%s-err" hidden></p>' % fid


def radios(fid, name, options, legend, statut, aide='', cls='', required=False, describedby=True):
    aide_html = ('<p class="hint" id="%s-aide">%s</p>' % (fid, aide)) if aide else ''
    desc = ' '.join(x for x in [('%s-aide' % fid) if aide else '', '%s-err' % fid] if x)
    opts = ''.join(
        '<label class="choice" for="%s-%s"><input type="radio" id="%s-%s" name="%s" value="%s"%s><span>%s</span></label>'
        % (fid, v, fid, v, name, v, ' required' if required and i == 0 else '', l)
        for i, (v, l) in enumerate(options))
    return ('<fieldset class="group%s" id="%s" aria-describedby="%s" data-champ="%s"><legend>%s%s</legend>%s<div class="choices">%s</div>%s</fieldset>'
            % ((' ' + cls) if cls else '', fid, desc, name, legend, statut, aide_html, opts, erreur(fid)))


def champ(fid, name, label, statut, typ='text', aide='', attrs='', cls=''):
    desc = ' '.join(x for x in [('%s-aide' % fid) if aide else '', '%s-err' % fid] if x)
    aide_html = ('<p class="hint" id="%s-aide">%s</p>' % (fid, aide)) if aide else ''
    if typ == 'textarea':
        inp = '<textarea id="%s" name="%s" rows="5" aria-describedby="%s"%s></textarea>' % (fid, name, desc, attrs)
    else:
        inp = '<input id="%s" name="%s" type="%s" aria-describedby="%s"%s>' % (fid, name, typ, desc, attrs)
    return ('<div class="field%s" data-champ="%s"><label for="%s">%s%s</label>%s%s%s</div>'
            % ((' ' + cls) if cls else '', name, fid, label, statut, aide_html, inp, erreur(fid)))


def rappel_lien():
    return '<p class="dform__rappel"><a href="#rappel" data-vers-rappel>Vous préférez qu\'on vous rappelle ?</a></p>'


def form_devis(source, service=None):
    """Formulaire de devis en 3 étapes. Sans JavaScript : les 3 étapes l'une sous l'autre, un seul envoi."""
    cartes = ''
    for v, nom, ligne in TRAVAUX:
        nom = nom or svc_nom('cloisons-isothermes')
        chk = ' checked' if service == v else ''
        cartes += ('<label class="choice choice--card" for="d-travaux-%s"><input type="checkbox" id="d-travaux-%s" name="travaux[]" value="%s"%s>'
                   '%s<span class="choice__text"><b>%s</b><span>%s</span></span></label>'
                   % (v, v, v, chk, ICONS[v].replace('class="icon"', 'class="icon choice__icon"'), nom, ligne))
    etape1 = '''<fieldset class="dform__step" data-step="1" data-titre="vos travaux">
            <legend class="dform__legend" tabindex="-1"><span class="dform__num">Étape 1 sur 3</span> Quels travaux souhaitez-vous ?</legend>
            <div class="group" id="d-travaux" data-champ="travaux" aria-describedby="d-travaux-aide d-travaux-err">
              <p class="hint" id="d-travaux-aide">Vous pouvez en cocher plusieurs.</p>
              <div class="cards">%s</div>
              %s
            </div>
            <div class="dform__actions js-only"><button type="button" class="btn" data-suivant>Continuer : votre projet</button></div>
            %s
          </fieldset>''' % (cartes, erreur('d-travaux'), rappel_lien())

    etape2 = '''<fieldset class="dform__step" data-step="2" data-titre="votre projet">
            <legend class="dform__legend" tabindex="-1"><span class="dform__num">Étape 2 sur 3</span> Votre projet</legend>
            <p class="dform__oblig">Les champs obligatoires sont indiqués.</p>
            %s
            %s
            <input type="hidden" name="npa" value="">
            %s
            %s
            <div class="dform__actions js-only"><button type="button" class="btn btn--ghost" data-retour>Retour</button><button type="button" class="btn" data-suivant>Continuer : vos coordonnées</button></div>
            %s
          </fieldset>''' % (
        radios('d-type', 'type_client', TYPE_CLIENT, 'Vous êtes', OBL, required=True),
        champ('d-commune', 'commune', 'Commune des travaux', OBL, aide='Commune ou NPA, par exemple Lancy ou 1212.',
              attrs=' autocomplete="address-level2" required maxlength="80"'),
        radios('d-delai', 'delai', DELAI, 'Quand souhaitez-vous faire les travaux ?', FAC),
        radios('d-surface', 'surface', SURFACE, 'Quelle surface, à peu près ?', FAC, aide='Une estimation suffit.'),
        rappel_lien())

    creneau_aide = T('C03', 'Nous appelons du lundi au vendredi, de 7 h à 18 h.', '')
    connu = ''.join('<option value="%s">%s</option>' % c for c in CONNU)
    etape3 = '''<fieldset class="dform__step" data-step="3" data-titre="vos coordonnées">
            <legend class="dform__legend" tabindex="-1"><span class="dform__num">Étape 3 sur 3</span> Vos coordonnées</legend>
            <p class="dform__oblig">Les champs obligatoires sont indiqués.</p>
            %(civ)s
            %(nom)s
            %(tel)s
            %(mail)s
            %(pref)s
            %(creneau)s
            %(msg)s
            <div class="field file-field" data-champ="fichiers">
              <span class="label" id="d-fichiers-label">Photos ou plans%(fac)s</span>
              <p class="hint" id="d-fichiers-aide">JPG, PNG ou PDF, 3 fichiers et 10 Mo au total. Trop lourd ? Envoyez-les par e-mail après notre appel.</p>
              <input class="file-input" id="d-fichiers" name="fichiers[]" type="file" multiple accept="image/jpeg,image/png,application/pdf" aria-labelledby="d-fichiers-label" aria-describedby="d-fichiers-aide d-fichiers-etat d-fichiers-err">
              <div class="file-row js-only"><button type="button" class="btn btn--ghost file-btn" aria-describedby="d-fichiers-aide d-fichiers-etat" data-fichiers>Choisir des fichiers</button><span class="file-state" id="d-fichiers-etat" aria-live="polite">Aucun fichier choisi</span></div>
              <ul class="file-list js-only"></ul>
              %(err_f)s
            </div>
            <div class="field" data-champ="connu_par"><label for="d-connu">Comment nous avez-vous connus ?%(fac)s</label><select id="d-connu" name="connu_par" aria-describedby="d-connu-err"><option value="">Choisissez dans la liste</option>%(connu)s</select>%(err_c)s</div>
            %(reco)s
            <div class="dform__actions"><button type="button" class="btn btn--ghost js-only" data-retour>Retour</button><button type="submit" class="btn" data-envoi>Envoyer ma demande</button></div>
            <p class="dform__info">En envoyant ce formulaire, vous nous transmettez vos coordonnées pour traiter votre demande. Elles ne servent à rien d'autre. <a href="confidentialite.html">Protection des données</a></p>
            %(rap)s
          </fieldset>''' % dict(
        civ=radios('d-civ', 'civilite', [('madame', 'Madame'), ('monsieur', 'Monsieur')], 'Civilité', FAC, cls='group--inline'),
        nom=champ('d-nom', 'nom', 'Nom et prénom', OBL, attrs=' autocomplete="name" required maxlength="100"'),
        tel=champ('d-tel', 'telephone', 'Téléphone', ' <span class="req">(obligatoire si pas d\'e-mail)</span>', typ='tel',
                  aide='Pour vous rappeler et convenir de la visite. Exemple : 079 123 45 67.', attrs=' inputmode="tel" autocomplete="tel" maxlength="30"'),
        mail=champ('d-mail', 'email', 'E-mail', ' <span class="req">(obligatoire si pas de téléphone)</span>', typ='email',
                   aide='Pour vous envoyer la confirmation et l\'offre.', attrs=' autocomplete="email" maxlength="254"'),
        pref=radios('d-pref', 'preference_contact', PREF, 'Comment préférez-vous être recontacté(e) ?', FAC),
        creneau=radios('d-creneau', 'creneau', CRENEAU, 'Plutôt…', FAC, aide=creneau_aide, cls='group--inline js-cond'),
        msg=champ('d-msg', 'message', 'Votre projet en quelques mots', FAC, typ='textarea',
                  aide='Par exemple : logement habité ou vide, délai impératif, accès, étage. Professionnels : date de remise des offres.',
                  attrs=' maxlength="3000"'),
        fac=FAC, err_f=erreur('d-fichiers'), err_c=erreur('d-connu'), connu=connu,
        reco=champ('d-reco', 'recommande_par', 'Qui vous a recommandé Andy Construct ?', FAC, aide='Pour pouvoir remercier cette personne.',
                   attrs=' maxlength="100"', cls='js-cond'),
        rap=rappel_lien())

    reassurance = ''.join('<li>%s</li>' % x for x in [
        T('C01', 'Nous vous rappelons le jour même ou le jour ouvrable suivant.', 'Nous vous rappelons pendant nos heures de bureau.'),
        T('C02', 'La visite et le devis sont gratuits et sans engagement.', 'Vous décidez une fois l\'offre écrite reçue.'),
        'Vos coordonnées servent uniquement à votre demande. Pas de publicité.'])
    return '''<form class="dform" id="d-form" action="api/demande.php" method="post" enctype="multipart/form-data" data-form="devis" data-suivi-formulaire="devis" aria-labelledby="demande-titre"%s>
          %s
          <div class="dform__head js-only" aria-hidden="true"><p class="dform__etape">Étape 1 sur 3</p><div class="dform__bar"><span></span></div></div>
          <p class="visually-hidden" aria-live="polite" data-annonce></p>
          <p class="dform__recap js-only" hidden>Travaux : <b data-recap></b> · <button type="button" class="linklike" data-modifier>Modifier<span class="visually-hidden"> les travaux</span></button></p>
          <div class="dform__erreurs" tabindex="-1" hidden></div>
          %s
          %s
          %s
          <div class="dform__alerte" role="alert" hidden><p data-alerte-texte></p><button type="button" class="btn btn--ghost" data-reessayer>Réessayer</button></div>
        </form>
        <ul class="reassurance">%s</ul>''' % ((' data-service="%s"' % service) if service else '', cachés('devis', source),
                                              etape1, etape2, etape3, reassurance)


def module_rappel(source, seul=False, niveau='h3'):
    sous = (T('C01', 'Nous vous rappelons le jour même ou le jour ouvrable suivant. Votre numéro ne sert qu\'à ce rappel.',
              'Nous vous rappelons pendant nos heures de bureau. Votre numéro ne sert qu\'à ce rappel.')
            if seul else 'Votre numéro ne sert qu\'à ce rappel.')
    return '''<div class="rappel" id="rappel">
          <%(n)s id="rappel-titre">Vous préférez qu'on vous rappelle ?</%(n)s>
          <p>Laissez simplement votre numéro.</p>
          <form class="rform" id="r-form" action="api/demande.php" method="post" data-form="rappel" data-suivi-formulaire="rappel" aria-labelledby="rappel-titre">
            %(caches)s
            %(tel)s
            %(nom)s
            %(cren)s
            <div class="dform__alerte" role="alert" hidden><p data-alerte-texte></p><button type="button" class="btn btn--ghost" data-reessayer>Réessayer</button></div>
            <button type="submit" class="btn" data-envoi>Être rappelé(e)</button>
            <p class="rform__note">%(sous)s</p>
          </form>
        </div>''' % dict(n=niveau, caches=cachés('rappel', source), sous=sous,
                         tel=champ('r-tel', 'telephone', 'Votre numéro de téléphone', OBL, typ='tel', aide='Exemple : 079 123 45 67',
                                   attrs=' inputmode="tel" autocomplete="tel" required maxlength="30"'),
                         nom=champ('r-nom', 'nom', 'Votre nom', FAC, attrs=' autocomplete="name" maxlength="100"'),
                         cren=radios('r-creneau', 'creneau', CRENEAU, 'Plutôt…', FAC, cls='group--inline'))


def par_telephone():
    h = horaires()
    return '''<div class="phone-box" data-suivi-zone="bloc_demande">
          <h3>Par téléphone</h3>
          <p>Bureau : %s</p>
          <p>%s : %s</p>%s
        </div>''' % (tel_link(cls='big'), mob_label(), tel_link(numero='mobile', cls='big'), ('<p class="phone-box__h">%s</p>' % h) if h else '')


def bloc_demande(p, service=None, h2='Demander un devis', intro=None, refs=True, source='accueil', surtitre=True):
    if intro is None:
        intro = ('Encore 2 étapes, moins d\'une minute. Nous vous rappelons pour convenir d\'une visite.' if service
                 else '3 étapes, environ une minute. Nous vous rappelons pour convenir d\'une visite.')
    st = '<p class="eyebrow">Votre demande</p>\n          ' if surtitre else ''
    return '''    <section class="section section--mist demande" id="demande" aria-labelledby="demande-titre" data-suivi-zone="bloc_demande">
      <div class="container">
        <div class="demande__head">
          %s<h2 id="demande-titre">%s</h2>
          <p class="lead">%s</p>
        </div>
        <div class="demande__grid">
          <div class="demande__form">
        %s
          </div>
          <aside class="demande__aside" aria-label="Autres moyens de nous joindre">
        %s
        %s
        %s
          </aside>
        </div>
      </div>
    </section>
''' % (st, h2, intro, form_devis('%s-devis' % source, service), module_rappel('%s-rappel' % source), par_telephone(),
       refs_ligne('refs-line--aside') if refs else '')


def cta_band(p, h2='Vous avez un projet ?', texte='Décrivez-le en trois étapes ou appelez-nous : nous convenons d\'une visite.'):
    return '''    <section class="section section--dark on-dark section--tight" aria-labelledby="cta-titre" data-suivi-zone="bande_appel">
      <div class="container cta-band">
        <div>
          <h2 id="cta-titre">%s</h2>
          <p>%s</p>
        </div>
        <div class="cta-band__actions">
          %s
          <a class="btn btn--light" href="%s" data-suivi-numero="fixe">Appeler le %s</a>
        </div>
      </div>
    </section>
''' % (h2, texte, devis_btn(p, 'bande_appel'), TEL_URI, TEL)


# ---------------------------------------------------------------- témoignages et avis (masqués tant qu'ils sont vides)
def temoignages():
    if not ctx.TEMOIGNAGES:
        return ''
    items = ''
    for t in ctx.TEMOIGNAGES[:3]:
        qui = ', '.join(x for x in [t.get('auteur'), t.get('organisation'), t.get('commune')] if x)
        quoi = ', '.join(x for x in [t.get('travaux'), str(t.get('annee') or '')] if x)
        items += ('<figure class="quote"><blockquote><p>« %s »</p></blockquote><figcaption><b>%s</b>%s</figcaption></figure>'
                  % (e(t['texte']), e(qui), (' · ' + e(quoi)) if quoi else ''))
    return '''    <section class="section" aria-labelledby="temoignages-titre">
      <div class="container">
        <h2 id="temoignages-titre">Ce qu'en disent nos clients</h2>
        <div class="quotes">%s</div>
        <p class="muted">Témoignages publiés tels quels, avec l'accord écrit de leurs auteurs.</p>
      </div>
    </section>
''' % items


def avis_ligne():
    a = ctx.AVIS
    if not a or (a.get('nombre') or 0) < 5 or not a.get('note'):
        return ''
    return ('<p class="avis">Avis Google : %s sur 5, %d avis (relevé le %s). <a href="%s" rel="noopener">Lire les avis sur Google</a></p>'
            % (str(a['note']).replace('.', ','), a['nombre'], e(a.get('date_releve', '')), e(a.get('url', ''))))
