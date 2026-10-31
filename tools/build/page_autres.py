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


def heberg_ligne():
    """C34 : nom, adresse et pays de l'hébergeur à fournir ; repli : ligne masquée (jamais « en Suisse » sans confirmation)."""
    nom = (ctx.CONF.get('C34') or {}).get('note', '').strip()
    if nom and definitif('C34'):
        return '<p>Le site est hébergé par %s.</p>' % e(nom)
    ctx.M('C34')
    return ''


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
        %(heberg)s<p>Conception et réalisation : Harbor Digital.</p>
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
           heberg=heberg_ligne(),
           photos=T('C25', '<p>Les photos montrent des chantiers réalisés par l\'entreprise. Les personnes et les lieux reconnaissables sont publiés avec l\'accord des intéressés.</p>', ''),
           date=DATE)
    page(p, corps)


def confidentialite():
    """Politique de confidentialité : titre, meta, H1 et chapeau du copy deck §M ; texte relu par le juriste
    (docs/v2/automatisation.md §9). Les éléments encore inconnus (hébergeur C34, messagerie, e-mail C30) sont marqués
    en vérification et jamais inventés ; le paragraphe des statistiques suit la configuration Umami."""
    p = dict(fichier='confidentialite.html', title='Protection des données | Andy Construct',
             desc='Comment Andy Construct traite les données du formulaire et des statistiques du site : finalités, durées, prestataires et vos droits.')
    p['ld'] = [ld_page('confidentialite.html', p['title'], 'Protection des données')]
    umami = bool(ctx.CONFIG.get('umami_src') and ctx.CONFIG.get('umami_id'))
    if umami:
        stats = ('<p>Notre site n\'utilise <strong>aucun cookie</strong>. Nous mesurons l\'audience avec Umami, installé sur un serveur que nous louons en Suisse (Infomaniak). '
                 'Il compte les pages vues et les clics sur le téléphone ou les boutons, et note le site d\'où vous venez, le type d\'appareil et de navigateur, et le pays ou la région. '
                 'Il ne vous identifie pas et ne conserve pas votre adresse IP. Ce que vous tapez dans les formulaires ne lui est jamais envoyé. Ces statistiques sont gardées %s.</p>'
                 % marque('V02', '24 mois'))
    else:
        stats = '<p>Notre site n\'utilise <strong>aucun cookie</strong> et ne mesure pas son audience.</p>'
    nom_heb = (ctx.CONF.get('C34') or {}).get('note', '').strip()
    heberg = e(nom_heb) if (nom_heb and definitif('C34')) else marque('C34', 'l\'hébergeur du site')
    if not (nom_heb and definitif('C34')):
        ctx.M('C34')
    corps = page_head('Protection des données', 'Protection des données',
                      'Ce que nous faisons des informations que vous nous transmettez, combien de temps nous les gardons, et comment exercer vos droits.')
    texte = """<h2>Qui est responsable</h2>
        <p>Andy Construct, Chanton & Cie, société en nom collectif, Route des Acacias 48, 1227 Carouge, IDE CHE-113.706.162. Pour toute question sur vos données : %(mail)s ou %(tel)s.</p>
        <h2>Ce que nous recevons quand vous nous écrivez</h2>
        <p>Quand vous demandez un devis ou un rappel, nous recevons ce que vous saisissez : votre nom (et votre civilité si vous l'indiquez), votre numéro de téléphone ou votre adresse e-mail, la commune des travaux, le type de travaux, votre situation (propriétaire, régie, architecte…), la surface et le délai, votre préférence de contact, votre message et les photos ou plans que vous joignez. Si vous nous dites comment vous nous avez connus, ou qui vous a recommandé Andy Construct, nous le recevons aussi.</p>
        <p>Le formulaire nous transmet aussi, pour savoir comment notre site est trouvé : la page d'où vous l'envoyez, la page par laquelle vous êtes arrivé(e), le site d'où vous veniez (un moteur de recherche, par exemple) et, le cas échéant, le nom de la campagne publicitaire (paramètres « utm »).</p>
        <h2>À quoi elles servent</h2>
        <p>Ces informations servent à traiter votre demande : vous rappeler, convenir d'une visite, vous remettre une offre et, si vous nous confiez les travaux, organiser et suivre le chantier. La provenance de votre visite nous sert aussi à compter, sans vous nommer, les pages et les campagnes qui amènent des demandes. Le nom de la personne qui vous a recommandé(e) sert uniquement à la remercier.</p>
        <p>Nous ne vendons pas vos données et nous ne les utilisons pas pour de la publicité. Seule exception : si vous devenez client et que nous vous en avons informé(e) à la commande, nous pouvons vous écrire au sujet de prestations semblables (voir « Après un chantier »).</p>
        <h2>Comment nous traitons votre demande</h2>
        <p>Pour rappeler chacun dans un délai raisonnable, nous classons les demandes par ordre de priorité, selon les informations de la demande (type de travaux et de client, ampleur, lieu, délai, provenance). <strong>Toutes les demandes sont rappelées</strong> et c'est toujours une personne qui décide de la suite.</p>
        <p>Vous recevez un e-mail de confirmation si vous avez donné votre adresse, ou un SMS si vous n'avez laissé qu'un numéro de portable. Si nous n'arrivons pas à vous joindre, nous vous l'écrivons ; après trois essais sans réponse, nous classons la demande et ne vous relançons plus.</p>
        <p>Après l'envoi d'une offre, nous pouvons vous écrire ou vous appeler au plus trois fois en trois semaines, pour savoir si vous avez des questions. Une simple réponse arrête ces messages. Si vous nous dites que votre projet est reporté et que nous pouvons vous recontacter, nous vous écrivons une seule fois, environ six mois plus tard.</p>
        <h2>Le guide imprimé et les conseils par e-mail</h2>
        <p>Nos guides se téléchargent librement, sans inscription. Si vous demandez la version imprimée, nous utilisons votre nom et votre adresse postale uniquement pour vous l'envoyer. Si vous donnez votre e-mail, vous recevez une confirmation. Si vous avez coché la case prévue, nous vous envoyons aussi deux e-mails de conseils sur le même sujet, puis plus rien. Chaque e-mail contient un lien pour vous désinscrire ; vous pouvez aussi répondre « STOP ».</p>
        <h2>Après un chantier</h2>
        <p>Une fois le chantier terminé, nous vous demandons votre avis, par e-mail (et par SMS pour les particuliers), avec une seule relance au plus. Nous le demandons à tous nos clients, sans tri et sans contrepartie. Nous vous demandons aussi si nous pouvons montrer des photos de votre chantier : nous ne publions rien sans votre accord, et vous pouvez le retirer à tout moment.</p>
        <p>Si nous vous avons informé(e) de ce droit au moment de la commande, nous pouvons vous écrire de temps en temps au sujet de prestations semblables, par exemple pour faire le point un an après les travaux. Vous pouvez vous y opposer à tout moment, gratuitement, en répondant « STOP » ou par le lien en bas de chaque message.</p>
        <h2>Si vous êtes un professionnel que nous contactons</h2>
        <p>Nous écrivons et téléphonons à des régies, des bureaux d'architectes, des communes et des entreprises pour présenter notre travail. Nous utilisons alors le nom, la fonction et les coordonnées professionnelles (adresse, téléphone) d'une personne de contact, trouvés dans un annuaire public ou sur le site de son organisation, et nos notes sur la suite donnée. Nous n'envoyons pas d'e-mail publicitaire sans votre accord et nous respectons l'astérisque de l'annuaire. Sur simple demande, nous ne vous contactons plus. Sans suite de votre part, ces données sont effacées après 24 mois.</p>
        <h2>Qui d'autre voit vos données</h2>
        <p>Seuls les associés d'Andy Construct et notre agence web (Harbor Digital, pour la mise en place et la maintenance) y ont accès. Nous faisons appel à des prestataires techniques, liés par un contrat de protection des données :</p>
        <ul>
          <li>%(heberg)s, pour le site et la réception du formulaire ;</li>
          <li>%(messagerie)s, pour nos e-mails ;</li>
          <li>Infomaniak (Suisse) pour le serveur de l'outil d'automatisation et des statistiques ;</li>
          <li>Pipedrive (Union européenne) pour le suivi des demandes et des chantiers ;</li>
          <li>Brevo (France, Union européenne) pour les e-mails de conseils, si vous les avez demandés ;</li>
          <li>ASPSMS (Suisse) pour l'envoi des SMS ;</li>
          <li>Healthchecks.io (Union européenne) pour la surveillance technique, sans vos coordonnées.</li>
        </ul>
        <p>Vos données sont hébergées en Suisse ou dans l'Union européenne, dont le niveau de protection est reconnu par le Conseil fédéral. Les photos que vous nous autorisez à publier sont visibles par tous sur les supports choisis, dont notre fiche Google.</p>
        <h2>Combien de temps nous les gardons</h2>
        <ul>
          <li>Demande sans suite : 24 mois après notre dernier contact, puis effacement.</li>
          <li>Photos et plans envoyés par le formulaire : 30 jours sur le serveur du site ; ensuite seulement dans le dossier de votre demande (outil de suivi et messagerie des associés), avec la même durée que la demande.</li>
          <li>Clients : les documents comptables et contractuels 10 ans (obligation légale) ; les autres données le temps de notre responsabilité pour les défauts (5 ans après la réception des travaux), puis revue.</li>
          <li>Adresse postale donnée pour le guide imprimé : 3 mois après l'envoi.</li>
          <li>Adresse e-mail donnée pour les conseils : jusqu'à votre désinscription, et 24 mois au plus.</li>
          <li>Si vous refusez nos messages : nous gardons votre adresse sous une forme codée, uniquement pour respecter ce refus.</li>
          <li>Adresse IP : notre formulaire ne l'enregistre jamais en clair. Une empreinte codée sert 24 heures à bloquer les abus ; un extrait de cette empreinte reste 30 jours dans le journal technique.</li>
          <li>Journaux techniques de l'hébergeur (adresse IP, pages demandées) : %(journaux)s.</li>
          <li>Historique de l'outil d'automatisation : 30 jours. Sauvegardes : remplacées en quatre semaines au plus.</li>
        </ul>
        <h2>Statistiques du site, sans cookie</h2>
        %(stats)s
        <p>Le site garde aussi dans votre navigateur, le temps que l'onglet reste ouvert (« stockage de session »), la provenance de votre visite, pour la joindre à votre demande si vous en envoyez une, un repère indiquant que vous avez commencé un formulaire et votre saisie en cours, pour ne rien perdre si la page se recharge. Rien n'est transmis à un tiers, et tout disparaît quand vous fermez l'onglet.</p>
        <p>Si votre navigateur envoie le signal « Ne pas me pister » (Do Not Track) ou « Global Privacy Control », aucune mesure n'est faite et rien n'est enregistré dans votre navigateur. Vous pouvez aussi bloquer ce stockage dans les réglages de votre navigateur : le site et le formulaire fonctionnent quand même.</p>
        <h2>Vos droits</h2>
        <p>Vous pouvez à tout moment, gratuitement :</p>
        <ul>
          <li>savoir quelles données nous avons sur vous et en recevoir une copie, sous forme électronique si vous le souhaitez ;</li>
          <li>les faire corriger ;</li>
          <li>les faire effacer, sous réserve de nos obligations légales de conservation ;</li>
          <li>retirer un accord donné (conseils par e-mail, photos) et vous opposer à tout message de notre part.</li>
        </ul>
        <p>Écrivez-nous à %(mail)s ou par courrier à l'adresse ci-dessus : nous répondons dans les 30 jours. Si vous estimez que vos droits ne sont pas respectés, vous pouvez vous adresser au Préposé fédéral à la protection des données et à la transparence (PFPDT), <a href="https://www.edoeb.admin.ch" rel="noopener">www.edoeb.admin.ch</a>.</p>
        <p class="maj">Dernière mise à jour : %(date)s</p>""" % dict(
        mail=mail_html(), tel=tel_link(), stats=stats, heberg=heberg, date=DATE,
        messagerie=marque('V02', 'notre fournisseur de messagerie'),
        journaux=marque('C34', 'durée fixée par l\'hébergeur'))
    corps += """    <section class="section">
      <div class="container prose">
        %s
      </div>
    </section>
""" % texte
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
