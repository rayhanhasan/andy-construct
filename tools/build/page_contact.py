# -*- coding: utf-8 -*-
"""Contact (architecture §4.6, copy deck §J) : téléphones, formulaire, rappel, zone d'intervention."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, page_head, ld_page, TEL, TEL_URI, MOB, tel_link, mob_label, horaires, mail_html, nap, MAPS)
import composants as c
from carte import carte_svg


def build():
    p = dict(fichier='contact.html', formulaire=True, title='Contact et demande de devis, Genève | Andy Construct',
             desc='Demandez un devis en trois étapes ou appelez le +41 22 771 20 15, du lundi au vendredi. Route des Acacias 48, Carouge. Toute la Suisse romande.')
    p['ld'] = [ld_page('contact.html', p['title'], 'Contact', typ='ContactPage', extra={'about': {'@id': PROD + '#entreprise'}})]
    corps = page_head('Contact', 'Contact et demande de devis',
                      'Appelez-nous, laissez votre numéro, ou décrivez vos travaux en trois étapes.')

    h = horaires()
    rdv = T('C29', '<p>Sur rendez-vous.</p>', '')
    appeler = '''<div class="info-block" data-suivi-zone="contact">
            <h2>Nous appeler</h2>
            <p class="info-line"><span>Bureau</span>%s</p>
            <p class="info-line"><span>%s</span>%s</p>
            %s
            <p class="muted">%s</p>
          </div>''' % (tel_link(cls='big'), mob_label(), tel_link(cls='big', numero='mobile'),
                       ('<p class="info-hours">%s</p>' % T('C03', 'Du lundi au vendredi, de 7 h à 18 h.')) if definitif('C03') else '',
                       T('C01 C03', 'Pas de réponse ? Laissez un message avec votre numéro : nous rappelons le jour même ou le jour ouvrable suivant.',
                         'Pas de réponse ? Laissez un message avec votre numéro : nous vous rappelons.'))
    reste = '''<div class="info-block" data-suivi-zone="contact">
            <h2>Nous écrire</h2>
            <p>%s</p>
          </div>
          <div class="info-block" data-suivi-zone="contact">
            <h2>Nous trouver</h2>
            <address>Andy Construct<br>Route des Acacias 48<br>1227 Carouge (Genève)</address>
            %s
            <p><a class="link-arrow" href="%s" rel="noopener">Voir sur la carte</a></p>
          </div>
          <div class="info-block">
            <h2>Pour préparer votre demande</h2>
            <ul class="ticks">
              <li>La surface approximative à traiter</li>
              <li>Quelques photos, ou des plans si vous en avez</li>
              <li>Le délai souhaité</li>
              <li>Le type de local : logement, bureau, commerce, salle</li>
              <li>Si les lieux seront habités pendant les travaux</li>
            </ul>
          </div>
          %s''' % (mail_html(cls='big big--mail', emplacement='contact'), rdv, MAPS, c.refs_ligne())

    corps += '''    <section class="section section--top contact" aria-label="Nous joindre">
      <div class="container contact__grid">
        <div class="contact__appel">
          %s
        </div>
        <div class="contact__forms" data-suivi-zone="bloc_demande">
          <div class="form-card" id="demande">
            <h2 id="demande-titre">Demander un devis</h2>
            <p class="lead">3 étapes, environ une minute. Nous vous rappelons pour convenir d'une visite.</p>
            %s
          </div>
          <div class="form-card form-card--rappel">
            %s
          </div>
        </div>
        <div class="contact__reste">
          %s
        </div>
      </div>
    </section>
''' % (appeler, c.form_devis('contact-devis'), c.module_rappel('contact-rappel', niveau='h2'), reste)

    villes = T('C21', 'Carouge (siège), Genève, Nyon, Lausanne, Yverdon-les-Bains, Neuchâtel, Fribourg, Sion, Delémont, Bienne.',
               'Carouge (siège), Genève, Nyon, Lausanne, Yverdon-les-Bains, Neuchâtel, Fribourg, Sion, Delémont, Bienne.')
    corps += '''    <section class="section section--mist" id="zone" aria-labelledby="zone-titre">
      <div class="container split">
        <div>
          <h2 id="zone-titre">Nous intervenons dans toute la Suisse romande</h2>
          <p class="lead">Depuis notre siège de Carouge : cantons de Genève, Vaud, Neuchâtel, Fribourg et Jura, Valais romand et Jura bernois.</p>
          <ul class="cantons"><li>Genève</li><li>Vaud</li><li>Neuchâtel</li><li>Fribourg</li><li>Valais romand</li><li>Jura</li><li>Jura bernois</li></ul>
          <p><b>Villes marquées sur la carte :</b> %s</p>
          <p>Votre commune n'est pas dans la liste ? Appelez-nous : %s.</p>
        </div>
        <figure class="carte">
          %s
          <figcaption>Toute la Suisse romande. Siège à Carouge. Fond de carte : swisstopo.</figcaption>
        </figure>
      </div>
    </section>
''' % (villes, tel_link(emplacement='zone'), carte_svg())
    page(p, corps)
