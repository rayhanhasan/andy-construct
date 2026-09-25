# -*- coding: utf-8 -*-
"""Réalisations : galerie statique générée depuis manifest.json (aucun fetch JS)."""
from common import *
from content import REF_GROUPS, REF_NOTE

TITLE = 'Réalisations et références à Genève | Andy Construct'
DESC = "Faux-plafonds et cloisons réalisés pour la Ville de Genève, des salles communales, le Conservatoire, la HEAD, des entreprises et des particuliers."

ORDER = ['plafonds-tendus', 'plafonds-acoustiques', 'plafonds-placo', 'plafonds-metalliques', 'cloisons', 'chantier']

SVG_PREV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
SVG_NEXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
SVG_CLOSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'


def gallery():
    counts = {c: sum(1 for m in MANIFEST if m['categorie'] == c) for c in ORDER}
    filters = ['<li><button type="button" data-filter="toutes" data-label="Toutes" aria-pressed="true">Toutes<span>(%d)</span></button></li>' % len(MANIFEST)]
    for c in ORDER:
        if counts[c]:
            filters.append('<li><button type="button" data-filter="%s" data-label="%s" aria-pressed="false">%s<span>(%d)</span></button></li>'
                           % (c, CAT[c], CAT[c], counts[c]))
    items = []
    for m in MANIFEST:
        b = m['base']
        items.append('''
          <li data-cat="%(cat)s">
            <button type="button" class="gallery__btn" aria-haspopup="dialog" aria-label="Agrandir la photo : %(t)s"
              data-webp="%(b)s-1600.webp" data-jpg="%(b)s-800.jpg" data-w="%(w)d" data-h="%(h)d" data-title="%(t)s" data-label="%(lab)s">
              <span class="media">%(pic)s</span>
              <span class="caption"><b>%(t)s</b><span>%(lab)s</span></span>
            </button>
          </li>''' % dict(cat=m['categorie'], t=e(m['titre']), b=b, w=m['largeur_1600'], h=m['hauteur_1600'],
                          lab=CAT[m['categorie']], pic=pic(m['id'], '(min-width: 1180px) 280px, (min-width: 760px) 33vw, 50vw')))
    return '\n          '.join(filters), ''.join(items)


def build():
    h = head(TITLE, DESC, 'realisations.html', ld=[page_ld('realisations.html', TITLE, 'Réalisations')])
    filters, items = gallery()

    groups = ''
    for g, names in REF_GROUPS:
        lis = ''.join('<li>%s%s</li>' % (e(n), ('<small>%s</small>' % e(REF_NOTE[n])) if REF_NOTE.get(n) else '') for n in names)
        groups += '\n          <div><h3>%s</h3><ul>%s</ul></div>' % (g, lis)

    body = '''
  <main id="contenu">
%(ph)s
    <section class="section" id="galerie" aria-labelledby="galerie-titre">
      <div class="container">
        <div class="section-head section-head--split">
          <div>
            <p class="eyebrow">Galerie</p>
            <h2 id="galerie-titre">Nos chantiers en photos</h2>
          </div>
          <p class="lead">Choisissez un type de travaux, puis cliquez sur une photo pour l'agrandir.</p>
        </div>
        <!-- PROVISOIRE : fiches « Projets choisis » (commune, année, client, besoin, solution) à créer avec les informations du client.
             Galerie générée en HTML statique depuis assets/img/portfolio/manifest.json ; catégories déduites des images, à valider. -->
        <span id="avant-apres"></span><!-- PROVISOIRE : photos avant / après à fournir par le client (ancre conservée pour la redirection 301) -->
        <ul class="filters" aria-label="Filtrer les photos par type de travaux">
          %(filters)s
        </ul>
        <p class="gallery-status" role="status">%(n)d photos affichées</p>
        <ul class="gallery" data-gallery>%(items)s
        </ul>
      </div>
    </section>

    <dialog class="lightbox" id="visionneuse" aria-label="Visionneuse de photos">
      <div class="lightbox__bar">
        <p class="lightbox__count" aria-live="polite"></p>
        <button type="button" class="btn btn--light" data-lb="close">Fermer %(close)s</button>
      </div>
      <div class="lightbox__stage">
        <picture><source type="image/webp"><img alt="" width="1600" height="1200"></picture>
      </div>
      <div class="lightbox__foot">
        <button type="button" class="btn btn--light" data-lb="prev">%(prev)s<span class="lightbox__nav-label">Précédente</span></button>
        <p class="lightbox__caption"><b></b><span></span></p>
        <button type="button" class="btn btn--light" data-lb="next"><span class="lightbox__nav-label">Suivante</span>%(next)s</button>
      </div>
    </dialog>

    <section class="section section--mist" id="references" aria-labelledby="references-titre">
      <div class="container">
        <div class="section-head section-head--split">
          <div>
            <p class="eyebrow">18 références</p>
            <h2 id="references-titre">Ils nous ont fait confiance</h2>
          </div>
          <p class="lead">Collectivités, institutions culturelles, entreprises et hôtels : des maîtres d'ouvrage publics et privés qui nous ont confié leurs travaux.</p>
        </div>
        <!-- PROVISOIRE : à valider avec le client (date de chaque référence, accord pour les logos de marques privées) -->
        <div class="refs-groups">%(groups)s
        </div>
      </div>
    </section>

    <section class="section" id="professionnels" aria-labelledby="pros-titre">
      <div class="container split pros">
        <div>
          <p class="eyebrow">Professionnels</p>
          <h2 id="pros-titre">Pour les architectes, régies et collectivités</h2>
          <p class="lead">Nous établissons nos offres sur la base de vos plans et descriptifs, et nous nous coordonnons avec les autres corps de métier du chantier.</p>
          <p><a class="link-arrow" href="contact.html#devis">Transmettre un dossier</a></p>
        </div>
        <!-- PROVISOIRE : à valider avec le client (codes CFC selon les prestations réelles, dossier de références PDF à produire) -->
        <dl class="pros__list">
          <div><dt>Ouvrages traités</dt><dd>Salles communales et polyvalentes, lieux culturels, bureaux et sièges d'entreprises, laboratoires, commerces et restaurants, logements.</dd></div>
          <div><dt>Codes CFC</dt><dd>271 Plâtrerie · 283 Faux-plafonds · 285 Traitement des surfaces intérieures (peinture)</dd></div>
          <div><dt>Dossier de références</dt><dd>Dossier PDF disponible sur demande, par e-mail à <a href="mailto:%(mail)s">%(mail)s</a>.</dd></div>
          <div><dt>Contact direct</dt><dd><a href="%(tel_uri)s">%(tel)s</a> · <a href="%(mob_uri)s">%(mob)s</a></dd></div>
        </dl>
      </div>
    </section>
%(cta)s  </main>
''' % dict(ph=page_head('Réalisations', 'Réalisations et références',
                        "%d photos prises sur nos chantiers, de la pose de l'ossature à la finition, et les 18 maîtres d'ouvrage qui nous ont fait confiance." % len(MANIFEST)),
           filters=filters, n=len(MANIFEST), items=items, close=SVG_CLOSE, prev=SVG_PREV, next=SVG_NEXT,
           groups=groups, mail=MAIL, tel=TEL, tel_uri=TEL_URI, mob=MOB, mob_uri=MOB_URI,
           cta=cta_band('Votre projet', "Montrez-nous votre local ou vos plans : nous vous conseillons le système adapté et vous remettons une offre détaillée."))

    write('realisations.html', h + header('realisations.html') + body + footer(joined=True))
