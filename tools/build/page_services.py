# -*- coding: utf-8 -*-
"""Pages services (architecture §4.2, copy deck §C à §F) : un gabarit, quatre jeux de textes."""
import ctx
from ctx import e, T, V, definitif, marque, M, PROD
from common import page, page_head, ld_page, TEL, TEL_URI, devis_btn, svc_nom, svc_url, doc, nom_isolantes, suivi_doc
import composants as c
import portfolio as pf
from icons import INFO

ZONES = ['Canton de Genève', 'Canton de Vaud', 'Canton de Neuchâtel', 'Canton de Fribourg', 'Valais romand', 'Canton du Jura', 'Jura bernois']
PRIX_REPLI = 'Le prix dépend'


def figure(pid, legende, sizes='(min-width: 1000px) 520px, 100vw', eager=False):
    return '<figure class="ph">%s<figcaption>%s</figcaption></figure>' % (c.pic(pid, sizes, pf.alt(pid), eager=eager), legende)


def figure_aa(pid, legende, eager=False):
    _, _, _, _, alt_av, alt_ap, _ = pf.PAIRE[pid]
    return '<figure class="ph">%s<figcaption>%s</figcaption></figure>' % (c.aa_pic(pid, 'apres', '(min-width: 1000px) 520px, 100vw', alt_ap), legende)


def savoir(items):
    return '<ul class="savoir">%s</ul>' % ''.join('<li>%s<p>%s</p></li>' % (INFO, x) for x in items if x)


def pour_qui(part, pro):
    return '''<div class="duo duo--boxes">
          <div class="box"><h3>Particuliers</h3><p>%s</p></div>
          <div class="box"><h3>Professionnels</h3><p>%s</p><a class="link-arrow" href="professionnels.html">Espace professionnels</a></div>
        </div>''' % (part, pro)


def prix_q(question, repli):
    """Questions de prix : la fourchette (C31) n'est pas fournie ; le repli s'affiche, signalé en vérification."""
    M('C31')
    return (question, marque('C31', repli), repli)


def lien_filtre(service, texte_filtre, texte_tous):
    """Lien vers les réalisations filtrées, seulement si le filtre a au moins un projet dans ce mode."""
    n = sum(1 for p in pf.PROJETS if pf.proj_ok(p) and service in pf.proj_tags(p))
    n += sum(1 for x in pf.PAIRES if service in pf.paire_services(x[0]))
    if n:
        return '<a class="link-arrow" href="realisations.html?filtre=%s">%s</a>' % (service, texte_filtre)
    return '<a class="link-arrow" href="realisations.html">%s</a>' % texte_tous


