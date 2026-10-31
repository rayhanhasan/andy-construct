# -*- coding: utf-8 -*-
"""Professionnels v3 (cro-v3 §6.2) : page B2B premium. En-tête « Envoyer un dossier de soumission », mur complet des
références (par secteur), chiffres, documents téléchargeables mis en avant (couvertures), ce que nous apportons,
lots CFC, méthode en site occupé illustrée, mini-cas public, soumission, demande."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import page, hero_page, ld_page, TEL, TEL_URI, devis_btn, doc, mail, tel_link, ZEFIX, suivi_doc
import composants as c


def couverture(nom, alt):
    b = 'assets/img/docs/%s-couverture' % nom
    return ('<picture><source type="image/webp" srcset="%s-320.webp 320w, %s-640.webp 640w" sizes="(min-width: 1000px) 200px, 140px">'
            '<img src="%s-640.jpg" width="640" height="906" alt="%s" loading="lazy" decoding="async"></picture>' % (b, b, b, e(alt)))


def build():
    ref, check, avis = doc('references'), doc('checklist'), doc('avis-locataires')
    hero_html, preload = c.hero_image('photo', 'plafond-placo-ilot-ovale-01')
    p = dict(fichier='professionnels.html', formulaire=True, preload=preload,
             title='Régies et architectes : plâtrerie, peinture | Andy Construct',
             desc='Plâtrerie, faux-plafonds et peinture pour régies, architectes et communes : immeubles habités, offres sur plans, dossier de références en PDF.')
    m = mail()
    mailto = lambda sujet: 'mailto:%s?subject=%s' % (m, sujet.replace(' ', '%20'))

    ld = ld_page('professionnels.html', p['title'], 'Professionnels',
                 extra={'audience': {'@type': 'BusinessAudience', 'audienceType': 'Régies, architectes, communes et entreprises'}})
    if ref:
        ld['@graph'].append({'@type': 'DigitalDocument', 'name': 'Dossier de références Andy Construct', 'url': PROD + ref[0],
                             'encodingFormat': 'application/pdf', 'publisher': {'@id': PROD + '#entreprise'}})
    p['ld'] = [ld]

    # 1. En-tête : action principale « Envoyer un dossier de soumission », dossier de références en second
    actions = '<a class="btn" href="#soumission" data-suivi="devis_clic" data-suivi-emplacement="entete_page">Envoyer un dossier de soumission</a>'
    if ref:
        actions += '<a class="btn btn--light" href="%s" %s>Dossier de références (%s)</a>' % (ref[0], suivi_doc('references'), ref[1])
    corps = hero_page('Professionnels', 'Régies, architectes, communes : plâtrerie, faux-plafonds et peinture',
                      T('C20', 'Immeubles habités, bureaux et bâtiments publics, <b>depuis 2007</b>. Offres sur plans et descriptifs.',
                        'Bureaux, logements et bâtiments publics, <b>depuis 2007</b>. Offres sur plans et descriptifs.'),
                      actions=actions, media=hero_html,
                      badges=c.badges(['B1', 'B5', 'B8', 'B10']))

    # 2. Références complètes (ancre conservée : redirection 301 de /realisations/references), puis les chiffres
    accord = ('<p class="muted">Références citées avec l\'accord des maîtres d\'ouvrage. Contacts de référence sur demande.</p>'
              if ctx.prod() and ctx.confirme('C22') else '')
    corps += '''    <section class="section section--mist mur" id="references" aria-labelledby="references-titre" data-suivi-zone="references">
      <div class="container">
        <div class="section-head section-head--row">
          <div>
            <h2 id="references-titre">Ils nous ont confié des travaux</h2>
            <p class="lead">%s</p>
          </div>
          %s
        </div>
        %s
        %s
      </div>
    </section>
''' % (marque('C22', '<b>%d références</b>, publiques et privées, à Genève et dans le canton de Vaud.' % c.nb_refs()),
       ('<a class="link-arrow" href="%s" %s>Le dossier de références (%s)</a>' % (ref[0], suivi_doc('references'), ref[1])) if ref else '',
       c.mur_complet(par_secteur=True), accord)
    corps += c.chiffres()

    # 3. Documents téléchargeables, mis en avant avec leur couverture
    cartes = ''
    if ref:
        cartes += ('<li class="docc"><a class="docc__couv" href="%s" %s tabindex="-1" aria-hidden="true">%s</a><div class="docc__txt">'
                   '<h3>Dossier de références</h3><p>Identité, références, méthode en immeuble habité, <b>lots CFC</b>, contacts. %d pages.</p>'
                   '<a class="btn" href="%s" %s>Télécharger (%s)</a></div></li>'
                   % (ref[0], suivi_doc('references'), couverture('andy-construct-references', ''), ref[2], ref[0], suivi_doc('references'), ref[1]))
    if check:
        cartes += ('<li class="docc"><a class="docc__couv" href="%s" %s tabindex="-1" aria-hidden="true">%s</a><div class="docc__txt">'
                   '<h3>Liste de contrôle : immeuble habité</h3><p>Avant, pendant et après les travaux : ce qu\'une régie <b>vérifie</b>, quelle que soit l\'entreprise. %d pages.</p>'
                   '<a class="btn btn--ghost" href="%s" %s>Télécharger (%s)</a></div></li>'
                   % (check[0], suivi_doc('checklist'), couverture('checklist-chantier-site-occupe', ''), check[2], check[0], suivi_doc('checklist'), check[1]))
    autres = ['<li>Extrait du registre du commerce : <a href="%s" rel="noopener">consulter sur Zefix</a></li>' % ZEFIX]
    if avis and definitif('C20'):
        autres.append('<li>%s</li>' % marque('C20', 'Modèle d\'avis aux locataires : <a href="%s" %s>télécharger (%s)</a>' % (avis[0], suivi_doc('avis-locataires'), avis[1])))
    elif check and check[2] >= 3 and definitif('C20'):
        autres.append('<li>%s</li>' % marque('C20', 'Modèle d\'avis aux locataires : en page 3 de la liste de contrôle'))
    if definitif('C12'):
        autres.append('<li>%s</li>' % T('C12', 'Attestation d\'assurance responsabilité civile : sur demande, par e-mail'))
    if definitif('C13'):
        autres.append('<li>%s</li>' % T('C13', 'Attestations AVS, LPP, impôts, convention collective : <a href="%s">sur demande</a>' % mailto("Demande d'attestations")))
    corps += '''    <section class="section" aria-labelledby="docs-titre">
      <div class="container">
        <div class="section-head section-head--row">
          <h2 id="docs-titre">Documents à télécharger</h2>
          <p>Libre téléchargement, sans inscription.</p>
        </div>
        <ul class="doccs">%s</ul>
        <ul class="ticks docs-autres">%s</ul>
      </div>
    </section>
''' % (cartes, ''.join(autres))

    # 4. Ce que nous vous apportons (20 mots par carte)
    act_regie = (('<a class="link-arrow" href="%s" %s>La liste de contrôle (%s)</a>' % (check[0], suivi_doc('checklist'), check[1].split(', ')[1]))
                 if check else devis_btn(p, 'metier', cls='link-arrow'))
    metiers = [
        ('Régies et gérances', T('C20', 'Remises en état, cages d\'escalier, plafonds après dégât d\'eau. <b>Parties communes protégées</b>, date convenue tenue.',
                                 'Remises en état, cages d\'escalier, plafonds après dégât d\'eau. <b>Parties communes protégées</b>.'), act_regie),
        ('Architectes et bureaux d\'études', T('C14', 'Lots <b>CFC 271, 283 et 285</b>. Offres complètes sur descriptif, variantes à part, questions posées avant de chiffrer.',
                                              'Lots de <b>plâtrerie et de peinture</b>. Offres complètes sur descriptif, variantes chiffrées à part.'),
         '<a class="link-arrow" href="#soumission">Envoyer un dossier</a>'),
        ('Communes et institutions', 'La Ville de Genève, <span class="nowrap">Plan-les-Ouates</span> et <span class="nowrap">Collonge-Bellerive</span> nous ont confié des travaux.'
         + T('C19', ' Interventions pendant les <b>vacances scolaires</b>.', ''), ''),
        ('Entreprises, bureaux et commerces', T('C19', 'Cloisons, salles de réunion plus calmes, peinture : <b>le soir ou le week-end</b>.',
                                               'Cloisons, salles de réunion plus calmes, peinture : <b>zone par zone</b>.'), devis_btn(p, 'metier', cls='link-arrow')),
    ]
    corps += '''    <section class="section section--mist" aria-labelledby="metiers-titre">
      <div class="container">
        <div class="section-head"><h2 id="metiers-titre">Ce que nous vous apportons</h2></div>
        <ul class="metiers">%s</ul>
      </div>
    </section>
''' % ''.join('<li class="metier"><h3>%s</h3><p>%s</p>%s</li>' % x for x in metiers)

    # 5. Lots CFC et normes
    lots = [('271', 'placo.html', 'Plâtrerie'), ('283', 'placo.html#faux-plafonds', marque('C14', 'Faux-plafonds')), ('285', 'peinture.html', 'Peinture intérieure')]
    if not definitif('C14'):
        lots = [x for x in lots if x[0] != '283']
    lis = ''.join('<li><span class="cfc__n">CFC %s</span><a href="%s">%s</a></li>' % x for x in lots)
    normes = T('C15', 'Performances acoustiques, thermiques et incendie : celles du projet (<b>SIA 181, SIA 180, AEAI</b>), précisées dans l\'offre.',
               'Les performances visées sont celles du projet, précisées dans l\'offre.')
    corps += '''    <section class="section" aria-labelledby="lots-titre">
      <div class="container">
        <div class="section-head"><h2 id="lots-titre">Lots CFC</h2></div>
        <ul class="cfc">%s</ul>
        <p class="cfc__normes">%s</p>
      </div>
    </section>
''' % (lis, normes)

    # 6. Méthode en site occupé (6 points), illustrée d'une vraie photo : escalier protégé pendant les travaux
    points = [('C20', 'Avis aux locataires et horaires convenus, affichés quelques jours avant.'),
              ('C07', 'Parties communes, ascenseur et sols <b>protégés dès le premier jour</b>.'),
              ('C07', 'Poussière contenue, <b>nettoyage chaque soir</b>, passages libres.'),
              ('C09', 'Un <b>responsable de chantier</b> nommé, joignable.'),
              ('C06', 'Un imprévu est <b>chiffré avant</b> d\'être exécuté.'),
              ('C32', 'Réception avec photos et liste des retouches.')]
    lis = ''.join('<li><span>%s</span></li>' % T(code, txt) for code, txt in points if definitif(code))
    if lis:
        photo = 'habillage-placo-niches-arrondies-01'
        import portfolio as pf
        corps += c.feat('site-occupe-titre', 'Immeubles habités et lieux publics : notre méthode',
                        '<ol class="numlist numlist--1">%s</ol>%s' % (lis, ('<p><a class="link-arrow" href="%s" %s>La liste de contrôle « immeuble habité » (%s)</a></p>'
                                                                             % (check[0], suivi_doc('checklist'), check[1])) if check else ''),
                        c.media('photo', photo, '(min-width: 1440px) 660px, (min-width: 1000px) 46vw, 100vw', fmt='4x5'),
                        inverse=True, legende=pf.legende(photo), cls='feat--haut')

    # 7. Collectivités : cartes typographiques (aucune photo rattachée à ces lieux ; nature et année des travaux : C22)
    salles = ''.join('<li class="lieu lieu--typo"><span class="lieu__type">Collectivité</span><span class="lieu__nom">%s</span>'
                     '<span class="laser laser--court" aria-hidden="true"></span><span class="lieu__commune">%s</span></li>'
                     % (c.insec(e(c.nom_ref(rid))), commune) for rid, commune in (('plan-les-ouates', 'Plan-les-Ouates'), ('collonge-bellerive', 'Collonge-Bellerive')))
    corps += '''    <section class="section section--dark on-dark" aria-labelledby="public-titre" data-trait>
      <div class="container cas-public">
        <div>
          <h2 id="public-titre">Collectivités</h2>
          <span class="laser laser--court" aria-hidden="true"></span>
          <p class="lead">La Ville de Genève et deux communes genevoises nous ont confié des travaux, dont leurs <b>salles communales</b>.</p>
        </div>
        <ul class="cas-public__lieux">%s</ul>
      </div>
    </section>
''' % salles

    # 8. Dossier de soumission
    visite = T('C40', 'Vous préférez voir notre travail ? Nous vous faisons visiter un chantier en cours.', '')
    corps += '''    <section class="section soumission" id="soumission" aria-labelledby="soumission-titre" data-suivi-zone="soumission">
      <div class="container soumission__grid">
        <div>
          <h2 id="soumission-titre">Envoyer un dossier de soumission</h2>
          <span class="laser laser--court" aria-hidden="true"></span>
          <p class="lead">Écrivez à <b>%s</b> avec le descriptif ou la série de prix, les plans, la date de remise des offres et, si elle est prévue, la date de la visite.</p>
          <p class="soumission__cta"><a class="btn" href="%s" data-suivi="devis_clic" data-suivi-emplacement="soumission">Envoyer un dossier de soumission</a><a class="btn btn--ghost" href="%s" data-suivi-numero="fixe" data-suivi-emplacement="soumission">Appeler le %s</a></p>
        </div>
        <ul class="ticks ticks--filets">
          <li>Fichiers lourds : un <b>lien de transfert</b> (SwissTransfer ou autre) convient.</li>
          <li>%s</li>
          %s
        </ul>
      </div>
    </section>
''' % (T('C30', m, m), mailto('Dossier de soumission'), TEL_URI, TEL,
       T('C01 C09', 'Accusé de réception <b>le jour même</b> ou le jour ouvrable suivant, avec le nom de la personne qui suit votre dossier.',
         'Nous accusons réception de votre dossier et vous indiquons <b>qui le suit</b>.'),
       ('<li>%s</li>' % visite) if visite else '')

    # 9. Demande (sans ligne de références : le mur complet est plus haut)
    corps += c.bloc_demande(p, refs=False, source='professionnels')
    page(p, corps)
