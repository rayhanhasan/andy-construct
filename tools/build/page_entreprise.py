# -*- coding: utf-8 -*-
"""L'entreprise (architecture §4.5, copy deck §I)."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import page, page_head, ld_page, ZEFIX, IDE, LEGAL, svc_nom, SERVICES, svc_url
import composants as c


def build():
    p = dict(fichier='entreprise.html', title='L\'entreprise, à Carouge depuis 2007 | Andy Construct',
             desc='Andy Construct, Chanton & Cie : entreprise de Carouge inscrite au registre du commerce depuis 2007. Histoire, méthode, engagements, identité.')
    p['ld'] = [ld_page('entreprise.html', p['title'], 'L\'entreprise', typ='AboutPage', extra={'about': {'@id': PROD + '#entreprise'}})]

    corps = page_head('L\'entreprise', 'Andy Construct, entreprise de Carouge depuis 2007',
                      T('C10 C09', 'Une entreprise genevoise de plâtrerie, de peinture et d\'isolation intérieure, dirigée par ses deux associés, qui suivent eux-mêmes les chantiers.',
                        'Une entreprise genevoise de plâtrerie, de peinture et d\'isolation intérieure, dirigée par ses deux associés.'))

    aujourdhui = ('<a href="placo.html">Placo</a>, <a href="peinture.html">peinture</a>, <a href="isolation-acoustique.html">isolation acoustique</a> '
                  'et <a href="cloisons-isothermes.html">%s</a>, dans toute la Suisse romande.' % T('C16', 'cloisons isolantes', 'cloisons isothermes'))
    frise = [
        ('2007', 'Début de l\'activité le 1<sup>er</sup> juin 2007, à Perly-Certoux. Inscription au registre du commerce de Genève.'),
        ('2010', 'Le siège s\'installe à Chêne-Bourg.'),
        ('2023', 'Le siège s\'installe à Carouge, route des Acacias.' + T('C10', ' Caroline Chanton Bajrami rejoint Adnan Bajrami comme associée.', '')),
        ('Aujourd\'hui', aujourdhui),
    ]
    corps += '''    <section class="section" aria-labelledby="histoire-titre">
      <div class="container split split--48">
        <h2 id="histoire-titre">Notre histoire</h2>
        <div>
          <ol class="frise">%s</ol>
          <p class="frise__refs">Au fil des années, la Ville de Genève, le Conservatoire de musique de Genève, la HEAD et des particuliers de toute la région nous ont confié des travaux.</p>
        </div>
      </div>
    </section>

    <section class="section section--mist" aria-labelledby="metier-titre">
      <div class="container split split--48">
        <h2 id="metier-titre">Notre métier, tel qu'il est inscrit au registre du commerce</h2>
        <div>
          <figure class="citation">
            <blockquote><p>« Pose de faux-plafonds phoniques et cloisons légères phoniques et thermiques, isolations intérieures, plâtrerie, peinture, aménagement de logements et bureaux. »</p></blockquote>
            <figcaption>But social inscrit au registre du commerce de Genève</figcaption>
          </figure>
          <p>%s</p>
        </div>
      </div>
    </section>
''' % (''.join('<li><b>%s</b><p>%s</p></li>' % x for x in frise),
       T('C05', 'Ces métiers se suivent sur un même chantier : ossature, isolant, plaques, joints, peinture. Les réunir évite d\'attendre un autre artisan entre deux étapes.',
         'Ces métiers se suivent sur un même chantier : ossature, isolant, plaques, joints, peinture.'))

    principes = [('C06', 'Venir voir avant de chiffrer', 'Pas de prix au mètre carré au téléphone : nous mesurons et nous écoutons d\'abord.'),
                 ('C06', 'Une offre lisible', 'Poste par poste, en CHF, avec la durée et ce qui n\'est pas compris.'),
                 ('C06', 'Aucun supplément surprise', 'Un imprévu est annoncé et chiffré avant d\'être exécuté, avec votre accord écrit.'),
                 ('C07', 'Des lieux respectés', 'Protections posées avant de commencer, nettoyage chaque soir.')]
    cartes = [marque(code, '<div class="principe"><h3>%s</h3><p>%s</p></div>' % (t, d), bloc=True) for code, t, d in principes if definitif(code)]
    if len(cartes) >= 2:
        corps += '''    <section class="section" aria-labelledby="principes-titre">
      <div class="container">
        <h2 id="principes-titre">Ce qui guide notre travail</h2>
        <div class="principes">%s</div>
      </div>
    </section>
''' % ''.join(cartes)

    corps += '''    <section class="section section--mist" id="methode" aria-labelledby="methode-titre">
      <div class="container">
        <h2 id="methode-titre">Notre méthode, de la visite à la réception</h2>
        %s
      </div>
    </section>
''' % c.methode(True)

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
    garantie = T('C32', 'Appelez-nous dès que vous le constatez : nous venons voir et nous réparons ce qui relève de notre travail.',
                 'Appelez-nous dès que vous le constatez : nous venons voir.')
    loi = T('V01', '<p>Ce que dit la loi suisse, pour les contrats conclus depuis le 1<sup>er</sup> janvier 2026 : un défaut d\'un ouvrage peut être signalé dans les 60 jours qui suivent sa découverte, et le droit à la réparation gratuite ne peut plus être exclu par contrat pour un élément de construction. L\'action se prescrit par cinq ans pour un ouvrage immobilier. Si votre contrat se réfère à la norme SIA 118, le délai de garantie est de deux ans.</p>', '')
    corps += '''    <section class="section" aria-labelledby="verifier-titre">
      <div class="container split split--48">
        <div>
          <h2 id="verifier-titre">Vérifiez qui nous sommes</h2>
          <p>Avant de laisser entrer une entreprise chez vous, vous pouvez vérifier son identité. Voici la nôtre.</p>
        </div>
        <dl class="identite">%s</dl>
      </div>
    </section>

    <section class="section section--tight" aria-labelledby="defaut-titre">
      <div class="container">
        <div class="encadre">
          <h2 id="defaut-titre">Si un défaut apparaît après les travaux</h2>
          <p>%s</p>
          %s
        </div>
      </div>
    </section>
''' % (''.join('<div><dt>%s</dt><dd>%s</dd></div>' % x for x in lignes), garantie, loi)
    corps += c.cta_band(p)
    page(p, corps)