# ---------------------------------------------------------------- données des quatre pages
def placo():
    s = 'placo'
    return dict(
        service=s, crumb='Placo', title='Placo, cloisons et faux-plafonds à Genève | Andy Construct',
        desc=V('C05', 'Cloisons, doublages et faux-plafonds en plaques de plâtre, posés puis peints. Logements, bureaux et bâtiments publics, à Genève et en Suisse romande.',
               'Cloisons, doublages et faux-plafonds en plaques de plâtre, prêts à peindre. Logements, bureaux et bâtiments publics, à Genève et en Suisse romande.'),
        h1='Placo : cloisons, doublages et faux-plafonds',
        chapeau='Diviser une pièce, redresser un mur, cacher des tuyaux, abaisser un plafond : les plaques de plâtre le permettent sans maçonnerie.'
                + T('C05', ' Nous posons, puis <a href="peinture.html">nous peignons</a>.', ''),
        btn='Demander un devis pour du placo',
        bref=['Logements, bureaux, commerces et salles', T('C05', 'Pose, joints et peinture par la même équipe', 'Pose et joints, prêt à peindre'),
              'Genève et toute la Suisse romande'],
        photo=figure('faux-plafond-placo-gorge-lumineuse-02', 'Faux-plafond arrondi en plaques de plâtre, éclairage intégré', eager=True),
        faire='''<h2 id="faire-titre">Ce que nous posons en plaques de plâtre</h2>
        <p class="lead">Une ossature métallique, des plaques vissées, des joints enduits puis poncés : la même technique sert à quatre ouvrages.</p>
        <div class="blocs">
          <div class="bloc" id="cloisons"><h3>Cloisons</h3><p>Une cloison sépare une pièce en deux, ou crée une chambre, un bureau, une salle de réunion. Elle se monte en quelques jours, sans attendre le séchage d'une maçonnerie. Avec un isolant à l'intérieur, elle atténue le bruit d'une pièce à l'autre. Nous prévoyons dès la pose les portes, les prises et les renforts pour fixer un meuble ou une télévision.</p></div>
          <div class="bloc" id="doublages"><h3>Doublages</h3><p>Un doublage est un parement de plaques posé devant un mur existant. Il redresse un mur abîmé ou irrégulier, laisse passer les gaines électriques et peut recevoir un isolant, <a href="cloisons-isothermes.html">contre le froid</a> ou <a href="isolation-acoustique.html">contre le bruit</a>.</p></div>
          <div class="bloc" id="faux-plafonds"><h3>Faux-plafonds</h3><p>Un faux-plafond est suspendu sous le plafond existant. Il cache conduites et ventilation, accueille spots et trappes de visite, et permet des formes : retombées, courbes, gorges lumineuses. C'est aussi une bonne manière de refaire un plafond fissuré ou abîmé par un dégât d'eau.</p></div>
          <div class="bloc" id="caissons"><h3>Caissons et habillages</h3><p>Une poutre, une gaine ou un appareil de ventilation à cacher ? Nous construisons un caisson en plaques de plâtre, ajusté à la place disponible, avec une trappe si l'appareil doit rester accessible.</p></div>
        </div>''',
        qui=pour_qui('Créer une chambre ou un bureau, refaire un plafond après un dégât d\'eau, cacher des tuyaux, aménager des combles. Nous venons voir, puis nous vous remettons une offre écrite (votre devis).',
                     T('C14', 'Lots de plâtrerie et de faux-plafonds (CFC 271 et 283), réaménagement de bureaux, remise en état entre deux locataires. Offres établies sur plans et descriptifs.',
                       'Lots de plâtrerie (CFC 271), réaménagement de bureaux, remise en état entre deux locataires. Offres établies sur plans et descriptifs.')),
        savoir=[T('C07', 'Poncer les joints fait une poussière fine. Nous fermons la zone, protégeons les passages et nettoyons chaque soir.',
                  'Poncer les joints fait une poussière fine : la zone de travail doit être fermée et protégée.'),
                'Les câbles et les gaines passent avant la fermeture : nous coordonnons la pose avec votre électricien.',
                'En salle de bains, on pose des plaques prévues pour l\'humidité. Nous ne posons pas le carrelage.',
                'Sur un grand mur éclairé de côté, les joints se voient davantage. Nous choisissons avec vous, à la visite, le niveau de finition qui convient.',
                'Locataire ou copropriétaire ? Certains travaux demandent un accord écrit : voyez les questions plus bas.'],
        realisations=lambda: real_placo(),
        specifique='',
        faq_titre='Questions fréquentes sur le placo',
        faq=[prix_q('Combien coûte une cloison ou un faux-plafond en placo ?',
                    'Le prix dépend de la surface, de la hauteur, de l\'isolant, du nombre de portes et de spots, et de la finition. Après la visite, vous recevez une offre écrite détaillée.'),
             ('Combien de temps dure la pose ?', 'Pour une cloison ou le plafond d\'une pièce d\'habitation, comptez en général quelques jours, séchage des joints compris. Pour des bureaux ou une salle, nous établissons un calendrier des travaux après la visite. Le délai figure dans l\'offre.', None),
             ('Une cloison en placo isole-t-elle du bruit ?', 'Une cloison simple atténue les voix, sans plus. Avec un isolant et deux plaques de chaque côté, elle isole nettement mieux. Si le bruit est votre souci principal, voyez notre page sur <a href="isolation-acoustique.html">l\'isolation acoustique</a>.', None),
             ('Peut-on fixer des meubles sur une cloison en placo ?', 'Oui, avec des chevilles adaptées pour les charges légères. Pour un meuble lourd, une télévision ou des éléments de cuisine, nous posons des renforts dans la cloison : dites-le-nous avant la fermeture.', None),
             ('Le placo convient-il à une salle de bains ?', 'Oui, avec des plaques prévues pour les pièces humides. Les zones exposées à l\'eau reçoivent ensuite une étanchéité sous le carrelage, posée par le carreleur.', None),
             ('Faut-il l\'accord de la régie ou de la copropriété ?', 'Si vous êtes locataire, oui : il faut l\'accord écrit du bailleur avant de transformer le logement. En PPE (propriété par étages), une cloison dans votre lot est en général possible ; vérifiez le règlement, et parlez-en à l\'administrateur si elle touche une partie commune.', None)],
        h2_demande='Demander un devis pour du placo',
        ld_desc='Cloisons, doublages, faux-plafonds et caissons en plaques de plâtre, posés puis peints, à Genève et en Suisse romande.',
        service_type='Plâtrerie et faux-plafonds en plaques de plâtre',
    )


