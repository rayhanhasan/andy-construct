# -*- coding: utf-8 -*-
"""Contact v3 (cro-v3 §6.5, §7) : en-tête sombre (téléphone d'abord), formulaire en 3 étapes avec, à côté, badges,
logos des références, rappel, coordonnées ; zone d'intervention."""
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, hero_page, ld_page, TEL, TEL_URI, MOB, tel_link, mob_label, horaires, mail_html, MAPS)
import composants as c
from carte import carte_svg


def build():
    p = dict(fichier='contact.html', formulaire=True, title='Contact et demande de devis, Genève | Andy Construct',
             desc='Demandez un devis en trois étapes ou appelez le +41 22 771 20 15, du lundi au vendredi. Route des Acacias 48, Carouge. Toute la Suisse romande.')
    p['ld'] = [ld_page('contact.html', p['title'], 'Contact', typ='ContactPage', extra={'about': {'@id': PROD + '#entreprise'}})]

    h = horaires()
    actions = ('<a class="btn" href="%s" data-suivi-numero="fixe" data-suivi-emplacement="entete_page">Appeler le %s</a>'
               '<a class="btn btn--light" href="#demande">Décrire mes travaux</a>' % (TEL_URI, TEL))
    note = '<p class="hero__note">%s%s</p>' % (h + '. ' if h else '', '%s : %s' % (mob_label(), tel_link(numero='mobile', emplacement='entete_page')))
    corps = hero_page('Contact', 'Contact et demande de devis',
                      'Appelez-nous, laissez votre numéro, ou décrivez vos travaux en <b>trois étapes</b>.',
                      actions=actions, extra='', badges=note, cls='hero--contact')

    rdv = T('C29', ' Sur rendez-vous.', '')
    aside = '''<div class="contact__aside">
          %(badges)s
          %(refs)s
          <details class="rappel-repli" data-entree-demande><summary>Vous préférez qu'on vous rappelle ?</summary>%(rappel)s</details>
          <div class="contact__coord" data-suivi-zone="contact">
            <h2>Nous écrire, nous trouver</h2>
            <p>%(mail)s</p>
            <address>Andy Construct, Route des Acacias 48<br>1227 Carouge (Genève).%(rdv)s</address>
            <p><a class="link-arrow" href="%(maps)s" rel="noopener">Voir sur la carte</a></p>
            <p class="muted">%(rappel_txt)s</p>
          </div>
        </div>''' % dict(
        badges=c.badges(['B1', 'B3', '|B9|B4'], cls='badges--clair badges--col', label='Garanties'),
        refs=c.refs_ligne('refs-line--aside'), rappel=c.module_rappel('rappel-colonne', niveau='h3'),
        mail=mail_html(cls='big big--mail', emplacement='contact'), rdv=rdv, maps=MAPS,
        rappel_txt=T('C01 C03', 'Pas de réponse au téléphone ? Laissez un message : nous rappelons le jour même ou le jour ouvrable suivant.',
                     'Pas de réponse au téléphone ? Laissez un message avec votre numéro : nous vous rappelons.'))

    corps += '''    <section class="section section--mist contact" aria-labelledby="demande-titre">
      <div class="container contact__grid">
        <div class="form-card" id="demande" data-suivi-zone="bloc_demande">
          <h2 id="demande-titre">Demander un devis</h2>
          <p class="lead"><b>3 étapes</b>, environ <b>une minute</b>.</p>
          %s
        </div>
        %s
      </div>
    </section>
''' % (c.form_devis('contact'), aside)

    villes = ['Carouge (siège)', 'Genève', 'Nyon', 'Lausanne', 'Yverdon-les-Bains', 'Neuchâtel', 'Fribourg', 'Sion', 'Delémont', 'Bienne']
    villes_html = marque('C21', '<ul class="villes">%s</ul>' % ''.join('<li>%s</li>' % c.insec(v) for v in villes), bloc=True)
    corps += '''    <section class="section" id="zone" aria-labelledby="zone-titre">
      <div class="container split">
        <div>
          <h2 id="zone-titre">Toute la Suisse romande</h2>
          <span class="laser laser--court" aria-hidden="true"></span>
          <p class="lead">Depuis Carouge, dans toute la Suisse romande.</p>
          <ul class="cantons"><li>Genève</li><li>Vaud</li><li>Neuchâtel</li><li>Fribourg</li><li>Valais romand</li><li>Jura</li><li>Jura bernois</li></ul>
          <h3 class="villes__titre">Villes marquées sur la carte</h3>
          %s
          <p>Votre commune n'est pas dans la liste ? Appelez-nous : %s.</p>
        </div>
        <figure class="carte">
          %s
          <figcaption>Toute la Suisse romande. Siège à Carouge. Fond de carte : swisstopo.</figcaption>
        </figure>
      </div>
    </section>
''' % (villes_html, tel_link(emplacement='zone'), carte_svg())
    page(p, corps)
