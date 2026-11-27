# v8 — Étalonnage des photos, nouveau logo, héro, doublons, animations globales

## Introspection
| Ce que j'ai mal fait | Conséquence | Ce qui change |
|---|---|---|
| J'ai réagi retour par retour, sans relire chaque page en entier | Des éléments empilés : badges « Registre du commerce » 4 fois par page (en-tête, menu, formulaire, pied de page), logos 2 fois, photos de l'en-tête reprises dans la bande des projets | Script d'audit des doublons (photos, logos, badges, titres) page par page : 0 doublon |
| J'ai posé les photos telles quelles | Ensemble incohérent : murs jaunes, piscine verte, salon et combles sombres, traçage plat | Étalonnage commun à l'import (balance des blancs, exposition, contraste, hautes lumières) |
| En-tête de l'accueil : 4 photos hétérogènes (salon sombre + photos claires) | Pas d'unité | 3 photos claires, nettes, même étalonnage |
| Filigrane tiré d'un tracé vectoriel d'un PNG | Bords en escalier une fois agrandi | Image du vrai « A » du logo |
| Une règle CSS ajoutée sans revérifier l'en-tête | La photo de l'en-tête disparaissait sur ordinateur (repéré à la capture, corrigé) | Capture systématique après chaque règle globale |

## Photos : analyse et traitement (`tools/images/importer_photos.py`)
Mesures sur les originaux (luminance, dominante R/G/B, contraste, netteté, hautes lumières brûlées) :
- Meilleure photo : salle vitrée (netteté 34,8). Bonnes : piscine, restaurant.
- Dominante jaune : couloir, salle de réunion, pièce sous combles. Dominante verte : piscine, salle vitrée.
- Sous-exposées : salon, combles. Plate : traçage laser. Faible : couloir (480 px, floue).
Traitement : gris neutre légèrement chaud commun (R 1,015 · G 1 · B 0,975, 75 % de la dominante corrigée), gamma vers une
luminance de 0,52, contraste sigmoïde si l'écart-type < 0,17, hautes lumières protégées ; recadrages 4:5 et 16:9 centrés
sur le sujet ; métadonnées supprimées.

## Logo
Logo « géométrique » partout : en-tête, pied de page (version blanche), espace /admin, favicons et icône d'application
(« A » sur fond blanc), marqueurs de la carte, image de partage, PDF (régénérés), données structurées.

## Doublons retirés
Badges du menu mobile, de la colonne du formulaire et du pied de page ; logos du pied de page sur les pages qui ont déjà le
mur des références ; tableau des normes sur l'accueil ; section « Collectivités » (professionnels) ; photos répétées
(accueil, réalisations, acoustique).

## Animations globales
Barre d'en-tête qui descend au chargement ; en-tête de l'accueil : filigrane qui entre puis dérive, photos qui s'ouvrent
en rideau avec zoom lent, carte du projet qui change avec la photo ; titres de section mot à mot ; grilles en cascade ;
photos qui se dévoilent ; parallaxe ; bande des projets ; compteurs. Tout est coupé en mouvement réduit.

## Axes d'amélioration
1. **Photos originales** : trois photos ne font que 480 px, les autres 768 à 1024 px (sauf deux en 4032 px). Les originaux
   du téléphone (4032 px) permettraient des en-têtes plus nets et la correction des verticales (salle vitrée, salle de
   réunion). Idéal : une demi-journée de photographe sur 5 ou 6 chantiers récents.
2. **Logo vectoriel** (SVG/AI/PDF) : plus net à l'écran et indispensable pour l'impression ; prévoir une version compacte
   (le « CONSTRUCT » devient petit dans l'en-tête).
3. **Preuves** : aucun avis Google ni témoignage affiché ; lieux et accords de citation des références à confirmer.
4. **Bande des projets** : elle reprend d'anciennes photos de chantier, moins bonnes ; à remplacer au fil des nouvelles.
5. **Cartes sans photo** (fibre de bois, cloisons mobiles et aluminium, enduits, finitions) : schémas en attendant des photos.
6. **PDF** : couverture du dossier de références encore sur une ancienne photo.
7. **Mise en ligne** : tester l'envoi réel des formulaires (SMTP), configurer les statistiques, déclarer le site à Google
   (Search Console, fiche d'établissement).
8. **Juridique** : mentions légales et protection des données à valider à la fin.