def real_placo():
    p1 = pf.PROJ['projet-hall-gorge-lumineuse']
    refs = (marque('C23', '<div class="refs-svc"><p>Réalisé notamment pour :</p>%s</div>' % c.refs_service(['ville-de-geneve', 'conservatoire-musique-geneve', 'energestion']), bloc=True)
            if definitif('C23') else '<p class="refs-svc refs-svc--txt">Ils nous ont confié des travaux : Ville de Genève · Conservatoire de musique de Genève · HEAD – Genève.</p>')
    return '''<h2 id="real-titre">Nos réalisations en placo</h2>
        <div class="real-svc">
          %s
          <div class="real-svc__photos">%s%s</div>
        </div>
        %s
        <p class="section-foot">%s</p>''' % (
        pf.carte_projet(p1, '(min-width: 1000px) 640px, 100vw', ancre=False, grande=True),
        figure('chantier-suspentes-ossature-01', pf.legende('chantier-suspentes-ossature-01'), '(min-width: 1000px) 300px, (min-width: 640px) 45vw, 100vw'),
        figure('habillage-placo-niches-arrondies-01', pf.legende('habillage-placo-niches-arrondies-01'), '(min-width: 1000px) 300px, (min-width: 640px) 45vw, 100vw'),
        refs, lien_filtre('placo', 'Voir toutes les réalisations en placo', 'Voir toutes les réalisations'))


