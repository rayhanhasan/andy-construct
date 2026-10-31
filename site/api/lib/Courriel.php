<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

use PHPMailer\PHPMailer\PHPMailer;

/**
 * Envoi des e-mails : SMTP authentifié (PHPMailer), repli sur mail() si le
 * SMTP échoue, puis mise de côté pour un nouvel essai par cron.php.
 * En mode test, aucun envoi : le message complet (MIME) est écrit dans
 * stockage/test-mails/.
 *
 * Sécurité des en-têtes : sujet et noms nettoyés (aucun retour à la ligne),
 * adresses validées en amont, et PHPMailer encode et contrôle chaque en-tête.
 */
final class Courriel
{
    public function __construct(
        private Config $config,
        private Stockage $stockage,
        private Journal $journal
    ) {
    }

    /** @return array{ok: bool, transport: string, fichier?: string} */
    public function envoyer(Message $m, bool $mettreDeCoteSiEchec = true): array
    {
        $m->sujet = Message::entete($m->sujet);
        if ($m->a === []) {
            return ['ok' => false, 'transport' => 'aucun-destinataire'];
        }

        if ($this->config->modeTest()) {
            $fichier = $this->ecrireFichier($m);
            return ['ok' => true, 'transport' => 'fichier', 'fichier' => $fichier];
        }

        $transports = [];
        if (class_exists(PHPMailer::class)) {
            if ($this->config->get('smtp.actif') && $this->config->get('smtp.hote')) {
                $transports[] = 'smtp';
            }
            if ($this->config->get('repli_mail', true)) {
                $transports[] = 'mail';
            }
        } elseif ($this->config->get('repli_mail', true)) {
            $transports[] = 'mail-natif';
        }

        foreach ($transports as $transport) {
            try {
                if ($transport === 'mail-natif') {
                    $ok = $this->envoyerNatif($m);
                } else {
                    $mailer = $this->construire($m, $transport);
                    $ok = $mailer->send();
                }
                if ($ok) {
                    if ($transport !== 'smtp') {
                        $this->journal->alerte('courriel_repli', ['ref' => $m->ref, 'categorie' => $m->categorie, 'transport' => $transport]);
                    }
                    return ['ok' => true, 'transport' => $transport];
                }
            } catch (\Throwable $e) {
                $this->journal->erreur('courriel_echec', [
                    'ref' => $m->ref, 'categorie' => $m->categorie, 'transport' => $transport,
                    'erreur' => Journal::nettoyerMessage($e->getMessage()),
                ]);
            }
        }

        if ($mettreDeCoteSiEchec) {
            $this->mettreDeCote($m);
        }
        return ['ok' => false, 'transport' => 'echec'];
    }

    /** Construit l'objet PHPMailer (aussi utilisé pour produire le MIME en mode test). */
    private function construire(Message $m, string $transport): PHPMailer
    {
        $mail = new PHPMailer(true);
        $mail->CharSet = PHPMailer::CHARSET_UTF8;
        $mail->Encoding = PHPMailer::ENCODING_QUOTED_PRINTABLE;
        $mail->XMailer = ' ';
        $mail->setLanguage('fr', dirname(__DIR__) . '/vendor/phpmailer/phpmailer/language/');

        if ($transport === 'smtp') {
            $mail->isSMTP();
            $mail->Host = (string) $this->config->get('smtp.hote');
            $mail->Port = (int) $this->config->get('smtp.port', 587);
            $mail->Timeout = (int) $this->config->get('smtp.delai', 10);
            $securite = (string) $this->config->get('smtp.securite', 'tls');
            $mail->SMTPSecure = $securite === 'ssl' ? PHPMailer::ENCRYPTION_SMTPS : ($securite === 'tls' ? PHPMailer::ENCRYPTION_STARTTLS : '');
            $mail->SMTPAutoTLS = $securite !== 'aucune';
            $utilisateur = (string) $this->config->get('smtp.utilisateur', '');
            if ($utilisateur !== '') {
                $mail->SMTPAuth = true;
                $mail->Username = $utilisateur;
                $mail->Password = (string) $this->config->get('smtp.mot_de_passe', '');
            }
        } else {
            $mail->isMail();
        }

        $de = (string) $this->config->get('expediteur.email');
        $mail->setFrom($de, Message::entete((string) $this->config->get('expediteur.nom', 'Andy Construct'), 80));
        $mail->Sender = $de; // enveloppe (retours) sur le domaine, alignée SPF
        foreach ($m->a as [$adresse, $nom]) {
            $mail->addAddress($adresse, Message::entete($nom, 80));
        }
        if ($m->repondreA !== null && $m->repondreA[0] !== '') {
            $mail->addReplyTo($m->repondreA[0], Message::entete($m->repondreA[1] ?? '', 80));
        }
        $mail->Subject = $m->sujet;
        $mail->addCustomHeader('Auto-Submitted', 'auto-generated');
        $mail->addCustomHeader('X-Auto-Response-Suppress', 'All');
        if ($m->ref !== '') {
            $mail->addCustomHeader('X-AC-Ref', Message::entete($m->ref, 40));
        }
        if ($m->html !== null) {
            $mail->isHTML(true);
            $mail->Body = $m->html;
            $mail->AltBody = $m->texte;
        } else {
            $mail->isHTML(false);
            $mail->Body = $m->texte;
        }
        foreach ($m->pieces as $p) {
            if (is_file($p['chemin'])) {
                $mail->addAttachment($p['chemin'], Message::entete($p['nom'], 100), PHPMailer::ENCODING_BASE64, $p['type']);
            }
        }
        return $mail;
    }

