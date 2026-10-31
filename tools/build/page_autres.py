# -*- coding: utf-8 -*-
"""Merci, mentions légales, confidentialité, 404 et redirection de l'ancienne page Prestations."""
import os
import ctx
from ctx import e, T, V, definitif, marque, PROD
from common import (page, page_head, ld_page, TEL, TEL_URI, MOB, tel_link, horaires, mail, mail_html, LEGAL, IDE, ZEFIX,
                    svc_nom, svc_url, SERVICES, AUJOURDHUI, ASSETS)
import portfolio as pf

MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
DATE = '%d %s %d' % (AUJOURDHUI.day, MOIS[AUJOURDHUI.month - 1], AUJOURDHUI.year)


def merci():
    p = dict(fichier='merci.html', index=False, sans_devis=True, title='Demande bien reçue | Andy Construct',
             desc='Votre demande est bien arrivée. Voici ce qui va se passer et comment préparer la visite.')
    urgence = 'Une question urgente ? Appelez le %s%s.' % (tel_link(emplacement='merci'), T('C03', ', du lundi au vendredi, de 7 h à 18 h', ''))
    # Filtres disponibles (le lien « voir nos réalisations en … » ne mène jamais à un filtre vide)
    filtres = [s for s in SERVICES if any(pf.proj_ok(x) and s in pf.proj_tags(x) for x in pf.PROJETS)
               or any(s in pf.paire_services(x[0]) for x in pf.PAIRES)]
    noms = {s: ctx.fr(svc_nom(s, html=False)).lower() for s in SERVICES}
    corps = '''    <section class="section merci" data-suivi-zone="merci" data-filtres="%(filtres)s" data-noms="%(noms)s">
      <div class="container narrow">
        <div data-variante="devis">
          <h1 id="titre-page">Merci, votre demande est bien arrivée</h1>
          <p class="merci__ref" hidden>Référence de votre demande : <b data-ref></b></p>
          <div class="merci__recap" hidden>
            <p>Vous nous avez demandé un devis pour : <b data-travaux></b><span data-commune-bloc>, à <b data-commune></b></span>.</p>
            <p data-pref-bloc>Vous préférez être recontacté(e) : <b data-pref></b>.</p>
          </div>
          <h2>Et maintenant ?</h2>
          <ol class="merci__etapes">
            <li>%(e1)s</li>
            <li>%(e2)s</li>
            <li>%(e3)s</li>
          </ol>
          <p class="merci__mail" data-si-email hidden>Un e-mail de confirmation vient de partir. Vous ne le voyez pas ? Regardez dans le dossier des courriers indésirables.</p>
          <h2>Pour gagner du temps à la visite</h2>
          <ul class="ticks">
            <li>Quelques photos des pièces concernées</li>
            <li>Les dimensions approximatives</li>
            <li>Les plans, si vous en avez</li>
            <li>La date à laquelle les travaux doivent être finis</li>
          </ul>
          <p><a class="link-arrow" href="realisations.html" data-lien-service>En attendant, voir nos réalisations</a></p>
          <p class="merci__urgence">%(urgence)s</p>
        </div>
        <div data-variante="rappel" hidden>
          <h1>Merci, nous vous rappelons</h1>
          <p class="merci__ref" hidden>Référence : <b data-ref></b></p>
          <p class="lead">%(rappel)s</p>
          <p>Pour gagner du temps, notez la surface approximative, le délai souhaité et, si possible, prenez quelques photos.</p>
          <p><a class="link-arrow" href="realisations.html">En attendant, voir nos réalisations</a></p>
          <p class="merci__urgence">Une question urgente ? %(tel)s</p>
        </div>
      </div>
    </section>
''' % dict(filtres=' '.join(filtres), noms=e('|'.join('%s=%s' % (s, noms[s]) for s in SERVICES)),
           e1=T('C01', 'Nous vous rappelons le jour même ou le jour ouvrable suivant, depuis le +41 22 771 20 15.',
                'Nous vous rappelons pendant nos heures de bureau, depuis le +41 22 771 20 15.'),
           e2=T('C41', 'Ensemble, nous convenons d\'une visite, en général dans la semaine.', 'Ensemble, nous convenons d\'une date de visite.'),
           e3=T('C08', 'Vous recevez ensuite notre offre écrite.', 'Vous recevez ensuite notre offre écrite.'),
           urgence=urgence,
           rappel=T('C01', 'Nous vous rappelons<span data-creneau></span>, le jour même ou le jour ouvrable suivant, depuis le +41 22 771 20 15.',
                    'Nous vous rappelons pendant nos heures de bureau, depuis le +41 22 771 20 15.'),
           tel=tel_link(emplacement='merci'))
    page(p, corps)