def peinture():
    s = 'peinture'
    aa6_ok = definitif('C26')   # « Séjour repeint » : la prestation peinture doit être confirmée (C26) en production
    photo = marque('C26', figure_aa('aa6', 'Séjour repeint, avec un faux-plafond et des spots', eager=True), bloc=True) if aa6_ok else ''
    return dict(
        service=s, crumb='Peinture', title='Entreprise de peinture intérieure à Genève | Andy Construct',
        desc='Peinture des murs et plafonds : appartements, fins de bail, cages d\'escalier, bureaux. Supports préparés, chantier protégé. Genève et Suisse romande.',
        h1='Peinture intérieure : murs, plafonds, cages d\'escalier',
        chapeau='Repeindre un appartement, préparer une fin de bail, rafraîchir des bureaux ou une cage d\'escalier : nous préparons les supports, protégeons les lieux et rendons des pièces propres.',
        btn='Demander un devis pour de la peinture',
        bref=['Appartements, villas, bureaux, parties communes', 'Murs préparés avant la peinture',
              T('C07', 'Lieux protégés, nettoyés le dernier jour', 'Lieux protégés pendant les travaux')],
        photo=photo,
        faire='''<h2 id="faire-titre">Ce que nous peignons</h2>
        <p class="lead">Une peinture qui tient dépend surtout de ce qu'on fait avant : reboucher, poncer, poser une couche d'impression. Nous le faisons pour chaque chantier.</p>
        <div class="blocs">
          <div class="bloc"><h3>Logements</h3><p>Une pièce ou tout l'appartement, habité ou vide. %s</p></div>
          %s
          <div class="bloc"><h3>Cages d'escalier et parties communes</h3><p>%s</p></div>
          <div class="bloc"><h3>Bureaux et commerces</h3><p>%s</p></div>
          %s
        </div>''' % (
            T('C17', 'Nous déplaçons et couvrons les meubles, protégeons les sols, rebouchons trous et fissures, puis appliquons deux couches de peinture.',
              'Nous déplaçons et couvrons les meubles, protégeons les sols, rebouchons trous et fissures, puis peignons murs et plafonds.'),
            T('C17', '<div class="bloc"><h3>Fins de bail et remises en état</h3><p>Pour les régies et les propriétaires : remise en état entre deux locataires, dans des délais courts, pour que le logement soit prêt à l\'état des lieux d\'entrée.</p></div>', ''),
            T('C20', 'Dans un immeuble habité, nous travaillons par étages, gardons le passage libre et informons les habitants avant de commencer.',
              'Dans un immeuble habité, nous travaillons par étages, gardons le passage libre.'),
            T('C19', 'Le soir, le week-end ou zone par zone, pour que vous n\'ayez pas à fermer.', 'Zone par zone, pour limiter la gêne.'),
            T('C05', '<div class="bloc"><h3><a href="placo.html">Après nos travaux de placo</a></h3><p>Les cloisons et les plafonds neufs reçoivent une couche d\'impression, puis la peinture de finition. Vous n\'avez pas à chercher un autre artisan.</p></div>', '')),
        qui=pour_qui('Un appartement à rafraîchir après vingt ans, une pièce avant l\'arrivée d\'un enfant, un logement à préparer pour une vente. Nous venons voir, puis nous vous remettons une offre écrite (votre devis).',
                     T('C17', 'Remises en état de fin de bail, cages d\'escalier, bureaux et arcades. Lot de peinture (CFC 285), prix par pièce sur demande pour les régies.',
                       'Remises en état de fin de bail, cages d\'escalier, bureaux et arcades. Lot de peinture (CFC 285).')),
        savoir=[T('C06', 'La préparation compte autant que la peinture. Dans l\'offre, elle figure sur une ligne à part : vous voyez ce que vous payez.',
                  'La préparation compte autant que la peinture.'),
                'Une fissure revient si sa cause n\'est pas traitée (mouvement du bâtiment, humidité). Nous vous le disons à la visite.',
                'Une tache d\'humidité ou de moisissure demande d\'abord d\'en trouver la cause. La repeindre sans cela ne règle rien.',
                T('C17', 'Pour choisir une teinte, nous pouvons appliquer un échantillon sur le mur.', ''),
                'Nous peignons à l\'intérieur seulement : pas de façades.'],
        realisations=(lambda: '''<h2 id="real-titre">Nos réalisations en peinture</h2>
        %s
        <p class="section-foot"><a class="link-arrow" href="realisations.html">Voir toutes les réalisations</a></p>''' % pf.avant_apres('aa6', grande=True)) if aa6_ok else None,
        specifique='',
        faq_titre='Questions fréquentes sur la peinture',
        faq=[prix_q('Combien coûte la peinture d\'un appartement ?',
                    'Le prix dépend de la surface des murs et des plafonds, de leur état, de la hauteur, des meubles à déplacer et du nombre de teintes.'),
             prix_q('Combien de temps faut-il pour repeindre un appartement ?',
                    'Cela dépend de la surface et de l\'état des murs. La durée figure dans l\'offre écrite.'),
             c.Q('C20', 'Peut-on rester chez soi pendant les travaux ?', 'Oui. Nous travaillons pièce par pièce, couvrons les meubles et gardons un passage libre. Il suffit de dégager l\'accès aux murs.'),
             c.Q('C17', 'Faut-il vider les pièces ?', 'Non. Retirez les objets fragiles et ce qui est accroché aux murs ; nous déplaçons et couvrons les meubles.',
                 'Retirez au moins les objets fragiles et ce qui est accroché aux murs. Le reste se décide à la visite.'),
             c.Q('C17', 'Travaillez-vous pour les fins de bail ?', 'Oui, pour les régies et les propriétaires. Donnez-nous la date de l\'état des lieux : nous planifions les travaux pour que le logement soit prêt.'),
             ('Peignez-vous aussi les façades ?', 'Non. Nous travaillons à l\'intérieur : murs, plafonds, cages d\'escalier et parties communes. Pour une façade, adressez-vous à une entreprise de peinture extérieure.', None)],
        h2_demande='Demander un devis pour de la peinture',
        ld_desc='Peinture intérieure des murs et plafonds : logements, fins de bail, cages d\'escalier et bureaux, à Genève et en Suisse romande.',
        service_type='Peinture intérieure',
    )