    /** Repli sans PHPMailer : texte brut, en-têtes construits et encodés à la main. */
    private function envoyerNatif(Message $m): bool
    {
        $de = (string) $this->config->get('expediteur.email');
        $nomDe = Message::entete((string) $this->config->get('expediteur.nom', 'Andy Construct'), 80);
        $destinataires = implode(', ', array_map(
            static fn ($d) => $d[0],
            array_filter($m->a, static fn ($d) => Validateur::normaliserEmail($d[0]) !== null)
        ));
        if ($destinataires === '') {
            return false;
        }
        $entetes = [
            'From: ' . mb_encode_mimeheader($nomDe, 'UTF-8', 'Q') . " <$de>",
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit',
            'Auto-Submitted: auto-generated',
        ];
        if ($m->repondreA !== null && Validateur::normaliserEmail($m->repondreA[0]) !== null) {
            $entetes[] = 'Reply-To: ' . $m->repondreA[0];
        }
        $texte = $m->texte;
        if ($m->pieces !== []) {
            $texte .= "\n\n(Pièces jointes non incluses dans cet envoi de secours : voir le stockage privé ou le CRM.)";
        }
        $parametres = Validateur::normaliserEmail($de) !== null ? '-f' . $de : '';
        return mail($destinataires, mb_encode_mimeheader($m->sujet, 'UTF-8', 'Q'), $texte, implode("\r\n", $entetes), $parametres);
    }

    private function ecrireFichier(Message $m): string
    {
        $dossier = $this->stockage->dossier('test-mails');
        $nom = sprintf('%s-%s-%s.eml', date('Ymd-His'), preg_replace('/[^a-z0-9-]/', '', $m->categorie), bin2hex(random_bytes(3)));
        if (class_exists(PHPMailer::class)) {
            $mail = $this->construire($m, 'mail');
            $mail->preSend();
            $contenu = $mail->getSentMIMEMessage();
        } else {
            $contenu = 'To: ' . implode(', ', array_column($m->a, 0)) . "\r\nSubject: " . $m->sujet . "\r\n\r\n" . $m->texte;
        }
        $this->stockage->ecrireAtomique($dossier . '/' . $nom, $contenu);
        return $dossier . '/' . $nom;
    }

    private function mettreDeCote(Message $m): void
    {
        try {
            $fichier = $this->stockage->dossier('mails-echec') . '/' . date('Ymd-His') . '-' . bin2hex(random_bytes(4)) . '.json';
            $this->stockage->ecrireAtomique($fichier, (string) json_encode($m->versTableau(), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
            @chmod($fichier, 0600);
            $this->journal->alerte('courriel_mis_de_cote', ['ref' => $m->ref, 'categorie' => $m->categorie]);
        } catch (\Throwable $e) {
            $this->journal->erreur('courriel_perdu', ['ref' => $m->ref, 'categorie' => $m->categorie]);
        }
    }

    /** Nouvel essai des e-mails mis de côté (appelé par cron.php). */
    public function reessayer(int $max = 20): array
    {
        $bilan = ['envoyes' => 0, 'echecs' => 0];
        $fichiers = glob($this->stockage->dossier('mails-echec') . '/*.json') ?: [];
        sort($fichiers);
        foreach (array_slice($fichiers, 0, $max) as $fichier) {
            $donnees = json_decode((string) file_get_contents($fichier), true);
            if (!is_array($donnees)) {
                @unlink($fichier);
                continue;
            }
            $resultat = $this->envoyer(Message::depuisTableau($donnees), false);
            if ($resultat['ok']) {
                @unlink($fichier);
                $bilan['envoyes']++;
            } else {
                $bilan['echecs']++;
            }
        }
        return $bilan;
    }
}
