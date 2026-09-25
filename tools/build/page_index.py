# -*- coding: utf-8 -*-
from common import *
from content import *
from icons import ICONS

HERO = 'plafond-tendu-ilots-lumineux-01'
ABOUT = 'chantier-pose-plafond-lumineux-01'
WORKS = ['plafond-lumineux-circulaire-01', 'paroi-lumineuse-imprimee-01', 'plafond-couronnes-lumineuses-01',
         'panneaux-acoustiques-muraux-01', 'chantier-ossature-puits-de-lumiere-01', 'faux-plafond-placo-gorge-lumineuse-02']

TITLE = 'Faux-plafonds et cloisons à Genève | Andy Construct'
DESC = "Faux-plafonds, cloisons, isolation phonique et peinture à Genève et dans l'ouest vaudois. Particuliers, régies, architectes. Tél. +41 22 771 20 15."


def build():
    graph = {'@context': 'https://schema.org', '@graph': [
        BUSINESS,
        {'@type': 'WebSite', '@id': PROD + '#site', 'url': PROD, 'name': 'Andy Construct', 'inLanguage': 'fr-CH',
         'publisher': {'@id': PROD + '#entreprise'}},
        {'@type': 'WebPage', '@id': PROD + '#accueil', 'url': PROD, 'name': TITLE, 'inLanguage': 'fr-CH',
         'isPartOf': {'@id': PROD + '#site'}, 'about': {'@id': PROD + '#entreprise'}},
    ]}
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': PROD + '#faq', 'inLanguage': 'fr-CH',
              'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    h = head(TITLE, DESC, 'index.html', preload=hero_preload(HERO), ld=[
        (graph, 'PROVISOIRE : à valider avec le client (legalName, foundingDate 2007, adresse de Carouge, geo approximatif, e-mail, horaires)'),
        (faq_ld, 'FAQ : texte identique au texte visible (brief SEO §6.3)')])

    refs = ''.join('<li>%s%s</li>' % (e(n), ('<small>%s</small>' % e(s)) if s else '') for n, s in REFS)

    services = ''.join('''
          <li class="service">
            <span class="service__icon">%s</span>
            <h3>%s</h3>
            <p>%s</p>
            <a class="link-arrow" href="prestations.html#%s">En savoir plus<span class="visually-hidden"> : %s</span></a>
          </li>''' % (ICONS[ic], t, d, anchor, t) for ic, t, anchor, d in HOME_SERVICES)
    also = ''.join('<li><a href="prestations.html#%s">%s</a></li>' % (a, t) for t, a in ALSO)

    works = ''
    for pid in WORKS:
        it = BY[pid]
        works += '''
          <li>
            <a href="realisations.html?categorie=%s">
              <span class="media">%s</span>
              <span class="caption"><span class="tag">%s</span><b>%s</b></span>
            </a>
          </li>''' % (it['categorie'], pic(pid, '(min-width: 1024px) 380px, (min-width: 640px) 50vw, 100vw'),
                      CAT[it['categorie']], e(it['titre']))

    faq = ''.join('''
            <details>
              <summary>%s</summary>
              <div><p>%s</p></div>
            </details>''' % (e(q), e(a)) for q, a in FAQ)

    body = '''
  <main id="contenu">
    <!-- ================= HÉRO ================= -->
    <section class="hero" aria-labelledby="titre-page">
      <div class="hero__media">%(hero_pic)s</div>
      <div class="container hero__inner">
        <div class="hero__content">
          <!-- PROVISOIRE : à confirmer avec le client (inscription au registre du commerce depuis 2007) -->
          <p class="eyebrow">Entreprise genevoise depuis 2007</p>
          <h1 id="titre-page">Faux-plafonds, cloisons et isolation à Genève</h1>
          <p class="hero__text">Plafonds · Cloisons · Peinture. Pour les particuliers, les régies, les architectes et les collectivités, de Genève à Nyon.</p>
          <div class="hero__actions">
            <a class="btn" href="#devis">Demander un devis</a>
            <a class="btn btn--light" href="%(tel_uri)s">Appeler le %(tel)s</a>
          </div>
        </div>
        <ul class="hero__facts" aria-label="En bref">
          <li><strong>Depuis 2007</strong><span>Siège à Carouge (Genève)</span></li>
          <li><strong>18 références publiques</strong><span>Collectivités, culture, entreprises</span></li>
          <li><strong>Genève et Vaud</strong><span>Jusqu'à Coppet et Nyon</span></li>
          <!-- PROVISOIRE : à valider avec le client (devis gratuit et sans engagement, établi après visite) -->
          <li><strong>Devis gratuit</strong><span>Après visite sur place</span></li>
        </ul>
      </div>
    </section>

    <!-- ================= RÉFÉRENCES ================= -->
    <section class="section" aria-labelledby="refs-titre">
      <div class="container split split--48 refs">
        <div>
          <p class="eyebrow">Références</p>
          <h2 id="refs-titre">Ils nous ont fait confiance</h2>
          <p class="muted">Collectivités publiques, lieux culturels, horlogerie, banques, laboratoires : des maîtres d'ouvrage exigeants nous ont confié leurs plafonds et leurs cloisons.</p>
          <a class="link-arrow" href="realisations.html#references">Voir les références par secteur</a>
        </div>
        <ul class="refs-list">%(refs)s</ul>
      </div>
    </section>

    <!-- ================= L'ENTREPRISE ================= -->
    <section class="section section--mist" id="entreprise" aria-labelledby="entreprise-titre">
      <div class="container">
        <div class="about">
          <div>
            <p class="eyebrow">L'entreprise</p>
            <h2 id="entreprise-titre">Le plafond et la cloison, notre métier depuis 2007</h2>
            <!-- PROVISOIRE : à confirmer avec le client (2007, dirigée par ses deux associés) -->
            <p class="lead">Andy Construct est une entreprise genevoise spécialisée dans la pose de faux-plafonds (tendus, acoustiques, en plaques de plâtre, en fibre ou métalliques), de cloisons légères et mobiles, d'isolation thermique et phonique, ainsi que dans la peinture intérieure.</p>
            <p>Inscrite au registre du commerce depuis 2007 et dirigée par ses deux associés, elle intervient dans tout le canton de Genève et dans l'ouest vaudois pour des particuliers, des régies, des architectes, des entreprises et des collectivités publiques.</p>
            <p>Nous prenons en charge les travaux complexes : grands volumes, îlots suspendus, éclairages intégrés, puits de lumière. Notre objectif : plus de confort et un bel aspect, sans jamais sacrifier la technique.</p>
            <p class="about__sign"><b>Les associés d'Andy Construct</b>Route des Acacias 48, Carouge</p>
          </div>
          <figure>
            <span class="media">%(about_pic)s</span>
            <figcaption class="caption">%(about_cap)s</figcaption>
          </figure>
        </div>
        <ul class="figures" aria-label="Chiffres clés">
          <li><b>19 ans</b><span>d'activité, depuis 2007</span></li>
          <li><b>18</b><span>références publiques citées</span></li>
          <!-- PROVISOIRE : à valider avec le client (nombre de chantiers réalisés) -->
          <li><b>300+</b><span>chantiers réalisés</span></li>
          <li><b>2 cantons</b><span>Genève et Vaud</span></li>
        </ul>
      </div>
    </section>

    <!-- ================= PRESTATIONS ================= -->
    <section class="section" id="prestations" aria-labelledby="prestations-titre">
      <div class="container">
        <div class="section-head section-head--split">
          <div>
            <p class="eyebrow">Plafonds · Cloisons · Peinture</p>
            <h2 id="prestations-titre">Nos prestations</h2>
          </div>
          <p class="lead">Nous posons tous les types de faux-plafonds et de cloisons, et nous réalisons les finitions. Chaque système est choisi selon l'usage du local : acoustique, isolation, résistance au feu, esthétique.</p>
        </div>
        <ul class="services">%(services)s
        </ul>
        <div class="also">
          <h3 class="label">Également</h3>
          <ul>%(also)s</ul>
        </div>
        <div class="section-foot">
          <a class="btn btn--ghost" href="prestations.html">Toutes nos prestations en détail</a>
        </div>
      </div>
    </section>

    <!-- ================= RÉALISATIONS ================= -->
    <section class="section section--mist" aria-labelledby="realisations-titre">
      <div class="container">
        <div class="section-head section-head--split">
          <div>
            <p class="eyebrow">Réalisations</p>
            <h2 id="realisations-titre">Des chantiers réels, photographiés sur place</h2>
          </div>
          <p class="lead">Salles publiques, bureaux, commerces : un aperçu de nos travaux, de la pose de l'ossature à la finition. Toutes les photos proviennent de nos chantiers.</p>
        </div>
        <ul class="works">%(works)s
        </ul>
        <div class="section-foot">
          <a class="btn btn--ghost" href="realisations.html">Voir les %(nb)d photos de chantiers</a>
        </div>
      </div>
    </section>

    <!-- ================= MÉTHODE ================= -->
    <section class="section" aria-labelledby="methode-titre">
      <div class="container">
        <div class="section-head section-head--split">
          <div>
            <p class="eyebrow">Méthode</p>
            <h2 id="methode-titre">Quatre étapes, de la visite à la réception</h2>
          </div>
          <p class="lead">Une démarche simple et transparente. Vous savez à chaque étape ce qui est prévu, qui intervient et quand.</p>
        </div>
        <!-- PROVISOIRE : à valider avec le client (déroulé d'un chantier) -->
        <ol class="steps">
          <li><h3>Visite et conseil</h3><p>Nous venons voir le local, prenons les mesures et écoutons vos besoins : acoustique, isolation, éclairage, budget.</p></li>
          <li><h3>Offre détaillée</h3><p>Vous recevez une offre écrite, poste par poste et en CHF, avec la durée prévue du chantier.</p></li>
          <li><h3>Pose soignée</h3><p>Nous protégeons les lieux, respectons le planning convenu et laissons un chantier propre.</p></li>
          <li><h3>Réception des travaux</h3><p>Nous contrôlons les finitions avec vous et restons joignables après la fin du chantier.</p></li>
        </ol>
      </div>
    </section>

    <!-- ================= POURQUOI NOUS CHOISIR ================= -->
    <section class="section section--mist" aria-labelledby="engagements-titre">
      <div class="container split split--48 commit">
        <div class="commit__head">
          <p class="eyebrow">Nos engagements</p>
          <h2 id="engagements-titre">Pourquoi choisir Andy Construct</h2>
          <p class="muted">Des arguments simples, que vous pouvez vérifier.</p>
        </div>
        <ul class="commit__list">
          <!-- PROVISOIRE : à confirmer avec le client (2007) -->
          <li><h3>Une entreprise établie</h3><p>Inscrite au registre du commerce depuis 2007, avec un siège à Carouge.</p></li>
          <li><h3>Des spécialistes du plafond</h3><p>Plafonds, cloisons, isolation et finitions : c'est notre cœur de métier, pas une activité d'appoint.</p></li>
          <li><h3>Des références vérifiables</h3><p>Ville de Genève, Conservatoire, HEAD, salles communales : des maîtres d'ouvrage exigeants, cités publiquement.</p></li>
          <li><h3>Une entreprise locale</h3><p>Des chantiers dans tout le canton de Genève et dans l'ouest vaudois, de Carouge à Nyon.</p></li>
          <!-- PROVISOIRE : à valider avec le client (engagements de service formulés par l'agence) -->
          <li><h3>Une offre lisible</h3><p>Matériaux, surfaces et finitions : chaque poste est détaillé et chiffré en CHF.</p></li>
          <li><h3>Un chantier protégé</h3><p>Protection des sols et du mobilier pendant les travaux, nettoyage en fin de chantier.</p></li>
        </ul>
      </div>
    </section>

    <!-- ================= TÉMOIGNAGES ================= -->
    <section class="section" aria-labelledby="temoignages-titre">
      <div class="container">
        <div class="section-head">
          <p class="eyebrow">Témoignages</p>
          <h2 id="temoignages-titre">Ce que disent nos clients</h2>
        </div>
        <!-- PROVISOIRE : témoignages à recueillir auprès de vrais clients (textes et profils génériques, fictifs) -->
        <ul class="quotes">
          <li>
            <figure class="quote">
              <span class="quote__mark" aria-hidden="true">«</span>
              <blockquote><p>Plafond acoustique posé dans les délais, sans gêne pour les bureaux voisins. Le rendu correspond exactement aux plans.</p></blockquote>
              <figcaption><b>Architecte, Carouge</b>Plafond acoustique, bureaux</figcaption>
            </figure>
          </li>
          <li>
            <figure class="quote">
              <span class="quote__mark" aria-hidden="true">«</span>
              <blockquote><p>Un interlocuteur joignable, une offre claire et une équipe soigneuse dans un immeuble habité. Nous faisons de nouveau appel à eux.</p></blockquote>
              <figcaption><b>Régie immobilière, Genève</b>Cloisons et faux-plafonds, immeuble locatif</figcaption>
            </figure>
          </li>
          <li>
            <figure class="quote">
              <span class="quote__mark" aria-hidden="true">«</span>
              <blockquote><p>Notre plafond tendu a transformé le séjour. Pose rapide et propre, et de bons conseils pour l'éclairage.</p></blockquote>
              <figcaption><b>Propriétaire, Vésenaz</b>Plafond tendu, séjour</figcaption>
            </figure>
          </li>
        </ul>
      </div>
    </section>

    <!-- ================= ZONE D'INTERVENTION ================= -->
    <section class="section section--mist" id="zone" aria-labelledby="zone-titre">
      %(zone)s
    </section>

    <!-- ================= FAQ (brief SEO §4, texte identique au JSON-LD) ================= -->
    <section class="section" id="faq" aria-labelledby="faq-titre">
      <div class="container split split--48 faq">
        <div>
          <p class="eyebrow">Vos questions</p>
          <h2 id="faq-titre">Questions fréquentes</h2>
          <p class="muted">Une autre question ? Appelez-nous au <a href="%(tel_uri)s">%(tel)s</a>.</p>
        </div>
        <div class="faq__list">%(faq)s
        </div>
      </div>
    </section>

    <!-- ================= APPEL À L'ACTION + FORMULAIRE ================= -->
    <section class="section section--dark on-dark" id="devis" aria-labelledby="devis-titre">
      <div class="container split cta">
        <div>
          <p class="eyebrow">Contact</p>
          <h2 id="devis-titre">Demander un devis</h2>
          <p class="lead">Décrivez-nous vos travaux en quelques lignes : nous vous rappelons pour convenir d'une visite. Vous préférez en parler tout de suite ? Appelez-nous.</p>
          %(p_addr)s
          <ul class="contact-lines">
            <li class="is-main"><span class="label">Bureau</span><a href="%(tel_uri)s">%(tel)s</a></li>
            <li><span class="label">Mobile</span><a href="%(mob_uri)s">%(mob)s</a></li>
            <li><span class="label">E-mail</span><a href="mailto:%(mail)s">%(mail)s</a></li>
          </ul>
          <p class="contact-note">%(hours)s</p>
        </div>
        %(form)s
      </div>
    </section>
  </main>
''' % dict(hero_pic=pic(HERO, '100vw', eager=True, hero=True), tel_uri=TEL_URI, tel=TEL, mob_uri=MOB_URI, mob=MOB,
           mail=MAIL, hours=HOURS, p_addr=P_ADDR, refs=refs,
           about_pic=pic(ABOUT, '(min-width: 900px) 480px, 100vw', pos='58% 50%'),
           about_cap=e(BY[ABOUT]['titre']), services=services, also=also, works=works, nb=len(MANIFEST),
           zone=zone_block(), faq=faq, form=devis_form('accueil', title='Votre demande'))

    write('index.html', h + header('index.html', devis='#devis') + body + footer(devis='#devis', joined=True))