def acoustique():
    s = 'isolation-acoustique'
    guide = doc('guide-bruit')
    specifique = ''
    if guide:
        specifique = '''<div class="guide">
          <h2 id="guide-titre">Guide : réduire le bruit chez soi</h2>
          <p>Ce qui marche, ce qui ne marche pas, et les questions à poser à une entreprise, quelle qu'elle soit. %d pages, 10 minutes de lecture.</p>
          <p><a class="btn" href="%s" %s>Télécharger le guide (%s)</a></p>
          %s
        </div>''' % (guide[2], guide[0], suivi_doc('guide-bruit'), guide[1], c.form_guide_poste('guide-reduire-le-bruit'))
    p6, p7 = pf.PROJ['projet-correction-acoustique'], pf.PROJ['projet-salle-de-reunion']
    cartes = ''.join(pf.carte_projet(p, '(min-width: 1000px) 560px, (min-width: 640px) 45vw, 100vw', ancre=False) for p in (p6, p7) if pf.proj_ok(p))
    refs = (marque('C23', '<div class="refs-svc"><p>Réalisé notamment pour :</p>%s</div>' % c.refs_service(['conservatoire-musique-geneve', 'head-geneve', 'collonge-bellerive']), bloc=True)
            if definitif('C23') else '<p class="refs-svc refs-svc--txt">Ils nous ont confié des travaux : Conservatoire de musique de Genève · HEAD – Genève · Salle de l\'Alhambra.</p>')
    return dict(
        service=s, crumb='Isolation acoustique', title='Isolation phonique et acoustique à Genève | Andy Construct',
        desc='Vous entendez vos voisins ? Doublages, faux-plafonds et cloisons acoustiques, correction de l\'écho dans les salles. Genève et Suisse romande.',
        h1='Isolation phonique et acoustique : moins de bruit chez vous',
        chapeau='Voisins, télévision, pas à l\'étage, voix dans la salle de réunion : nous isolons murs et plafonds pour que le bruit passe moins.'
                + T('C18', ' Et nous réduisons l\'écho des salles trop sonores.', ''),
        btn='Demander un devis pour une isolation acoustique',
        bref=['Logements, bureaux, écoles, salles communales', 'Des travaux choisis selon le bruit que vous entendez', 'Aucune promesse chiffrée sans mesure'],
        photo=figure('chantier-suspentes-ossature-01', 'Pendant les travaux : suspentes et ossature d\'un faux-plafond, sous une dalle isolée', eager=True),
        faire='''<h2 id="faire-titre">Isoler ou corriger : deux problèmes différents</h2>
        <div class="prose-cols">
          <p><strong>Isoler</strong>, c'est empêcher le bruit de passer d'un local à l'autre : celui du voisin, de l'étage, de la pièce d'à côté. Il faut alors une paroi à la fois lourde et souple, sans contact rigide avec la structure du bâtiment.</p>
          <p><strong>Corriger</strong>, c'est réduire l'écho à l'intérieur d'une pièce : une salle de réunion où l'on s'entend mal, un réfectoire, une salle communale. On pose alors des surfaces qui absorbent le son.</p>
          <p>Un panneau absorbant ne protège pas du bruit du voisin. Une cloison isolante ne réduit pas l'écho. À la visite, nous commençons donc par identifier ce que vous entendez.</p>
          <p>Dans un appartement, on isole le plus souvent contre le voisin. Dans une salle communale ou un réfectoire, on corrige d'abord l'écho. Il faut parfois faire les deux.</p>
        </div>
        <h2 class="h2-suite" id="poser-titre">Ce que nous posons contre le bruit</h2>
        <div class="blocs">
          <div class="bloc"><h3>Doublage acoustique d'un mur</h3><p>Une ossature indépendante du mur, une laine minérale, puis une ou deux plaques de plâtre. Efficace contre les voix et la télévision du voisin. %s</p></div>
          <div class="bloc"><h3>Faux-plafond acoustique</h3><p>Suspendu sous le plafond par des suspentes qui amortissent les vibrations, avec un isolant au-dessus. Il réduit les voix venant d'en haut, et en partie les bruits de pas.</p></div>
          <div class="bloc"><h3>Cloison acoustique</h3><p>Deux ossatures séparées, un isolant, des plaques doublées : pour une chambre, un bureau, une salle de réunion ou un cabinet où la confidentialité compte.</p></div>
          %s
        </div>''' % (T('C18', 'La pièce perd en général 7 à 10 cm.', 'La pièce perd quelques centimètres.'),
                     T('C18', '<div class="bloc" id="correction"><h3>Correction acoustique des salles</h3><p>Plafonds perforés et panneaux muraux qui absorbent le son, pour les salles de réunion, les salles communales et les salles de classe.</p></div>',
                       '<span id="correction"></span>')),
        qui='',   # pas de bloc « Pour qui ? » sur cette page (copy deck §E)
        savoir=['Les bruits de pas du voisin du dessus se traitent le mieux à la source, dans son sol. Un faux-plafond chez vous les atténue, sans les supprimer. Nous vous le disons à la visite.',
                'Le bruit passe aussi par les côtés : prises, gaines, portes, murs voisins. Une isolation qui oublie ces points déçoit.',
                'Personne ne peut promettre un résultat en décibels sans mesure.' + T('C15', ' Si une performance est exigée (norme SIA 181), elle est fixée par le projet, et nous posons un système qui y répond.', ''),
                'En location ou en PPE (propriété par étages), demandez l\'accord avant des travaux qui touchent un mur mitoyen ou la structure.',
                'L\'isolation acoustique seule n\'est en général pas subventionnée.',
                'Une pièce froide plutôt que bruyante ? Voyez nos <a href="cloisons-isothermes.html">%s</a>.' % V('C16', 'cloisons isolantes', 'cloisons isothermes')],
        realisations=lambda: '''<h2 id="real-titre">Nos réalisations en acoustique</h2>
        %s
        %s
        <p class="section-foot">%s</p>''' % (('<div class="projets projets--2">%s</div>' % marque('C18', cartes, bloc=True)) if cartes else '', refs,
                                            lien_filtre('isolation-acoustique', 'Voir toutes les réalisations en acoustique', 'Voir toutes les réalisations')),
        specifique=specifique,
        faq_titre='Questions fréquentes sur le bruit',
        faq=[('Comment réduire le bruit des voisins du dessus ?', 'Pour les voix et la musique, un faux-plafond acoustique, suspendu par des attaches qui amortissent les vibrations, donne de bons résultats. Pour les bruits de pas, le plus efficace est d\'agir sur le sol du voisin. À la visite, nous vous disons ce qui est réaliste chez vous.', None),
             ('Les panneaux en mousse ou les boîtes à œufs isolent-ils du bruit ?', 'Non. Ils réduisent un peu l\'écho dans la pièce, mais n\'empêchent pas le bruit de passer. Pour isoler, il faut une paroi lourde, désolidarisée de la structure et étanche à l\'air.', None),
             prix_q('Combien coûte une isolation phonique ?', 'Le prix dépend de la surface, du type de travaux (doublage, faux-plafond, cloison), des points faibles à traiter et de la finition.'),
             c.Q('C18', 'Combien de place perd-on ?', 'Un doublage acoustique prend en général 7 à 10 cm sur l\'épaisseur de la pièce, un faux-plafond un peu plus. Nous mesurons avant de proposer.',
                 'Quelques centimètres sur l\'épaisseur de la pièce. Nous mesurons avant de proposer.'),
             c.Q('C18', 'Pouvez-vous mesurer le bruit avant et après ?', 'Nous ne faisons pas de mesure acoustique nous-mêmes. Si une mesure est demandée, elle est confiée à un bureau d\'acoustique, et nous travaillons avec lui.'),
             c.Q('C18', 'Que faire dans une salle de réunion où l\'on s\'entend mal ?', 'C\'est un problème d\'écho : des panneaux absorbants au plafond ou aux murs le réduisent nettement, souvent sans gros travaux. Si les voix passent aussi dans le bureau voisin, il faut en plus isoler la cloison.')],
        h2_demande='Demander un devis pour une isolation acoustique',
        ld_desc='Isolation phonique des murs et plafonds (doublages, faux-plafonds et cloisons acoustiques) et correction de l\'écho des salles, à Genève et en Suisse romande.',
        service_type='Isolation acoustique',
    )