def mentions():
    p = dict(fichier='mentions-legales.html', title='Mentions légales | Andy Construct',
             desc='Mentions légales du site andyconstruct.ch : éditeur Andy Construct, Chanton & Cie à Carouge, IDE CHE-113.706.162, hébergement et crédits.')
    p['ld'] = [ld_page('mentions-legales.html', p['title'], 'Mentions légales')]
    lignes = [('Raison sociale', LEGAL), ('Forme juridique', 'société en nom collectif')]
    if definitif('C10'):
        lignes.append(('Associés', T('C10', 'Adnan Bajrami, Caroline Chanton Bajrami')))
    lignes += [('Siège', 'Route des Acacias 48, 1227 Carouge (Genève), Suisse'),
               ('Numéro IDE', '%s · Registre du commerce du canton de Genève, inscription en 2007' % IDE)]
    if definitif('C35'):
        lignes.append(('Numéro TVA', T('C35', 'CHE-113.706.162 TVA')))
    lignes += [('Téléphone', tel_link()), ('E-mail', mail_html())]
    corps = page_head('Mentions légales', 'Mentions légales', 'Qui édite ce site, qui l\'héberge et à qui appartiennent ses contenus.')
    corps += '''    <section class="section">
      <div class="container prose">
        <h2>Éditeur du site</h2>
        <dl>%(lignes)s</dl>
        <h2>Hébergement</h2>
        <p>%(heberg)s</p>
        <p>Conception et réalisation : Harbor Digital.</p>
        <h2>Propriété des contenus</h2>
        <p>Les textes, le logo et les photos de chantiers publiés sur ce site appartiennent à Andy Construct, Chanton & Cie. Leur reproduction demande un accord écrit.</p>
        %(photos)s
        <h2>Références citées</h2>
        <p>Les noms des maîtres d'ouvrage cités sur ce site indiquent des travaux réalisés pour eux. Ils ne signifient ni partenariat ni recommandation. Les logos sont reproduits avec l'accord écrit de leurs titulaires ; les armoiries publiques et les emblèmes d'organisations internationales ne sont jamais reproduits.</p>
        <h2>Informations et prix</h2>
        <p>Les informations de ce site sont générales. Elles ne remplacent pas une visite ni un conseil adapté à votre situation. Les prix indicatifs éventuels ne constituent pas une offre : seule l'offre écrite remise après la visite engage l'entreprise.</p>
        <h2>Liens vers d'autres sites</h2>
        <p>Les liens vers des sites tiers (carte, registre du commerce, réseaux sociaux) ouvrent des sites soumis à leurs propres conditions et à leur propre politique de confidentialité.</p>
        <h2>Crédits</h2>
        <p>Polices de caractères : Montserrat et Source Sans 3, sous licence SIL Open Font License, hébergées sur ce site. Carte de la zone d'intervention : limites cantonales de swisstopo et de l'Office fédéral de la statistique, via le paquet swiss-maps (Interactive Things, licence BSD).</p>
        <h2 id="donnees">Protection des données</h2>
        <p>La façon dont nous traitons les données transmises par le formulaire et les statistiques du site est décrite dans notre politique de confidentialité. <a href="confidentialite.html">Lire la politique de confidentialité</a></p>
        <h2>Droit applicable</h2>
        <p>Ce site et son utilisation sont soumis au droit suisse.</p>
        <p class="maj">Dernière mise à jour : %(date)s</p>
      </div>
    </section>
''' % dict(lignes=''.join('<dt>%s</dt><dd>%s</dd>' % x for x in lignes),
           heberg=T('C34', 'Le site est hébergé en Suisse.', 'Le site est hébergé en Suisse.'),
           photos=T('C25', '<p>Les photos montrent des chantiers réalisés par l\'entreprise. Les personnes et les lieux reconnaissables sont publiés avec l\'accord des intéressés.</p>', ''),
           date=DATE)
    page(p, corps)


