# -*- coding: utf-8 -*-
"""L'entreprise v3 (cro-v3 §6.3) : récit court et frise chronologique réelle (registre du commerce, FOSC :
docs/v2/dossier-client.md §4), métier inscrit au registre, engagements, méthode, chiffres, identité vérifiable,
rappel des références."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import page, hero_page, ld_page, ZEFIX, IDE, LEGAL, devis_btn
import composants as c
from composants import I_BADGE


def build():
    hero_html, preload = c.hero_image('photo', 'chantier-suspentes-ossature-01')
    p = dict(fichier='entreprise.html', preload=preload, title='L\'entreprise, à Carouge depuis 2007 | Andy Construct',
             desc='Andy Construct, Chanton & Cie : entreprise de Carouge inscrite au registre du commerce depuis 2007. Histoire, méthode, engagements, identité.')
    p['ld'] = [ld_page('entreprise.html', p['title'], 'L\'entreprise', typ='AboutPage', extra={'about': {'@id': PROD + '#entreprise'}})]

    actions = '%s<a class="btn btn--light" href="#methode">Notre méthode</a>' % devis_btn(p, 'entete_page')
    corps = hero_page('L\'entreprise', 'Andy Construct, entreprise de Carouge depuis 2007',
                      T('C10 C09', 'Plâtrerie, peinture et isolation intérieure. Deux associés qui <b>suivent eux-mêmes</b> les chantiers.',
                        'Plâtrerie, peinture et isolation intérieure, dirigée par <b>deux associés</b>.'),
                      actions=actions, media=hero_html, badges=c.badges(['B1', 'B2', 'B3'], cls='badges--3'))

    # Frise réelle : FOSC 126/2007 (début le 01.06.2007 à Perly-Certoux), FOSC 44/2010 (Chêne-Bourg), FOSC du 02.05.2023 (Carouge)
    frise = [
        ('2007', '1<sup>er</sup> juin', 'Perly-Certoux', 'Début de l\'activité et inscription au <b>registre du commerce</b> de Genève.'),
        ('2010', 'Février', 'Chêne-Bourg', 'Le siège s\'installe à Chêne-Bourg ; le but social actuel est inscrit.'),
        ('2023', 'Mai', 'Carouge', 'Siège route des Acacias.' + T('C10', ' Caroline Chanton Bajrami rejoint Adnan Bajrami comme <b>associée</b>.', '')),
        ('Aujourd\'hui', '', 'Suisse romande', '<a href="placo.html">Placo</a>, <a href="peinture.html">peinture</a>, <a href="isolation-acoustique.html">isolation acoustique</a> et '
         '<a href="cloisons-isothermes.html">%s</a>.' % T('C16', 'cloisons isolantes', 'cloisons isothermes')),
    ]
    lis = ''.join('<li><p class="frise__date%s">%s</p><p class="frise__lieu">%s%s</p><p>%s</p></li>'
                  % ('' if a.isdigit() else ' frise__date--mot', a, ('%s · ' % m) if m else '', l, t) for a, m, l, t in frise)
    corps += '''    <section class="section" aria-labelledby="histoire-titre">
      <div class="container">
        <div class="section-head">
          <h2 id="histoire-titre">Notre histoire</h2>
          <p class="lead">Née à <b>Perly-Certoux</b> en 2007, installée à <b>Carouge</b> depuis 2023 : une entreprise genevoise du second œuvre.</p>
        </div>
        <ol class="frise" data-trait>%s</ol>
      </div>
    </section>
''' % lis
    # Rappel des références juste après le récit (loin du rappel du pied de page : jamais deux listes dans le même écran)
    corps += c.bande_refs(titre_id='refs-entreprise-titre')

    # Le métier, tel qu'inscrit au registre du commerce (citation et source seulement, cro-v3 §6.3)
    corps += c.feat('metier-titre', 'Notre métier, inscrit au registre du commerce',
                    '<figure class="citation"><blockquote><p>« Pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, '
                    'plâtrerie, peinture, aménagement de logements et bureaux. »</p></blockquote><figcaption>But social, registre du commerce de Genève</figcaption></figure>',
                    c.media('ill', 'interieur-porte-coulissante-chene', '(min-width: 1440px) 660px, (min-width: 1000px) 46vw, 100vw'),
                    inverse=True, cls='section--mist')

    # Engagements (3 à 4 points, selon les confirmations ; aucune promesse non confirmée en production)
    engs = [('offre', 'Venir voir avant de chiffrer', 'Nous mesurons et écoutons sur place, puis remettons une <b>offre écrite</b>.', None),
            ('registre', 'Une entreprise vérifiable', 'Inscrite au <b>registre du commerce</b> depuis 2007, numéro IDE public.', None),
            ('visite', 'Aucun supplément surprise', 'Un imprévu est <b>annoncé et chiffré</b> avant d\'être exécuté, avec votre accord.', 'C06'),
            ('lieu', 'Des lieux respectés', T('C07', 'Protections posées avant de commencer, <b>nettoyage chaque soir</b>.',
                                             'Sols et passages <b>protégés</b> pendant les travaux.'), None)]
    items = ''
    for ic, t, d, code in engs:
        if code and not definitif(code):
            continue
        li = ('<li class="eng"><svg class="eng__i" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg><h3>%s</h3><p>%s</p></li>'
              % (I_BADGE[ic], t, marque(code, d) if code else d))
        items += li
    corps += '''    <section class="section" aria-labelledby="engagements-titre">
      <div class="container">
        <div class="section-head"><h2 id="engagements-titre">Nos engagements</h2></div>
        <ul class="engs">%s</ul>
      </div>
    </section>
''' % items

    corps += '''    <section class="section section--mist" id="methode" aria-labelledby="methode-titre">
      <div class="container">
        <div class="section-head"><h2 id="methode-titre">Notre méthode, de la visite à la réception</h2></div>
        %s
      </div>
    </section>
''' % c.methode(True)
    corps += c.chiffres()

    # L'équipe : masquée tant que photos et accords manquent (C10, C24)
    lignes = [('Raison sociale', LEGAL), ('Forme juridique', 'société en nom collectif'),
              ('Numéro IDE', '%s · <a href="%s" rel="noopener">Vérifier au registre du commerce</a>' % (IDE, ZEFIX)),
              ('Siège', 'Route des Acacias 48, 1227 Carouge (Genève)'), ('Activité', 'depuis le 1<sup>er</sup> juin 2007')]
    if definitif('C11'):
        lignes.append(('Association professionnelle', T('C11', 'membre du GGE, Groupement des entreprises genevoises du bâtiment')))
    if definitif('C12'):
        lignes.append(('Assurance', T('C12', 'responsabilité civile d\'entreprise, attestation sur demande')))
    if definitif('C28'):
        lignes.append(('Paiement', T('C28', 'Nous ne demandons jamais de paiement en liquide à l\'avance.')))
    garantie = T('C32', 'Appelez-nous dès que vous le constatez : nous venons voir et <b>nous réparons</b> ce qui relève de notre travail.',
                 'Appelez-nous dès que vous le constatez : <b>nous venons voir</b>.')
    loi = T('V01', '<details class="loi"><summary>Ce que dit la loi</summary><p>Pour les contrats conclus depuis le 1<sup>er</sup> janvier 2026 : un défaut d\'un ouvrage peut être signalé dans les 60 jours qui suivent sa découverte, et le droit à la réparation gratuite ne peut plus être exclu par contrat pour un élément de construction. L\'action se prescrit par cinq ans pour un ouvrage immobilier. Si votre contrat se réfère à la norme SIA 118, le délai de garantie est de deux ans.</p></details>', '')
    corps += '''    <section class="section" aria-labelledby="verifier-titre">
      <div class="container split split--48">
        <div>
          <h2 id="verifier-titre">Vérifiez qui nous sommes</h2>
          <p class="muted">Avant de laisser entrer une entreprise chez vous, vous pouvez vérifier son identité.</p>
          %s
        </div>
        <div>
          <dl class="identite">%s</dl>
          <div class="encadre encadre--defaut">
            <h3 id="defaut-titre">Si un défaut apparaît après les travaux</h3>
            <p>%s</p>
            %s
          </div>
        </div>
      </div>
    </section>
''' % (c.badges(['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'B8', 'B10', 'B11'], cls='badges--clair badges--col badges--verif', label='Vérifiable'),
       ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % x for x in lignes), garantie, loi)
    corps += c.cta_band(p)
    page(p, corps)
