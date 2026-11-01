/*
 * Maquette du tableau de bord d'administration : DONNÉES FICTIVES.
 * Aucune personne, aucune organisation, aucun chiffre n'est réel.
 * « Aujourd'hui » = jeudi 22 avril 2027, 9 h 40 (sixième mois après la mise en ligne, M1 = novembre 2026).
 * Les scores, priorités, échéances et indicateurs sont CALCULÉS par app.js à partir de ces lignes,
 * avec la grille de site/api/data/scoring.json et les heures ouvrables genevoises.
 * Les objectifs viennent de docs/v2/strategie-acquisition.md §1.1 (scénario M).
 */
window.MAQ = (function () {
  'use strict';

  var MAINTENANT = '2027-04-22 09:40';

  var UTILISATEURS = [
    { id: 'u1', nom: 'Camille Exemple', role: 'Associée', metier: 'bureau', deuxFa: 'Application + 10 codes', derniere: '2027-04-22 07:52' },
    { id: 'u2', nom: 'Alex Modèle', role: 'Associé', metier: 'terrain', deuxFa: 'Application + 10 codes', derniere: '2027-04-22 09:31' },
    { id: 'u3', nom: 'Secrétariat (démo)', role: 'Secrétariat', metier: '', deuxFa: 'Application', derniere: '2027-04-21 16:02' },
    { id: 'u4', nom: 'Agence, marketing (démo)', role: 'Agence marketing', metier: '', deuxFa: 'Application', derniere: '2027-04-19 10:15' },
    { id: 'u5', nom: 'Agence, technique (démo)', role: 'Agence technique', metier: '', deuxFa: 'Clé d’accès', derniere: '2027-04-02 14:40' }
  ];
  var MOI = 'u2';

  /* Grille de site/api/data/scoring.json (version 2026-10-31), recopiée telle quelle. */
  var GRILLE = {
    version: '2026-10-31',
    seuils: { A: 65, B: 40 },
    type_client: { commune: 30, regie: 30, architecte: 25, entreprise: 20, proprietaire: 15, '': 10, locataire: 5 },
    service: { plusieurs: 15, 'isolation-acoustique': 15, placo: 15, 'cloisons-isothermes': 12, peinture: 10, 'ne-sait-pas': 10, '': 10, autre: null },
    surface: { 'plus-200': 20, '50-200': 15, '15-50': 8, 'ne-sait-pas': 6, '': 6, 'moins-15': 2 },
    zone: { '1': 15, '2': 10, '3': 5, inconnue: 5, hors: null },
    delai: { 'moins-1-mois': 10, '1-3-mois': 8, '3-6-mois': 5, 'non-defini': 2, '': 2 },
    source: { recommandation: 10, partenaire: 10, b2b: 10, 'client-existant': 10, 'appel-direct': 8, 'carte-google': 8,
      'panneau-vehicule': 8, 'recherche-google': 7, annuaire: 7, 'google-ads': 6, aimant: 6, crm: 6, meta: 4, linkedin: 4,
      plateforme: 3, 'site-referent': 5, autre: 5, 'direct-inconnu': 5 },
    connu_par: { recommandation: 'recommandation', 'regie-architecte': 'partenaire', 'carte-google': 'carte-google',
      'recherche-google': 'recherche-google', 'panneau-vehicule': 'panneau-vehicule', facebook: 'meta', linkedin: 'linkedin', autre: 'autre' },
    bonus: { fichier_joint: 5, telephone_fourni: 3, message_vide_sans_telephone: -5 },
    regles: {
      plancher_B_types_client: ['commune', 'regie', 'architecte'],
      plancher_B_formulaires: ['rappel'],
      urgence_mots: ['dégât', 'degat', 'fuite', 'état des lieux', 'etat des lieux', 'fin de bail'],
      urgence_delai: 'moins-1-mois',
      zone3_sans_penalite_types_client: ['regie', 'architecte', 'commune', 'entreprise'],
      zone3_sans_penalite_surfaces: ['50-200', 'plus-200']
    }
  };

  /*
   * Demandes fictives. Une ligne par demande ; la référence est attribuée dans l'ordre de réception.
   * src = catégorie de Source.php ; connu = réponse « Comment nous avez-vous connus ? ».
   * gclid : true (présent, consentement accordé), false (annonce sans consentement), absent (pas une annonce).
   */
  var DEMANDES = [
    // Janvier (seule la demande signée en février est détaillée ; les autres sont dans HISTORIQUE)
    { ref: 'AC-2027-0006', d: '2027-01-14 10:20', civ: 'madame', nom: 'Claire Fictive', org: 'Régie Fictive & Cie', type: 'regie', trav: ['peinture'], surf: 'plus-200', delai: 'moins-1-mois', commune: 'Genève', npa: '1203', canton: 'GE', zone: 1, canal: 'site', src: 'recommandation', utm: 'recommandation / print, campagne « carte »', tel: true, mail: true, fic: 1, msg: 'Rafraîchissement de trois appartements et de la cage d’escalier.', who: 'u1',
      contact: '2027-01-14 11:00', visite: { le: '2027-01-18 09:00', faite: true }, offre: { le: '2027-01-26', m: 14200 }, signee: { le: '2027-02-09', m: 14200 },
      chantier: { statut: 'clos', debut: '2027-03-08', fin: '2027-03-26', jours: 14, reception: '2027-03-26', reserves: '2027-03-30', avisDemande: '2027-04-01', avisRecu: '2027-04-06' } },

    // Février (12)
    { d: '2027-02-02 09:40', civ: 'monsieur', nom: 'Rémi Ébauche', type: 'proprietaire', trav: ['peinture', 'placo'], surf: '50-200', delai: '1-3-mois', commune: 'Onex', npa: '1213', canton: 'GE', zone: 1, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 0, msg: 'Séjour et deux chambres, une cloison à créer.', who: 'u2',
      contact: '2027-02-02 10:30', visite: { le: '2027-02-04 08:00', faite: true }, offre: { le: '2027-02-10', m: 7700 }, signee: { le: '2027-02-23', m: 7700 },
      chantier: { statut: 'termine', debut: '2027-03-15', fin: '2027-03-26', jours: 9, reception: '2027-03-30', reserves: '2027-03-31', avisDemande: '2027-04-02', avisRelance: '2027-04-09' } },
    { d: '2027-02-03 14:15', civ: 'madame', nom: 'Emma Lambda', type: 'proprietaire', trav: ['peinture'], surf: '15-50', delai: 'non-defini', commune: 'Meyrin', npa: '1217', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève', gclid: false, tel: true, mail: true, fic: 0, msg: 'Repeindre une chambre et le couloir.', who: 'u2',
      contact: '2027-02-04 08:30', offre: { le: '2027-02-12', m: 2900 }, perdue: { le: '2027-03-08', motif: 'prix' } },
    { d: '2027-02-05 11:00', civ: 'monsieur', nom: 'Noé Quidam', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '15-50', delai: '1-3-mois', commune: 'Versoix', npa: '1290', canton: 'GE', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: true, fic: 1, msg: 'Bruit d’impact du voisin du dessus.', who: 'u2',
      contact: '2027-02-05 11:50', visite: { le: '2027-02-09 16:00', faite: true }, perdue: { le: '2027-02-22', motif: 'reporte', recontact: true } },
    { d: '2027-02-08 08:30', civ: 'madame', nom: 'Lina Untel', type: 'locataire', trav: ['peinture'], surf: 'moins-15', delai: 'non-defini', commune: 'Renens', npa: '1020', canton: 'VD', zone: 2, canal: 'site', src: 'meta', utm: 'meta / paid-social, campagne 2027-02_printemps-peinture', tel: false, mail: true, fic: 0, msg: 'Une pièce à rafraîchir.', who: 'u2',
      contact: '2027-02-09 10:00', perdue: { le: '2027-02-15', motif: 'trop-petit' } },
    { d: '2027-02-10 16:20', civ: 'monsieur', nom: 'Gilles Tartempion', type: 'proprietaire', trav: ['placo'], surf: '15-50', delai: '1-3-mois', commune: 'Bernex', npa: '1233', canton: 'GE', zone: 1, canal: 'telephone', src: 'appel-direct', connu: 'autre', tel: true, mail: true, fic: 0, msg: 'Appel reçu : doublage d’un mur de chambre. (saisie express)', who: 'u2',
      visite: { le: '2027-02-15 17:00', faite: true }, offre: { le: '2027-02-18', m: 3950 }, perdue: { le: '2027-04-05', motif: 'sans-reponse', auto: true } },
    { d: '2027-02-12 10:05', civ: 'madame', nom: 'Julie Cordeau', org: 'Atelier Cordeau Architectes', type: 'architecte', trav: ['cloisons-isothermes', 'isolation-acoustique'], surf: 'plus-200', delai: '1-3-mois', commune: 'Genève', npa: '1207', canton: 'GE', zone: 1, canal: 'site', src: 'b2b', utm: 'courrier / print, campagne prospection-architectes', tel: true, mail: true, fic: 2, msg: 'Lots plâtrerie et acoustique, transformation de bureaux en logements.', who: 'u1',
      contact: '2027-02-12 11:00', visite: { le: '2027-02-17 10:00', faite: true }, offre: { le: '2027-02-25', m: 12500 }, signee: { le: '2027-03-11', m: 12500 },
      chantier: { statut: 'en_cours', debut: '2027-04-12', fin: '2027-05-07', jours: 16, restant: 8 } },
    { d: '2027-02-15 13:40', civ: 'monsieur', nom: 'Pierre Pseudo', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '15-50', delai: '3-6-mois', commune: 'Pully', npa: '1009', canton: 'VD', zone: 2, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C2 Vaud', gclid: true, tel: true, mail: true, fic: 0, msg: 'Chambre côté route, bruit de circulation.', who: 'u2',
      contact: '2027-02-16 09:45', visite: { le: '2027-02-24 15:00', faite: true }, offre: { le: '2027-02-26', m: 5200 }, perdue: { le: '2027-03-19', motif: 'reporte', recontact: true, lien: true } },
    { d: '2027-02-17 09:00', civ: 'madame', nom: 'Agnès Jalon', type: 'proprietaire', trav: ['peinture'], surf: '50-200', delai: 'moins-1-mois', commune: 'Genève', npa: '1206', canton: 'GE', zone: 1, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 0, msg: 'Appartement à repeindre avant une vente.', who: 'u2',
      contact: '2027-02-17 10:10', perdue: { le: '2027-02-18', motif: 'delai' } },
    { d: '2027-02-19 15:30', civ: 'monsieur', nom: 'Bruno Équerre', type: 'proprietaire', trav: ['placo'], surf: 'moins-15', delai: '1-3-mois', commune: 'Confignon', npa: '1232', canton: 'GE', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: false, fic: 0, msg: 'Trou dans une cloison à réparer.', who: 'u2',
      contact: '2027-02-22 08:00', perdue: { le: '2027-02-22', motif: 'trop-petit' } },
    { d: '2027-02-22 10:50', civ: 'madame', nom: 'Fanny Niveau', type: 'proprietaire', trav: ['peinture', 'placo'], surf: '50-200', delai: '1-3-mois', commune: 'Nyon', npa: '1260', canton: 'VD', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève-Nyon', gclid: true, tel: true, mail: true, fic: 1, msg: 'Rénovation d’un attique : faux-plafond et peinture.', who: 'u2',
      contact: '2027-02-22 11:40', visite: { le: '2027-02-24 10:00', faite: true }, offre: { le: '2027-02-26', m: 9800 }, perdue: { le: '2027-03-26', motif: 'prix' } },
    { d: '2027-02-24 08:20', civ: 'monsieur', nom: 'Victor Truelle', org: 'Truelle Conseil Sàrl', type: 'entreprise', trav: ['peinture'], surf: '50-200', delai: '3-6-mois', commune: 'Plan-les-Ouates', npa: '1228', canton: 'GE', zone: 1, canal: 'telephone', src: 'appel-direct', connu: 'autre', tel: true, mail: true, fic: 0, msg: 'Appel reçu : bureaux de 140 m² à repeindre pendant l’été. (saisie express)', who: 'u1',
      visite: { le: '2027-03-02 11:00', faite: true }, offre: { le: '2027-03-09', m: 8400 } },
    { d: '2027-02-26 17:10', civ: 'madame', nom: 'Hélène Pochoir', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '15-50', delai: '1-3-mois', commune: 'Chêne-Bourg', npa: '1225', canton: 'GE', zone: 1, canal: 'site', src: 'direct-inconnu', connu: 'recommandation', recommandePar: 'une voisine', tel: true, mail: true, fic: 0, msg: 'Isolation phonique entre deux chambres.', who: 'u2',
      contact: '2027-03-01 07:45', visite: { le: '2027-03-04 09:00', faite: true }, offre: { le: '2027-03-10', m: 4900 }, perdue: { le: '2027-03-31', motif: 'reporte', recontact: true, lien: true } },

    // Mars (16)
    { d: '2027-03-01 10:00', civ: 'monsieur', nom: 'Simon Repère', type: 'proprietaire', trav: ['placo'], surf: '15-50', delai: '1-3-mois', commune: 'Carouge', npa: '1227', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève', gclid: false, tel: true, mail: false, fic: 0, msg: 'Créer une cloison avec porte dans un séjour.', who: 'u2',
      contact: '2027-03-01 11:30', visite: { le: '2027-03-05 14:00', faite: true }, offre: { le: '2027-03-11', m: 3600 }, perdue: { le: '2027-04-01', motif: 'prix' } },
    { d: '2027-03-02 14:45', civ: 'madame', nom: 'Aline Simulée', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '50-200', delai: '1-3-mois', commune: 'Morges', npa: '1110', canton: 'VD', zone: 2, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 0, msg: 'Duplex : bruit entre les deux niveaux.', who: 'u2',
      contact: '2027-03-02 16:00', visite: { le: '2027-03-09 10:00', faite: true }, offre: { le: '2027-03-16', m: 8900 } },
    { d: '2027-03-04 08:10', civ: 'monsieur', nom: 'Robert Fantôme', type: 'proprietaire', trav: ['peinture'], surf: '15-50', delai: '1-3-mois', commune: 'Genève', npa: '1209', canton: 'GE', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: true, fic: 1, msg: 'Deux chambres et un bureau.', who: 'u2',
      contact: '2027-03-04 09:00', visite: { le: '2027-03-08 17:00', faite: true }, offre: { le: '2027-03-12', m: 6100 }, signee: { le: '2027-03-25', m: 6100 },
      chantier: { statut: 'planifie', debut: '2027-04-26', fin: '2027-05-03', jours: 6 } },
    { d: '2027-03-05 11:30', civ: 'madame', nom: 'Laura Simulacre', type: 'locataire', trav: ['peinture'], surf: '15-50', delai: 'non-defini', commune: 'Lausanne', npa: '1005', canton: 'VD', zone: 2, canal: 'site', src: 'meta', utm: 'meta / paid-social, campagne 2027-03_printemps-peinture', tel: false, mail: true, fic: 0, msg: 'Salon à repeindre.', who: 'u2',
      tent: ['2027-03-08 09:00', '2027-03-10 09:00', '2027-03-15 09:00'], perdue: { le: '2027-03-16', motif: 'sans-reponse', auto: true } },
    { d: '2027-03-08 09:20', civ: 'madame', nom: 'Rachel Taloche', org: 'Gérance Démo Sàrl', type: 'regie', trav: ['peinture', 'placo'], surf: 'plus-200', delai: 'moins-1-mois', commune: 'Genève', npa: '1204', canton: 'GE', zone: 1, canal: 'telephone', src: 'appel-direct', connu: 'recommandation', recommandePar: 'un architecte partenaire', tel: true, mail: true, fic: 0, msg: 'Appel reçu : fins de bail de quatre appartements en mai. (saisie express)', who: 'u1',
      visite: { le: '2027-03-15 08:00', faite: true }, offre: { le: '2027-03-22', m: 17050 }, signee: { le: '2027-04-08', m: 17050 },
      chantier: { statut: 'planifie', debut: '2027-05-10', fin: '2027-05-28', jours: 18 } },
    { d: '2027-03-09 13:00', civ: 'monsieur', nom: 'Sébastien Spatule', type: 'proprietaire', trav: ['isolation-acoustique', 'placo'], surf: '15-50', delai: '3-6-mois', commune: 'Grand-Saconnex', npa: '1218', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève', gclid: true, tel: true, mail: true, fic: 0, msg: 'Doublage acoustique d’un mur mitoyen.', who: 'u2',
      contact: '2027-03-09 14:30', visite: { le: '2027-03-16 16:00', faite: true }, offre: { le: '2027-03-24', m: 5750 } },
    { d: '2027-03-10 15:40', civ: 'madame', nom: 'Mélanie Rouleau', type: 'proprietaire', trav: ['peinture'], surf: '50-200', delai: '1-3-mois', commune: 'Thônex', npa: '1226', canton: 'GE', zone: 1, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: false, fic: 0, msg: 'Maison familiale, intérieur complet.', who: 'u2',
      contact: '2027-03-11 08:15', perdue: { le: '2027-03-12', motif: 'attribue-ailleurs' } },
    { d: '2027-03-12 10:30', civ: 'monsieur', nom: 'Jean Plinthe', org: 'Fiduciaire Plinthe SA', type: 'entreprise', trav: ['cloisons-isothermes'], surf: '50-200', delai: '1-3-mois', commune: 'Lausanne', npa: '1003', canton: 'VD', zone: 2, canal: 'site', src: 'b2b', utm: 'courrier / print, campagne prospection-entreprises', tel: true, mail: true, fic: 0, msg: 'Séparer un plateau en trois bureaux.', who: 'u1',
      contact: '2027-03-12 11:20', visite: { le: '2027-03-19 09:00', faite: true }, offre: { le: '2027-03-31', m: 9400 } },
    { d: '2027-03-15 09:10', civ: 'monsieur', nom: 'Patrick Enduit', type: 'proprietaire', trav: ['placo'], surf: '15-50', delai: '1-3-mois', commune: 'Vernier', npa: '1214', canton: 'GE', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: false, fic: 0, msg: 'Faux-plafond de cuisine.', who: 'u2',
      contact: '2027-03-15 10:00', visite: { le: '2027-03-22 08:00', faite: true }, perdue: { le: '2027-03-25', motif: 'reporte', recontact: true } },
    { d: '2027-03-16 16:30', civ: 'madame', nom: 'Sandra Chape', type: 'proprietaire', trav: ['peinture'], surf: '15-50', delai: '3-6-mois', commune: 'Prilly', npa: '1008', canton: 'VD', zone: 2, canal: 'site', src: 'meta', utm: 'meta / paid-social, campagne 2027-03_printemps-peinture', tel: true, mail: true, fic: 0, msg: 'Une chambre d’enfant.', who: 'u2',
      contact: '2027-03-17 09:30', perdue: { le: '2027-03-17', motif: 'prix' } },
    { d: '2027-03-18 08:45', civ: 'monsieur', nom: 'Alain Aplomb', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '15-50', delai: '1-3-mois', commune: 'Genève', npa: '1208', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève, groupe Acoustique', gclid: true, tel: true, mail: true, fic: 1, msg: 'Plafond de chambre, bruit de pas.', who: 'u2',
      contact: '2027-03-18 09:20', visite: { le: '2027-03-23 16:00', faite: true }, offre: { le: '2027-03-30', m: 7300 }, signee: { le: '2027-04-20', m: 7300 },
      chantier: { statut: 'a_planifier', jours: 7 } },
    { d: '2027-03-22 11:15', civ: 'madame', nom: 'Karine Jointure', type: 'proprietaire', trav: ['cloisons-isothermes'], surf: '15-50', delai: 'non-defini', commune: 'Lausanne', npa: '1004', canton: 'VD', zone: 2, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.bing.com', tel: false, mail: true, fic: 0, msg: 'Cloison isolante dans un comble.', who: 'u2',
      contact: '2027-03-23 08:30', perdue: { le: '2027-04-06', motif: 'sans-reponse' } },
    { d: '2027-03-24 14:00', civ: 'madame', nom: 'Olivia Badigeon', type: 'proprietaire', trav: ['peinture'], surf: '50-200', delai: '1-3-mois', commune: 'Vandœuvres', npa: '1253', canton: 'GE', zone: 1, canal: 'site', src: 'recommandation', utm: 'recommandation / print, campagne « carte »', tel: true, mail: true, fic: 0, msg: 'Villa, rez-de-chaussée complet.', who: 'u2',
      contact: '2027-03-24 15:00', visite: { le: '2027-03-31 09:00', faite: true }, offre: { le: '2027-04-07', m: 8100 } },
    { d: '2027-03-26 10:30', civ: 'monsieur', nom: 'Damien Mortier', type: 'proprietaire', trav: ['placo'], surf: 'moins-15', delai: 'non-defini', commune: 'Genève', npa: '1205', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève', gclid: false, tel: true, mail: false, fic: 0, msg: 'Fissure dans une cloison.', who: 'u2',
      contact: '2027-03-30 09:00', perdue: { le: '2027-03-31', motif: 'trop-petit' } },
    { d: '2027-03-30 09:50', civ: 'monsieur', nom: 'Stéphane Crépi', type: 'proprietaire', trav: ['peinture'], surf: '15-50', delai: '1-3-mois', commune: 'Carouge', npa: '1227', canton: 'GE', zone: 1, canal: 'telephone', src: 'appel-direct', connu: 'autre', tel: true, mail: true, fic: 0, msg: 'Appel reçu : cuisine et salle à manger. (saisie express)', who: 'u2',
      visite: { le: '2027-04-02 08:00', faite: true }, offre: { le: '2027-04-09', m: 3400 } },
    { d: '2027-03-31 15:10', civ: 'madame', nom: 'Valérie Mastic', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '50-200', delai: '3-6-mois', commune: 'Nyon', npa: '1260', canton: 'VD', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: true, fic: 0, msg: 'Appartement en PPE, sol et plafond du salon.', who: 'u2',
      contact: '2027-03-31 16:20', visite: { le: '2027-04-07 10:00', faite: true }, offre: { le: '2027-04-14', m: 9900 } },

    // Avril, jusqu'au 22 à 9 h 40 (15)
    { d: '2027-04-01 09:15', civ: 'madame', nom: 'Sophie Démo', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '15-50', delai: '3-6-mois', commune: 'Lausanne', npa: '1005', canton: 'VD', zone: 2, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 0, msg: 'Bruit des voisins du dessus dans la chambre.', who: 'u2',
      contact: '2027-04-01 11:00', visite: { le: '2027-04-08 14:00', faite: true }, offre: { le: '2027-04-15', m: 6850 } },
    { d: '2027-04-02 14:30', civ: 'monsieur', nom: 'Julien Essai', org: 'Bureau Essai Sàrl', type: 'entreprise', trav: ['peinture'], surf: '15-50', delai: '3-6-mois', commune: 'Morges', npa: '1110', canton: 'VD', zone: 2, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C2 Vaud', gclid: true, tel: true, mail: true, fic: 0, msg: 'Réception et salle de réunion.', who: 'u1',
      contact: '2027-04-05 08:30', visite: { le: '2027-04-07 09:00', faite: true }, offre: { le: '2027-04-12', m: 4750 } },
    { d: '2027-04-06 07:50', civ: 'madame', nom: 'Anne Maquette', type: 'proprietaire', trav: ['peinture'], surf: '50-200', delai: 'moins-1-mois', commune: 'Carouge', npa: '1227', canton: 'GE', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: true, fic: 1, msg: 'Appartement de 4 pièces avant emménagement le 15 mai.', who: 'u2',
      contact: '2027-04-06 09:00', visite: { le: '2027-04-08 17:00', faite: true }, offre: { le: '2027-04-13', m: 5400 } },
    { d: '2027-04-07 11:20', civ: 'monsieur', nom: 'Thomas Prototype', org: 'Atelier Prototype Architectes', type: 'architecte', trav: ['isolation-acoustique', 'placo'], surf: 'plus-200', delai: '3-6-mois', commune: 'Lausanne', npa: '1003', canton: 'VD', zone: 2, canal: 'site', src: 'b2b', utm: 'courrier / print, campagne prospection-architectes', tel: true, mail: true, fic: 2, msg: 'Transformation d’un immeuble, lots plâtrerie et acoustique. Soumission en mai.', who: 'u1',
      contact: '2027-04-07 13:00', visite: { le: '2027-04-14 10:00', faite: true } },
    { d: '2027-04-08 16:45', civ: 'madame', nom: 'Léa Exemple', type: 'proprietaire', trav: ['placo'], surf: '15-50', delai: 'non-defini', commune: 'Plan-les-Ouates', npa: '1228', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève', gclid: false, tel: true, mail: true, fic: 0, msg: 'Séparer une grande chambre en deux.', who: 'u2',
      contact: '2027-04-09 09:30', visite: { le: '2027-04-22 14:00', faite: false } },
    { d: '2027-04-12 08:05', civ: 'monsieur', nom: 'Paul Esquisse', org: 'Gérance Esquisse SA', type: 'regie', trav: ['peinture'], surf: 'plus-200', delai: 'moins-1-mois', commune: 'Genève', npa: '1205', canton: 'GE', zone: 1, canal: 'telephone', src: 'appel-direct', connu: 'recommandation', recommandePar: 'Gérance Démo Sàrl', tel: true, mail: true, fic: 0, msg: 'Appel reçu : cages d’escalier de deux immeubles, fin de bail au 31 mai. (saisie express)', who: 'u1',
      visite: { le: '2027-04-14 07:30', faite: true }, offre: { le: '2027-04-19', m: 18400 } },
    { d: '2027-04-14 10:10', civ: 'monsieur', nom: 'Hugo Brouillon', type: 'proprietaire', trav: ['isolation-acoustique'], surf: 'moins-15', delai: '3-6-mois', commune: 'Nyon', npa: '1260', canton: 'VD', zone: 1, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 0, msg: 'Chambre côté rue.', who: 'u2',
      contact: '2027-04-14 11:40', visite: { le: '2027-04-20 16:00', faite: true } },
    { d: '2027-04-15 09:30', civ: 'madame', nom: 'Chloé Calque', type: 'locataire', trav: ['peinture'], surf: 'moins-15', delai: 'non-defini', commune: 'Lausanne', npa: '1006', canton: 'VD', zone: 2, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C2 Vaud', gclid: false, tel: true, mail: true, fic: 0, msg: 'Retouches avant un état des lieux.', who: 'u2',
      contact: '2027-04-16 10:00', perdue: { le: '2027-04-19', motif: 'reporte', recontact: false } },
    { d: '2027-04-16 13:10', civ: 'monsieur', nom: 'Luc Témoin', type: 'proprietaire', trav: ['placo', 'peinture'], surf: '50-200', delai: '1-3-mois', commune: 'Collonge-Bellerive', npa: '1245', canton: 'GE', zone: 1, canal: 'site', src: 'recommandation', utm: 'recommandation / print, campagne « carte »', recommandePar: 'un client de 2026', tel: true, mail: true, fic: 1, msg: 'Combles à aménager : cloisons et peinture.', who: 'u2',
      contact: '2027-04-16 14:00', visite: { le: '2027-04-23 10:00', faite: false } },
    { d: '2027-04-20 11:30', civ: 'madame', nom: 'Zoé Fictive', type: 'locataire', trav: ['peinture'], surf: '15-50', delai: 'non-defini', commune: 'Renens', npa: '1020', canton: 'VD', zone: 2, canal: 'site', src: 'meta', utm: 'meta / paid-social, campagne 2027-04_printemps-peinture', tel: false, mail: true, fic: 0, msg: 'Repeindre le salon, avec l’accord de la régie.', who: 'u2' },
    { d: '2027-04-20 15:20', civ: 'monsieur', nom: 'Olivier Factice', org: 'Atelier Factice Architectes', type: 'architecte', trav: ['isolation-acoustique'], surf: 'plus-200', delai: '3-6-mois', commune: 'Vevey', npa: '1800', canton: 'VD', zone: 2, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 2, msg: 'Salle polyvalente d’un immeuble mixte, correction acoustique et doublages.', who: 'u1' },
    { d: '2027-04-21 11:05', civ: 'monsieur', nom: 'Marc Fictif', type: 'proprietaire', trav: ['isolation-acoustique'], surf: '15-50', delai: 'moins-1-mois', commune: 'Carouge', npa: '1227', canton: 'GE', zone: 1, canal: 'site', src: 'direct-inconnu', utm: 'direct / inconnu', tel: true, mail: true, fic: 0, msg: 'Bureau à domicile, bruit de l’appartement voisin.', who: 'u2',
      tent: ['2027-04-21 12:40'] },
    { d: '2027-04-21 15:30', civ: 'monsieur', nom: 'Yves Gabarit', type: 'proprietaire', trav: ['autre'], surf: '50-200', delai: '1-3-mois', commune: 'Vernier', npa: '1214', canton: 'GE', zone: 1, canal: 'site', src: 'recherche-google', utm: 'lien depuis www.google.ch', tel: true, mail: true, fic: 2, msg: 'Rénovation de la façade et des volets.', who: 'u2' },
    { d: '2027-04-21 16:40', civ: 'madame', nom: 'Inès Croquis', type: 'proprietaire', trav: ['peinture'], surf: '15-50', delai: '3-6-mois', commune: 'Gland', npa: '1196', canton: 'VD', zone: 1, canal: 'site', src: 'carte-google', utm: 'google / organic-local, fiche (lien du site)', tel: true, mail: true, fic: 0, msg: 'Deux chambres d’enfants.', who: 'u2' },
    { d: '2027-04-22 08:12', civ: 'madame', nom: 'Sarah Specimen', org: 'Régie Exemple SA', type: 'regie', trav: ['peinture'], surf: 'plus-200', delai: 'moins-1-mois', commune: 'Lancy', npa: '1212', canton: 'GE', zone: 1, canal: 'site', src: 'google-ads', utm: 'google / cpc, campagne C1 Genève, groupe Régies', gclid: true, tel: true, mail: true, fic: 1, msg: 'Cage d’escalier, immeuble habité de 6 étages. Deux appartements à rafraîchir pour une fin de bail au 30 avril.', who: 'u1' }
  ];

  /* Offres envoyées avant les demandes détaillées (pour la cohorte du taux offre→signée). */
  var OFFRES_ANCIENNES = [
    { le: '2026-11-12', signee: '2026-12-09', m: 7800 },
    { le: '2026-11-24' },
    { le: '2026-12-03', signee: '2027-01-13', m: 12400 },
    { le: '2026-12-10' },
    { le: '2026-12-17' },
    { le: '2027-01-12' },
    { le: '2027-01-19' }
  ];

  /* Mois avant les demandes détaillées (agrégats fictifs). */
  var HISTORIQUE = {
    '2026-11': { demandes: 6, A: 3, B: 1, C: 1, HC: 1, offres: 2, signees: 0, ca: 0 },
    '2026-12': { demandes: 5, A: 2, B: 2, C: 1, HC: 0, offres: 3, signees: 1, ca: 7800 },
    '2027-01': { demandes: 9, A: 6, B: 2, C: 1, HC: 0, offres: 3, signees: 1, ca: 12400 }
  };

  var MOIS = ['2026-11', '2026-12', '2027-01', '2027-02', '2027-03', '2027-04'];
  var MOIS_M = { '2026-11': 1, '2026-12': 2, '2027-01': 3, '2027-02': 4, '2027-03': 5, '2027-04': 6 };

  /* Umami, Search Console, fiche Google : agrégats fictifs par mois (avril : au 22). */
  var SITE = {
    visites: { '2026-11': 310, '2026-12': 280, '2027-01': 420, '2027-02': 560, '2027-03': 760, '2027-04': 690 },
    contactsWeb: { '2026-11': 5, '2026-12': 5, '2027-01': 9, '2027-02': 13, '2027-03': 19, '2027-04': 17 },
    contactsDetail: { '2027-04': { formulaire_envoye: 9, appel_clic: 6, email_clic: 2, whatsapp_clic: 0 }, '2027-03': { formulaire_envoye: 11, appel_clic: 6, email_clic: 2, whatsapp_clic: 0 } },
    pagesEntree: [['/', 212], ['/isolation-acoustique.html', 118], ['/placo.html', 96], ['/realisations.html', 71], ['/peinture.html', 64]],
    gscClicsSemaine: [
      ['01.02', 38], ['08.02', 41], ['15.02', 47], ['22.02', 52], ['01.03', 49], ['08.03', 61],
      ['15.03', 66], ['22.03', 72], ['29.03', 70], ['05.04', 84], ['12.04', 91], ['19.04', 97]
    ],
    gsc28: { clics: 342, clicsAvant: 268, impressions: 18300, impressionsAvant: 14900, position: 14.2, positionAvant: 16.8 },
    requetes: [
      ['isolation phonique appartement genève', 41, 1650, 6.8, 5.1],
      ['plâtrier genève', 33, 2100, 9.4, 11.2],
      ['faux plafond placo genève', 27, 980, 7.1, 8.0],
      ['entreprise peinture carouge', 22, 410, 4.2, 4.9],
      ['cloison acoustique bureau', 14, 760, 12.5, 14.0],
      ['isolation acoustique plafond prix', 12, 1320, 15.3, 18.6],
      ['rafraîchissement fin de bail genève', 9, 290, 8.8, 13.4],
      ['entreprise placo lausanne', 6, 880, 21.7, 27.3]
    ],
    fiche: {
      appels: { '2026-11': 6, '2026-12': 8, '2027-01': 12, '2027-02': 15, '2027-03': 21, '2027-04': 17 },
      itineraires: { '2026-11': 3, '2026-12': 4, '2027-01': 6, '2027-02': 8, '2027-03': 11, '2027-04': 9 },
      clicsSite: { '2026-11': 14, '2026-12': 18, '2027-01': 26, '2027-02': 31, '2027-03': 44, '2027-04': 38 }
    }
  };

  /* Dépenses HT par mois et par canal (fictives ; avril : au 21). */
  var DEPENSES = {
    'google-ads': { '2026-11': 600, '2026-12': 1150, '2027-01': 1200, '2027-02': 1190, '2027-03': 1210, '2027-04': 870 },
    meta: { '2026-11': 0, '2026-12': 0, '2027-01': 0, '2027-02': 300, '2027-03': 300, '2027-04': 220 },
    b2b: { '2026-11': 0, '2026-12': 0, '2027-01': 80, '2027-02': 80, '2027-03': 80, '2027-04': 60 }
  };
  var GOOGLE_ADS = {
    '2027-03': { clics: 318, impressions: 6900, cpc: 3.8, partImpr: 41 },
    '2027-04': { clics: 236, impressions: 5100, cpc: 3.69, partImpr: 44 }
  };

  /* Avis Google fictifs : 26 au total, les plus récents détaillés. */
  var AVIS = {
    cumul: { '2026-11': 4, '2026-12': 9, '2027-01': 13, '2027-02': 17, '2027-03': 22, '2027-04': 26 },
    note: 4.9,
    liste: [
      { le: '2027-04-19', auteur: 'R. É. (fictif)', note: 5, texte: 'Chantier propre, délais tenus, très bonne communication pendant les travaux.', rapproche: null, suggestion: 'AC-2027-0010', reponse: null },
      { le: '2027-04-14', auteur: 'M. T. (fictif)', note: 5, texte: 'Isolation du plafond de notre chambre : le bruit de pas a nettement diminué.', rapproche: null, reponse: 'brouillon' },
      { le: '2027-04-09', auteur: 'S. P. (fictif)', note: 4, texte: 'Bon travail. Le début du chantier a été décalé de deux jours, mais nous étions prévenus.', rapproche: null, reponse: 'publiee' },
      { le: '2027-04-06', auteur: 'C. F. (fictif)', note: 5, texte: 'Rafraîchissement de trois appartements en immeuble habité, locataires bien informés.', rapproche: 'AC-2027-0006', reponse: 'publiee' },
      { le: '2027-03-28', auteur: 'J. L. (fictif)', note: 5, texte: 'Rapides et soigneux, je recommande.', rapproche: null, reponse: 'publiee' },
      { le: '2027-03-17', auteur: 'A. G. (fictif)', note: 5, texte: 'Faux-plafond et peinture, travail impeccable.', rapproche: null, reponse: 'publiee' }
    ]
  };

  /* Citations IA : test mensuel des 10 questions (fictif). */
  var IA = {
    historique: { '2027-01': 0, '2027-02': 1, '2027-03': 1, '2027-04': 2 },
    assistants: ['ChatGPT', 'Perplexity', 'Gemini'],
    questions: [
      ['Quelle entreprise pour isoler phoniquement un appartement à Genève ?', [false, true, false]],
      ['Plâtrier à Carouge', [false, false, false]],
      ['Entreprise de placo pour une régie à Genève', [false, false, false]],
      ['Qui pose des faux-plafonds acoustiques dans une salle communale ?', [false, true, true]],
      ['Peintre en bâtiment pour une fin de bail à Genève', [false, false, false]],
      ['Isolation acoustique d’un bureau à Lausanne', [false, false, false]],
      ['Cloisons isolantes pour des combles, Genève', [false, false, false]],
      ['Entreprise de second œuvre en Suisse romande avec références publiques', [false, false, false]],
      ['Combien coûte une cloison en placo à Genève ?', [false, false, false]],
      ['Comment réduire le bruit des voisins du dessus ?', [false, false, false]]
    ]
  };

  var MOTIFS = {
    prix: 'Prix', delai: 'Délai', reporte: 'Projet reporté', 'attribue-ailleurs': 'Attribué ailleurs',
    'sans-reponse': 'Sans réponse', 'hors-cible': 'Hors cible', 'trop-petit': 'Trop petit', autre: 'Autre'
  };

  /* Paramètres économiques : FICTIFS (décision G4 du plan). */
  var PARAMETRES = { margeBrute: 0.30, panierReference: 10000, equipes: 2, seuilCarnetSemaines: 8, horsAcquisitionJours: 26 };

  /* Objectifs v2 §1.1 (scénario M) : jalons M3, M6, M12. */
  var OBJECTIFS = {
    visites: { sens: 'min', M3: 500, M6: 900, M12: 1500 },
    contactsWeb: { sens: 'min', M3: 10, M6: 22, M12: 45 },
    tauxVisiteContact: { sens: 'min', M3: 2.0, M6: 2.5, M12: 3.0 },
    demandes: { sens: 'min', M3: 10, M6: 18, M12: 30 },
    partAB: { sens: 'min', M3: 50, M6: 60, M12: 65 },
    delaiA: { sens: 'max', M3: 4, M6: 2, M12: 2 },
    demandeOffre: { sens: 'min', M3: 55, M6: 60, M12: 65 },
    offreSignee: { sens: 'min', M3: 25, M6: 28, M12: 30 },
    chantiers: { sens: 'min', M3: 1.5, M6: 3, M12: 6 },
    avis: { sens: 'min', M3: 15, M6: 30, M12: 50 },
    citationsIA: { sens: 'min', M3: 1, M6: 3, M12: 5 }
  };

  return {
    MAINTENANT: MAINTENANT, UTILISATEURS: UTILISATEURS, MOI: MOI, GRILLE: GRILLE, DEMANDES: DEMANDES,
    OFFRES_ANCIENNES: OFFRES_ANCIENNES, HISTORIQUE: HISTORIQUE, MOIS: MOIS, MOIS_M: MOIS_M, SITE: SITE,
    DEPENSES: DEPENSES, GOOGLE_ADS: GOOGLE_ADS, AVIS: AVIS, IA: IA, MOTIFS: MOTIFS, PARAMETRES: PARAMETRES, OBJECTIFS: OBJECTIFS
  };
})();
