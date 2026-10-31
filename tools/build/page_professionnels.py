# -*- coding: utf-8 -*-
"""Professionnels (architecture §4.4, copy deck §H) : régies, architectes, communes, entreprises."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import page, page_head, ld_page, TEL, TEL_URI, devis_btn, doc, mail, tel_link, ZEFIX, suivi_doc
import composants as c


def build():
    p = dict(fichier='professionnels.html', formulaire=True,
             title='Régies et architectes : plâtrerie, peinture | Andy Construct',
             desc='Plâtrerie, faux-plafonds et peinture pour régies, architectes et communes : immeubles habités, offres sur plans, dossier de références en PDF.')
    ref, check, avis = doc('references'), doc('checklist'), doc('avis-locataires')
    m = mail()
    mailto = lambda sujet: 'mailto:%s?subject=%s' % (m, sujet.replace(' ', '%20'))

    ld = ld_page('professionnels.html', p['title'], 'Professionnels',
                 extra={'audience': {'@type': 'BusinessAudience', 'audienceType': 'Régies, architectes, communes et entreprises'}})
    if ref:
        ld['@graph'].append({'@type': 'DigitalDocument', 'name': 'Dossier de références Andy Construct', 'url': PROD + ref[0],
                             'encodingFormat': 'application/pdf', 'publisher': {'@id': PROD + '#entreprise'}})
    p['ld'] = [ld]

    # 1. En-tête : dossier de références (sans formulaire), soumission, téléphone
    if ref:
        boutons = ('<a class="btn" href="%s" %s>Télécharger le dossier de références (%s)</a>'
                   '<a class="btn btn--ghost" href="#soumission">Envoyer un dossier de soumission</a>' % (ref[0], suivi_doc('references'), ref[1]))
        contenu = 'identité, références, méthode en immeuble habité, lots CFC, contacts' if ref[2] >= 6 else 'identité, références, lots CFC, contacts'
        sous = '<p class="page-head__note">%d pages : %s. Libre téléchargement, sans inscription.</p>' % (ref[2], contenu)
    else:
        boutons = '<a class="btn" href="#soumission">Envoyer un dossier de soumission</a>' + devis_btn(p, 'entete_page', cls='btn btn--ghost')
        sous = ''
    extra = '<div class="page-head__actions">%s</div>%s<p class="page-head__tel">Une question ? %s</p>' % (
        boutons, sous, tel_link(emplacement='entete_page'))
    corps = page_head('Professionnels', 'Régies, architectes, communes : plâtrerie, faux-plafonds et peinture',
                      T('C20', 'Depuis 2007, nous travaillons dans des immeubles habités, des bureaux et des bâtiments publics. Offres sur plans et descriptifs, coordination avec les autres corps de métier, chantier tenu propre.',
                        'Depuis 2007, nous travaillons dans des bureaux, des logements et des bâtiments publics. Offres sur plans et descriptifs, coordination avec les autres corps de métier.'),
                      extra=extra)

    # 2. Selon votre métier (exposition 1 : noms des collectivités dans le texte)
    act_regie = (('<a class="link-arrow" href="%s" %s>Télécharger la liste de contrôle « immeuble habité » (PDF, %d pages, %s)</a>' % (check[0], suivi_doc('checklist'), check[2], check[1].split(', ')[1]))
                 if check else devis_btn(p, 'metier', cls='link-arrow'))
    act_comm = (marque('C13', '<a class="link-arrow" href="%s" data-suivi-emplacement="metier">Demander nos attestations</a>' % mailto("Demande d'attestations"))
                if definitif('C13') else '')
    cartes = [
        ('Régies et gérances',
         T('C20 C09', 'Remises en état entre deux locataires, cages d\'escalier, plafonds après un dégât d\'eau, cloisons pour une arcade. Nous informons les locataires, protégeons les parties communes et tenons la date convenue. Un seul interlocuteur, joignable sur son portable.',
           'Remises en état entre deux locataires, cages d\'escalier, plafonds après un dégât d\'eau, cloisons pour une arcade. Nous protégeons les parties communes. Un interlocuteur joignable.'),
         act_regie),
        ('Architectes et bureaux d\'études',
         T('C14 C22', 'Lots CFC 271 (plâtrerie), 283 (faux-plafonds) et 285 (peinture). Offres complètes sur descriptif, variantes chiffrées à part, questions posées avant de chiffrer. Ouvrages dans des lieux exigeants : salles de musique et de spectacle, écoles d\'art, bureaux.',
           'Lots de plâtrerie et de peinture. Offres complètes sur descriptif, variantes chiffrées à part.'),
         '<a class="link-arrow" href="#soumission">Envoyer un dossier de soumission</a>'),
        ('Communes et institutions',
         'La Ville de Genève et les communes de <span class="nowrap">Plan-les-Ouates</span> et de <span class="nowrap">Collonge-Bellerive</span> (salles communales) nous ont confié des travaux.'
         + T('C19 C13', ' Travaux possibles pendant les vacances scolaires ou entre deux manifestations. Attestations sociales et fiscales sur demande.', ''),
         act_comm),
        ('Entreprises, bureaux et commerces',
         T('C19', 'Cloisons, salles de réunion plus calmes, peinture des locaux : le soir ou le week-end, pour ne pas fermer. Nous préparons le descriptif à remettre à votre bailleur pour son accord.',
           'Cloisons, salles de réunion plus calmes, peinture des locaux, zone par zone. Nous préparons le descriptif à remettre à votre bailleur pour son accord.'),
         devis_btn(p, 'metier', cls='link-arrow')),
    ]
    corps += '''    <section class="section" aria-labelledby="metiers-titre">
      <div class="container">
        <h2 id="metiers-titre">Ce que nous vous apportons</h2>
        <div class="metiers">%s</div>
      </div>
    </section>
''' % ''.join('<div class="metier"><h3>%s</h3><p>%s</p>%s</div>' % x for x in cartes)

    # 3. Méthode en site occupé : chaque point dépend de sa confirmation
    points = [('C20', 'Un avis aux locataires ou aux usagers, préparé avec vous et affiché quelques jours avant.'),
              ('C20', 'Des horaires de travail convenus, communiqués aux habitants.'),
              ('C07', 'Parties communes, ascenseur et sols protégés avant le premier jour.'),
              ('C07', 'La poussière contenue : zone fermée par des bâches, aspiration.'),
              ('C09', 'Un responsable de chantier nommé, joignable pendant toute la durée des travaux.'),
              ('C07', 'Nettoyage chaque soir, passages libres pour les habitants.'),
              ('C06', 'Un imprévu ? Nous le signalons avec son prix, avant de l\'exécuter.'),
              ('C32', 'Réception avec photos et liste des retouches, levées dans le délai convenu.')]
    lis = ''.join('<li>%s</li>' % T(code, txt) for code, txt in points if definitif(code))
    if lis:
        lien = ('<p class="section-foot"><a class="link-arrow" href="%s" %s>Télécharger la liste de contrôle « immeuble habité » (PDF, %d pages, %s)</a></p>' % (check[0], suivi_doc('checklist'), check[2], check[1].split(', ')[1])) if check else ''
        corps += '''    <section class="section section--mist" aria-labelledby="site-occupe-titre">
      <div class="container">
        <div class="section-head">
          <h2 id="site-occupe-titre">Immeubles habités et lieux publics : notre méthode</h2>
          <p class="lead">Les plaintes et les retards naissent presque toujours d'un manque d'organisation. Voici ce que nous faisons à chaque chantier.</p>
        </div>
        <ol class="numlist">%s</ol>
        %s
      </div>
    </section>
''' % (lis, lien)

    # 4. Lots, normes et documents
    lots = T('C14', '<a href="placo.html">271 Plâtrerie</a> · <a href="placo.html#faux-plafonds">283 Faux-plafonds</a> · <a href="peinture.html">285 Traitement des surfaces intérieures (peinture)</a>',
             '<a href="placo.html">271 Plâtrerie</a> · <a href="peinture.html">285 Peinture</a>')
    normes = T('C15 C33', 'Nous travaillons selon la norme SIA 118 lorsque le contrat s\'y réfère. Isolation acoustique et thermique selon les exigences du projet (SIA 181 et SIA 180). Protection incendie selon les prescriptions AEAI lorsque le projet l\'exige.',
               'Les performances visées sont celles du projet, précisées dans l\'offre.')
    lignes = []
    if ref:
        lignes.append(('Dossier de références (%d pages)' % ref[2], '<a href="%s" %s>Télécharger (%s)</a>' % (ref[0], suivi_doc('references'), ref[1])))
    if check:
        lignes.append(('Liste de contrôle : travaux en immeuble habité (%d pages)' % check[2], '<a href="%s" %s>Télécharger (%s)</a>' % (check[0], suivi_doc('checklist'), check[1])))
    if avis and definitif('C20'):
        lignes.append(('Modèle d\'avis aux locataires', marque('C20', '<a href="%s" %s>Télécharger (%s)</a>' % (avis[0], suivi_doc('avis-locataires'), avis[1]))))
    elif check and check[2] >= 3 and definitif('C20'):
        # Pas de fichier Word : le modèle figure en page 3 de la liste de contrôle (livrables/README.md)
        lignes.append(('Modèle d\'avis aux locataires', marque('C20', 'En page 3 de la <a href="%s" %s>liste de contrôle (%s)</a>' % (check[0], suivi_doc('checklist'), check[1]))))
    lignes.append(('Extrait du registre du commerce', '<a href="%s" rel="noopener">Consulter sur Zefix</a>' % ZEFIX))
    if definitif('C12'):
        lignes.append(('Attestation d\'assurance responsabilité civile', T('C12', 'Sur demande, par e-mail')))
    if definitif('C13'):
        lignes.append(('Attestations AVS, LPP, impôts, convention collective', T('C13', 'Sur demande, par e-mail')))
    table = ''.join('<div class="docs__row"><dt>%s</dt><dd>%s</dd></div>' % x for x in lignes)
    corps += '''    <section class="section" aria-labelledby="lots-titre">
      <div class="container">
        <h2 id="lots-titre">Lots, normes et documents</h2>
        <div class="lots">
          <div><h3>Lots CFC</h3><p>%s</p></div>
          <div><h3>Normes</h3><p>%s</p></div>
        </div>
        <h3 class="docs__titre">Documents</h3>
        <dl class="docs"><div class="docs__row docs__row--head" aria-hidden="true"><span>Document</span><span>Comment l'obtenir</span></div>%s</dl>
      </div>
    </section>
''' % (lots, normes, table)

    # 5. Grille complète des références (exposition 2)
    accord = ('<p class="muted">Références citées avec l\'accord des maîtres d\'ouvrage. Contacts de référence sur demande.</p>'
              if ctx.prod() and ctx.confirme('C22') else '')
    corps += '''    <section class="section section--mist" id="references" aria-labelledby="references-titre">
      <div class="container">
        <div class="section-head">
          <h2 id="references-titre">Ils nous ont confié des travaux</h2>
          <p class="lead">%s</p>
        </div>
        %s
        %s
      </div>
    </section>
''' % (marque('C22', '18 maîtres d\'ouvrage publics et privés, à Genève et dans le canton de Vaud.'), c.refs_grille(), accord)

    # 6. Dossier de soumission
    visite = T('C40', '<li>Vous préférez voir notre travail sur place ? Nous vous faisons visiter un chantier en cours.</li>', '')
    corps += '''    <section class="section" id="soumission" aria-labelledby="soumission-titre" data-suivi-zone="soumission">
      <div class="container">
        <div class="encadre encadre--soumission">
          <h2 id="soumission-titre">Envoyer un dossier de soumission</h2>
          <p>Écrivez à <strong>%s</strong> avec :</p>
          <ul class="ticks">
            <li>le descriptif ou la série de prix, et les plans ;</li>
            <li>la date de remise des offres ;</li>
            <li>la date de la visite, si elle est prévue.</li>
          </ul>
          <ul class="notes">
            <li>Fichiers lourds : un lien de transfert (SwissTransfer ou autre) convient.</li>
            <li>%s</li>
            %s
          </ul>
          <p><a class="btn" href="%s">Écrire à Andy Construct</a></p>
        </div>
      </div>
    </section>
''' % (T('C30', m, m),
       T('C01 C09', 'Nous accusons réception le jour même ou le jour ouvrable suivant, avec le nom de la personne qui suit votre dossier.',
         'Nous accusons réception de votre dossier et vous indiquons qui le suit.'),
       visite, mailto('Dossier de soumission'))

    # 7. Demande (sans ligne de références : la grille complète est juste au-dessus)
    corps += c.bloc_demande(p, refs=False, source='professionnels')
    page(p, corps)
