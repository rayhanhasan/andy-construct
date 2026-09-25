# -*- coding: utf-8 -*-
"""Contact, mentions légales, 404."""
from common import *


def contact():
    title = 'Contact et devis · Genève et Suisse romande | Andy Construct'
    desc = "Contactez Andy Construct pour vos travaux de placo, peinture ou isolation en Suisse romande : +41 22 771 20 15 ou +41 78 631 14 34, du lundi au vendredi."
    h = head(title, desc, 'contact.html', ld=[page_ld('contact.html', title, 'Contact', 'ContactPage')])
    body = '''
  <main id="contenu">
%(ph)s
    <div class="section">
      <div class="container split contact-grid">
        <div>
          <section class="info-block" aria-labelledby="appeler-titre">
            <h2 id="appeler-titre" class="label">Nous appeler</h2>
            <p><span class="muted">Bureau</span><br><a class="big" href="%(tel_uri)s">%(tel)s</a></p>
            <p><span class="muted">Mobile</span><br><a class="big" href="%(mob_uri)s">%(mob)s</a></p>
            %(p_addr)s
            <p class="info-hours">%(hours)s</p>
          </section>
          <section class="info-block" aria-labelledby="adresse-titre">
            <h2 id="adresse-titre" class="label">Adresse</h2>
            %(nap)s
            <p><a class="link-arrow" href="%(maps)s" rel="noopener">Voir sur la carte</a></p>
          </section>
          <section class="info-block" aria-labelledby="preparer-titre">
            <h2 id="preparer-titre" class="label">Pour préparer votre demande</h2>
            <ul class="ticks">
              <li>La surface approximative à traiter</li>
              <li>Des plans ou quelques photos du local</li>
              <li>Le délai souhaité pour les travaux</li>
              <li>Le type de local : logement, bureau, commerce, salle…</li>
            </ul>
            <p><a class="link-arrow" href="realisations.html#references">Voir nos références</a></p>
          </section>
        </div>
        <section id="devis" aria-labelledby="ecrire-titre">
          %(form)s
        </section>
      </div>
    </div>

    <section class="section section--mist" id="zone" aria-labelledby="zone-titre">
      %(zone)s
    </section>
  </main>
''' % dict(ph=page_head('Contact', "Contact et demande d'offre",
                        "Appelez-nous, écrivez-nous ou remplissez le formulaire : nous vous répondons et convenons d'une visite si nécessaire."),
           tel_uri=TEL_URI, tel=TEL, mob_uri=MOB_URI, mob=MOB, hours=HOURS, p_addr=P_ADDR, nap=nap(), maps=MAPS,
           form=devis_form('contact', title='Nous écrire', hl='h2', title_id='ecrire-titre'), zone=zone_block())
    write('contact.html', h + header('contact.html', devis='#devis') + body + footer(devis='#devis'))