def isolantes():
    s = 'cloisons-isothermes'
    aa3 = pf.avant_apres('aa3', grande=False)
    p2 = pf.PROJ['projet-grande-salle-ossature']
    p2_html = marque('C25', pf.carte_projet(p2, '(min-width: 1000px) 560px, (min-width: 640px) 45vw, 100vw', ancre=False), bloc=True) if (definitif('C25') and pf.proj_ok(p2)) else ''
    sing = T('C16', 'une cloison isolante', 'une cloison isotherme')
    return dict(
        service=s, crumb=svc_nom(s), title=V('C16', 'Cloisons isolantes, cave et garage à Genève | Andy Construct', 'Cloisons isothermes, cave et garage à Genève | Andy Construct'),
        desc='Cloisons isolantes (isothermes) entre pièces chauffées et caves, garages ou combles, en plaques de plâtre. Genève et Suisse romande.',
        h1='Cloisons isothermes et isolantes : caves, garages et combles',
        chapeau='Une pièce froide au-dessus d\'un garage, un bureau contre une cave, des combles à aménager : une cloison ou un doublage isolant sépare ce qui est chauffé de ce qui ne l\'est pas.',
        precision=T('C16', 'Nous ne posons pas de chambres froides ni de panneaux frigorifiques.', ''),
        btn='Demander un devis pour ' + sing,
        bref=['Entre pièces chauffées et locaux froids', 'Ossature, isolant, plaques : prêt à peindre', 'Villas, immeubles, locaux d\'activité'],
        photo=figure('chantier-ossature-puits-de-lumiere-02', 'Pendant les travaux : ossature métallique et isolant, avant la pose des plaques', eager=True),
        faire='''<h2 id="faire-titre">Ce que nous posons pour garder la chaleur</h2>
        <div class="blocs">
          <div class="bloc"><h3>Cloison isolante</h3><p>Entre une pièce chauffée et un garage, une cave, un atelier ou un dépôt : une ossature métallique, un isolant thermique et des plaques de plâtre. La cloison limite les pertes de chaleur et les courants d'air froid.</p></div>
          <div class="bloc"><h3>Doublage isolant d'un mur froid</h3><p>Un mur contre la terre, une cave ou l'extérieur reste froid au toucher ? Un doublage avec isolant, posé côté pièce, améliore le confort.</p></div>
          <div class="bloc"><h3>Plafond de cave ou de garage</h3><p>%s</p></div>
          %s
        </div>''' % (T('C16', 'Le sol de la pièce du dessus est froid ? Un isolant fixé sous la dalle de la cave ou du garage, fermé par des plaques si le local le demande, réduit la perte de chaleur.',
                       'Le sol de la pièce du dessus est froid ? Un isolant fixé sous la dalle de la cave ou du garage, fermé par des plaques si le local le demande, réduit la perte de chaleur.'),
                     T('C16', '<div class="bloc"><h3>Combles et rampants</h3><p>Un isolant entre ou sous les chevrons, puis des plaques de plâtre : les combles deviennent une pièce habitable.</p></div>', '')),
        qui=pour_qui('Une chambre au-dessus du garage, un sous-sol aménagé en bureau, des combles à transformer. Nous venons voir, puis nous vous remettons une offre écrite (votre devis).',
                     'Locaux non chauffés dans les immeubles (caves, parkings, locaux techniques), ateliers et dépôts attenants à des bureaux. Offres sur plans et descriptifs.'),
        savoir=['L\'épaisseur d\'isolant dépend de l\'écart de température entre les deux locaux et des exigences de votre canton. Nous la proposons dans l\'offre.',
                'Sur un mur enterré ou dans une cave humide, on vérifie d\'abord l\'humidité : un isolant posé sur un mur mouillé crée de nouveaux problèmes.',
                'Le pare-vapeur se pose du côté chauffé. Mal placé, il fait condenser l\'humidité dans la paroi.',
                'Le bruit vous gêne aussi ? Un isolant bien choisi peut traiter les deux : voyez <a href="isolation-acoustique.html">l\'isolation acoustique</a>.',
                'Entre un garage et un logement, des exigences de protection incendie peuvent s\'appliquer. '
                + T('C15', 'Nous en tenons compte dans le choix des plaques.', 'Vérifiez-les avant les travaux.')],
        realisations=lambda: '''<h2 id="real-titre">Nos réalisations en isolation</h2>
        <div class="projets projets--2">%s%s</div>
        <p class="section-foot">%s</p>''' % (aa3, p2_html, lien_filtre('cloisons-isothermes', 'Voir toutes les réalisations', 'Voir toutes les réalisations')),
        specifique='''<div class="encadre">
          <h2 id="subv-titre">Des subventions sont-elles possibles ?</h2>
          <p>Certaines isolations thermiques peuvent être subventionnées, par le Programme Bâtiments et par les cantons, si elles atteignent les performances exigées. La demande se dépose <strong>avant</strong> le début des travaux. Renseignez-vous auprès du service de l'énergie de votre canton%s</p>
        </div>''' % T('C43', ' ; nous vous fournissons les informations techniques dont il a besoin.', '.'),
        faq_titre='Questions fréquentes sur l\'isolation intérieure',
        faq=[c.Q('C16', 'Qu\'est-ce qu\'une cloison isotherme ?',
                 'C\'est une cloison isolante : une ossature métallique, un isolant thermique et des plaques de plâtre. Elle sépare une pièce chauffée d\'un local qui ne l\'est pas, comme un garage ou une cave. Ce n\'est pas une chambre froide.',
                 'C\'est une cloison isolante : une ossature métallique, un isolant thermique et des plaques de plâtre. Elle sépare une pièce chauffée d\'un local qui ne l\'est pas, comme un garage ou une cave.'),
             ('Comment isoler le plafond d\'une cave ou d\'un garage ?', 'On fixe un isolant sous la dalle, puis on le ferme par des plaques si le local est utilisé. Le sol de la pièce du dessus devient moins froid, et la chaleur reste où elle doit être.', None),
             c.Q('C16', 'Faut-il une autorisation pour aménager des combles ?', 'Transformer des combles en pièce habitable peut demander une autorisation de construire, selon le canton et la commune. Renseignez-vous avant de commencer ; nous vous donnons les informations techniques utiles.'),
             ('Quelle épaisseur d\'isolant faut-il ?', 'Elle dépend des températures de part et d\'autre et des exigences énergétiques du canton. Nous la proposons dans l\'offre, avec le type d\'isolant.', None),
             prix_q('Combien coûte une cloison isolante ?', 'Le prix dépend de la surface, de l\'épaisseur d\'isolant, des portes et de la finition.')],
        h2_demande='Demander un devis pour ' + sing,
        ld_desc='Cloisons et doublages isolants (isothermes) entre pièces chauffées et caves, garages ou combles, en plaques de plâtre, à Genève et en Suisse romande.',
        service_type=V('C16', 'Cloisons isolantes et isolation intérieure', 'Cloisons isothermes et isolation intérieure'),
        alternate=V('C16', 'Cloisons isothermes', 'Cloisons isolantes'),
    )