def confidentialite():
    """Politique de confidentialité : titre, meta, H1 et chapeau du copy deck §M. Le corps est un projet factuel
    (sources : site/api, strategie-acquisition.md §9.1), à faire relire par le juriste (V02)."""
    p = dict(fichier='confidentialite.html', title='Protection des données | Andy Construct',
             desc='Comment Andy Construct traite les données du formulaire et des statistiques du site : finalités, durées, prestataires et vos droits.')
    p['ld'] = [ld_page('confidentialite.html', p['title'], 'Protection des données')]
    umami = bool(ctx.CONFIG.get('umami_src') and ctx.CONFIG.get('umami_id'))
    stats = ('<p>Nous mesurons la fréquentation du site avec Umami, un outil sans cookie, hébergé en Suisse. Il compte les pages vues et les clics sur les boutons (par exemple « Appeler »), sans enregistrer votre adresse IP complète ni ce que vous écrivez dans les formulaires. Si votre navigateur envoie le signal « Ne pas me suivre » (Do Not Track ou GPC), aucune mesure n\'est faite.</p>'
             if umami else '<p>Le site ne mesure pas sa fréquentation et ne dépose aucun cookie.</p>')
    corps = page_head('Protection des données', 'Protection des données',
                      'Ce que nous faisons des informations que vous nous transmettez, combien de temps nous les gardons, et comment exercer vos droits.')
    texte = '''<h2>Qui est responsable de vos données ?</h2>
        <p>Andy Construct, Chanton & Cie, Route des Acacias 48, 1227 Carouge (Genève), IDE CHE-113.706.162. Pour toute question : %(mail)s ou %(tel)s.</p>
        <h2>Ce que nous recevons quand vous remplissez un formulaire</h2>
        <p>Les informations que vous saisissez : les travaux, qui vous êtes (propriétaire, régie…), la commune, le délai et la surface, vos nom et coordonnées, votre message, les photos ou plans joints et la façon dont vous nous avez connus. Le formulaire transmet aussi la page d'où vous l'envoyez et, si vous êtes arrivé par un lien de campagne, le nom de cette campagne. Aucun de ces champs n'est obligatoire, sauf ceux qui sont indiqués.</p>
        <h2>Elles servent à traiter votre demande, et à rien d'autre</h2>
        <p>Nous les utilisons pour vous rappeler, convenir d'une visite, établir l'offre écrite et en assurer le suivi. Nous ne les vendons pas et ne les utilisons pas pour de la publicité.</p>
        <p>Pour rappeler d'abord les demandes les plus urgentes, un calcul automatique classe les demandes selon le délai, la surface et le type de travaux. Toutes les demandes sont rappelées, et c'est toujours une personne qui décide.</p>
        <h2>Qui y a accès ?</h2>
        <p>Les associés d'Andy Construct, et les prestataires techniques qui hébergent le site, la messagerie et l'outil de suivi des demandes. Ils sont liés par contrat et traitent les données en Suisse ou dans l'Union européenne. Aucune donnée n'est transmise à un tiers sans que nous vous le disions.</p>
        <h2>Combien de temps nous les gardons</h2>
        <ul>
          <li>Photos et plans envoyés par le formulaire : 30 jours sur le serveur du site, puis seulement dans le dossier de votre demande.</li>
          <li>Demande sans suite : 24 mois après notre dernier échange, puis effacement.</li>
          <li>Client : les pièces comptables et contractuelles 10 ans, comme la loi l'exige.</li>
          <li>Journaux techniques du serveur : 30 jours.</li>
        </ul>
        <h2>Statistiques de visite</h2>
        %(stats)s
        <p>Votre navigateur garde aussi, le temps de la visite, le brouillon du formulaire (pour ne rien perdre si la page se recharge) et la page par laquelle vous êtes arrivé. Ces informations s'effacent quand vous fermez l'onglet.</p>
        <h2>Vos droits</h2>
        <p>Vous pouvez demander à consulter, corriger ou effacer vos données, par e-mail à %(mail)s. Nous répondons dans les 30 jours. Vous pouvez aussi vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT).</p>
        <h2>Sécurité</h2>
        <p>Le site fonctionne en connexion chiffrée (HTTPS). Seules les personnes qui traitent votre demande y ont accès.</p>
        <p class="maj">Dernière mise à jour : %(date)s</p>''' % dict(mail=mail_html(), tel=tel_link(), stats=stats, date=DATE)
    corps += '''    <section class="section">
      <div class="container prose">
        %s
      </div>
    </section>
''' % marque('V02', texte, bloc=True)
    page(p, corps)