def mentions():
    title = 'Mentions légales et confidentialité | Andy Construct'
    desc = "Mentions légales et politique de confidentialité du site d'Andy Construct, Chanton & Cie, entreprise de placo, peinture et isolation à Carouge (Genève)."
    h = head(title, desc, 'mentions-legales.html', ld=[page_ld('mentions-legales.html', title, 'Mentions légales')])
    body = '''
  <main id="contenu">
%(ph)s
    <div class="section">
      <div class="container"><div class="prose">
        <h2 id="editeur">Éditeur du site</h2>
        <!-- PROVISOIRE : à valider avec le client (données relevées au registre du commerce : raison sociale, forme, associés, siège, IDE, date d'inscription) -->
        %(nap)s
        <dl>
          <dt>Raison sociale</dt><dd>%(legal)s</dd>
          <dt>Forme juridique</dt><dd>Société en nom collectif</dd>
          <dt>Associés</dt><dd>Adnan Bajrami, Caroline Chanton Bajrami</dd>
          <dt>Siège</dt><dd>%(street)s, %(city)s, Suisse</dd>
          <dt>Numéro IDE</dt><dd>%(ide)s</dd>
          <dt>Registre du commerce</dt><dd>Canton de Genève, inscription depuis 2007</dd>
          <dt>Téléphone</dt><dd><a href="%(tel_uri)s">%(tel)s</a></dd>
          <dt>E-mail</dt><dd><a href="mailto:%(mail)s">%(mail)s</a></dd>
        </dl>

        <h2 id="hebergement">Hébergement</h2>
        <!-- PROVISOIRE : à valider avec le client (compléter le nom et l'adresse de l'hébergeur de production) -->
        <p>Le site est hébergé en Suisse. Conception et réalisation : Harbor Digital.</p>

        <h2 id="propriete">Propriété intellectuelle et crédits photos</h2>
        <p>Les textes, le logo et les photos de chantiers publiés sur ce site appartiennent à %(legal)s. Toute reproduction demande son accord écrit. Les noms des clients cités en référence restent la propriété de leurs titulaires ; aucun logo de client n'est reproduit.</p>
        <p>Polices de caractères : Montserrat et Source Sans 3, sous licence SIL Open Font License, hébergées sur ce site. Fond de la carte « Zone d'intervention » : limites cantonales de swisstopo et de l'Office fédéral de la statistique, via le paquet swiss-maps (Interactive Things, licence BSD).</p>

        <h2 id="donnees">Protection des données (nLPD)</h2>
        <p>Nous traitons vos données personnelles conformément à la loi fédérale sur la protection des données (nLPD).</p>
        <h3>Responsable du traitement</h3>
        <p>%(legal)s, %(street)s, %(city)s. Contact : <a href="mailto:%(mail)s">%(mail)s</a>.</p>
        <h3>Données collectées par le formulaire</h3>
        <p>Nom et prénom, téléphone, e-mail, commune du chantier, type de travaux, message et, le cas échéant, la photo ou le plan que vous joignez.</p>
        <h3>Finalité</h3>
        <p>Répondre à votre demande, organiser une visite et établir une offre. Vos données ne sont ni vendues ni utilisées à des fins publicitaires.</p>
        <!-- PROVISOIRE : à valider avec le client (durée de conservation, lieu d'hébergement et messagerie) -->
        <h3>Durée de conservation</h3>
        <p>Au maximum 12 mois si votre demande n'aboutit pas à un contrat. En cas de contrat, pendant la durée légale de conservation des pièces commerciales.</p>
        <h3>Destinataires</h3>
        <p>L'hébergeur du site et le fournisseur de messagerie de l'entreprise, uniquement pour assurer ces services. Les données sont traitées en Suisse.</p>
        <h3>Vos droits</h3>
        <p>Vous pouvez demander l'accès à vos données, leur rectification ou leur effacement en écrivant à <a href="mailto:%(mail)s">%(mail)s</a>. Vous pouvez aussi vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT).</p>

        <h2 id="cookies">Cookies et mesure d'audience</h2>
        <p>Ce site ne dépose aucun cookie et n'utilise aucun outil de mesure d'audience. Aucune police ni ressource n'est chargée depuis un serveur tiers.</p>
        <!-- MAQUETTE : le bandeau de présentation mémorise sa fermeture dans le stockage de session du navigateur ; il disparaît en production. -->
        <p>Les liens « Voir sur la carte » (Google Maps) et Facebook ouvrent des sites tiers, soumis à leur propre politique de confidentialité.</p>
        <p class="muted">Dernière mise à jour : 25 septembre 2026.</p>
      </div></div>
    </div>
  </main>
''' % dict(ph=page_head('Mentions légales', 'Mentions légales et protection des données',
                        "Qui édite ce site, comment nous joindre et comment nous traitons les données que vous nous transmettez."),
           nap=nap('nap nap--page'), legal=LEGAL, street=STREET, city=CITY, ide=IDE, tel=TEL, tel_uri=TEL_URI, mail=MAIL)
    write('mentions-legales.html', h + header('') + body + footer())


def notfound():
    title = 'Page introuvable | Andy Construct'
    h = head(title, "Cette page n'existe pas ou a été déplacée. Retrouvez nos prestations, nos réalisations et nos coordonnées.",
             '404.html', canonical=False)
    h = h.replace('<head>\n', '<head>\n  <!-- Chemins relatifs : si l\'hébergeur sert cette page pour des adresses situées dans des sous-dossiers,\n       ajouter <base href="/res/andy-construct/"> (maquette) ou <base href="/"> (production). -->\n', 1)
    body = '''
  <main id="contenu">
    <section class="notfound" aria-labelledby="titre-page">
      <div class="container">
        <p class="notfound__code" aria-hidden="true">404</p>
        <h1 id="titre-page">Cette page est introuvable</h1>
        <p class="lead">L'adresse a peut-être changé depuis la refonte du site. Voici les pages principales :</p>
        <ul>
          <li><a href="index.html">Accueil</a></li>
          <li><a href="prestations.html">Nos prestations</a></li>
          <li><a href="realisations.html">Réalisations et références</a></li>
          <li><a href="contact.html">Contact et demande d'offre</a></li>
        </ul>
        <p class="notfound__call">Vous pouvez aussi nous appeler au <a href="%s">%s</a>.</p>
      </div>
    </section>
  </main>
''' % (TEL_URI, TEL)
    write('404.html', h + header('') + body + footer())


def build():
    contact()
    mentions()
    notfound()