# ---------------------------------------------------------------- gabarit
def rendre(d):
    s = d['service']
    fichier = svc_url(s)
    p = dict(fichier=fichier, formulaire=True, service=s, title=d['title'], desc=d['desc'])
    faq = [q if len(q) == 3 and q[2] is not None else (q[0], q[1], q[1]) for q in d['faq'] if q]
    faq = [(q, a, __import__('re').sub(r'<[^>]+>', '', t)) for q, a, t in faq]
    faq_html, faq_ld = c.faq_items(faq)
    url = PROD + fichier
    service_ld = {'@type': 'Service', '@id': url + '#service', 'name': ctx.fr(svc_nom(s, html=False)), 'serviceType': d['service_type'],
                  'description': d['ld_desc'], 'provider': {'@id': PROD + '#entreprise'}, 'url': url,
                  'areaServed': [{'@type': 'AdministrativeArea', 'name': z} for z in ZONES]}
    if d.get('alternate'):
        service_ld['alternateName'] = d['alternate']
    ld = ld_page(fichier, d['title'], svc_nom(s, html=False), extra={'about': {'@id': url + '#service'}})
    ld['@graph'].append(service_ld)
    p['ld'] = [ld, c.faq_ld(url, faq_ld)]

    bref = '<ul class="bref" aria-label="En bref">%s</ul>' % ''.join('<li>%s</li>' % b for b in d['bref'] if b)
    precision = ('<p class="precision">%s</p>' % d['precision']) if d.get('precision') else ''
    actions = '<div class="page-head__actions">%s<a class="btn btn--ghost" href="%s" data-suivi-numero="fixe" data-suivi-emplacement="entete_page">Appeler le %s</a></div>' % (
        devis_btn(p, 'entete_page', texte=d['btn']), TEL_URI, TEL)
    corps = page_head(d['crumb'], d['h1'], d['chapeau'], extra=precision + actions + bref, photo=d['photo'], cls='page-head--svc')

    corps += '''    <section class="section" aria-labelledby="faire-titre">
      <div class="container">
        %s
      </div>
    </section>
''' % d['faire']
    if d['qui']:
        corps += '''    <section class="section section--mist section--tight" aria-labelledby="qui-titre-%s">
      <div class="container">
        <h2 id="qui-titre-%s">Pour qui ?</h2>
        %s
      </div>
    </section>
''' % (s, s, d['qui'])
    corps += '''    <section class="section" aria-labelledby="savoir-titre">
      <div class="container narrow">
        <h2 id="savoir-titre">Ce qu'il faut savoir avant de commencer</h2>
        %s
      </div>
    </section>
''' % savoir(d['savoir'])
    if d['specifique']:
        corps += '    <section class="section section--tight">\n      <div class="container">\n        %s\n      </div>\n    </section>\n' % d['specifique']
    if d['realisations']:
        corps += '''    <section class="section section--mist" aria-labelledby="real-titre">
      <div class="container">
        %s
      </div>
    </section>
''' % d['realisations']()
    corps += c.section_methode_courte()
    corps += '''    <section class="section faq" aria-labelledby="faq-titre">
      <div class="container split split--48">
        <div class="faq__head"><h2 id="faq-titre">%s</h2><p>Une autre question ? Appelez le <a href="%s" data-suivi-numero="fixe" data-suivi-emplacement="faq">%s</a>.</p></div>
        <div class="faq__list">%s</div>
      </div>
    </section>
''' % (d['faq_titre'], TEL_URI, TEL, faq_html)
    corps += c.bloc_demande(p, service=s, h2=d['h2_demande'], source='page-' + s, surtitre=False)
    page(p, corps)


def build():
    for f in (placo, peinture, acoustique, isolantes):
        rendre(f())