def page_404():
    p = dict(fichier='404.html', index=False, base=ctx.prod(), canonical=False, title='Page introuvable | Andy Construct',
             desc='Cette page n\'existe pas ou a été déplacée. Retrouvez nos prestations, nos réalisations et notre numéro de téléphone.')
    h = T('C03', ', du lundi au vendredi, de 7 h à 18 h', '')
    liens = [('placo.html', 'Placo : cloisons, doublages, faux-plafonds'), ('peinture.html', 'Peinture intérieure'),
             ('isolation-acoustique.html', 'Isolation acoustique'), ('cloisons-isothermes.html', svc_nom('cloisons-isothermes')),
             ('realisations.html', 'Nos réalisations'), ('contact.html', 'Contact et demande de devis')]
    corps = '''    <section class="section notfound" data-suivi-zone="404">
      <div class="container">
        <p class="notfound__code" aria-hidden="true">404</p>
        <h1 id="titre-page">Cette page n'existe pas, ou elle a changé d'adresse</h1>
        <p class="lead">Notre site a été refait : certaines adresses ont changé. Voici les pages les plus consultées :</p>
        <ul>%s</ul>
        <p class="notfound__call">Vous pouvez aussi nous appeler : %s%s.</p>
        <p><a class="btn" href="index.html">Retour à l'accueil</a></p>
      </div>
    </section>
''' % (''.join('<li><a href="%s">%s</a></li>' % x for x in liens), tel_link(emplacement='404'), h)
    page(p, corps)


def prestations_redirection():
    """L'ancienne page de la maquette : redirection vers l'accueil (le .htaccess envoie une 301 sur Apache)."""
    doc = '''<!DOCTYPE html>
<html lang="fr-CH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prestations | Andy Construct</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="%s">
  <meta http-equiv="refresh" content="0; url=index.html">
  <link rel="stylesheet" href="%s">
</head>
<body>
  <main class="container section">
    <h1>Cette page a changé d'adresse</h1>
    <p>Chacune de nos prestations a maintenant sa page :</p>
    <ul>%s</ul>
    <p><a href="index.html">Retour à l'accueil</a></p>
  </main>
</body>
</html>
''' % (PROD, ASSETS['css'], ''.join('<li><a href="%s">%s</a></li>' % (svc_url(s), ctx.fr(svc_nom(s, html=False))) for s in SERVICES))
    with open(os.path.join(ctx.OUT, 'prestations.html'), 'w', encoding='utf-8') as f:
        f.write(doc)


def build():
    merci()
    mentions()
    confidentialite()
    page_404()
    prestations_redirection()
