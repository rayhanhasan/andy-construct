<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/**
 * Heures ouvrables (lundi-vendredi, 7 h-18 h par défaut), jours fériés du
 * canton de Genève et calcul des délais de premier contact (§2.4).
 */
final class HeuresOuvrables
{
    private const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
    private const MOIS = ['', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
        'août', 'septembre', 'octobre', 'novembre', 'décembre'];

    private \DateTimeZone $tz;

    /** @param list<string> $joursFermes dates AAAA-MM-JJ supplémentaires (vacances du bâtiment…) */
    public function __construct(
        private int $debut = 7,
        private int $fin = 18,
        private array $joursFermes = []
    ) {
        $this->tz = new \DateTimeZone('Europe/Zurich');
    }

    public static function depuisConfig(Config $config): self
    {
        return new self(
            (int) $config->get('heures_ouvrables.debut', 7),
            (int) $config->get('heures_ouvrables.fin', 18),
            (array) $config->get('heures_ouvrables.jours_fermes', [])
        );
    }

    /** Jours fériés officiels du canton de Genève pour une année (AAAA-MM-JJ). */
    public static function feriesGeneve(int $annee): array
    {
        $paques = self::paques($annee);
        $plus = static fn (int $jours): string => $paques->modify("+$jours days")->format('Y-m-d');
        // Jeûne genevois : jeudi qui suit le premier dimanche de septembre.
        $premierDimanche = new \DateTimeImmutable("first sunday of september $annee");
        return [
            "$annee-01-01",                 // Nouvel An
            $plus(-2),                      // Vendredi saint
            $plus(1),                       // Lundi de Pâques
            $plus(39),                      // Ascension
            $plus(50),                      // Lundi de Pentecôte
            "$annee-08-01",                 // Fête nationale
            $premierDimanche->modify('+4 days')->format('Y-m-d'), // Jeûne genevois
            "$annee-12-25",                 // Noël
            "$annee-12-31",                 // Restauration de la République
        ];
    }

    /** Dimanche de Pâques (algorithme de Meeus/Jones/Butcher, calendrier grégorien). */
    public static function paques(int $annee): \DateTimeImmutable
    {
        $a = $annee % 19;
        $b = intdiv($annee, 100);
        $c = $annee % 100;
        $d = intdiv($b, 4);
        $e = $b % 4;
        $f = intdiv($b + 8, 25);
        $g = intdiv($b - $f + 1, 3);
        $h = (19 * $a + $b - $d - $g + 15) % 30;
        $i = intdiv($c, 4);
        $k = $c % 4;
        $l = (32 + 2 * $e + 2 * $i - $h - $k) % 7;
        $m = intdiv($a + 11 * $h + 22 * $l, 451);
        $mois = intdiv($h + $l - 7 * $m + 114, 31);
        $jour = (($h + $l - 7 * $m + 114) % 31) + 1;
        return new \DateTimeImmutable(sprintf('%04d-%02d-%02d', $annee, $mois, $jour), new \DateTimeZone('Europe/Zurich'));
    }

    public function estJourOuvrable(\DateTimeImmutable $date): bool
    {
        $date = $date->setTimezone($this->tz);
        if ((int) $date->format('N') >= 6) {
            return false;
        }
        $jour = $date->format('Y-m-d');
        return !in_array($jour, self::feriesGeneve((int) $date->format('Y')), true)
            && !in_array($jour, $this->joursFermes, true);
    }

    /** Prochain instant ouvrable (lui-même s'il l'est déjà). */
    public function prochainInstantOuvrable(\DateTimeImmutable $t): \DateTimeImmutable
    {
        $t = $t->setTimezone($this->tz);
        for ($i = 0; $i < 30; $i++) {
            $ouverture = $t->setTime($this->debut, 0);
            $fermeture = $t->setTime($this->fin, 0);
            if ($this->estJourOuvrable($t)) {
                if ($t < $ouverture) {
                    return $ouverture;
                }
                if ($t < $fermeture) {
                    return $t;
                }
            }
            $t = $t->modify('+1 day')->setTime($this->debut, 0);
        }
        return $t;
    }

    /** Ajoute des minutes ouvrables à un instant. */
    public function ajouterMinutesOuvrables(\DateTimeImmutable $depart, int $minutes): \DateTimeImmutable
    {
        $t = $this->prochainInstantOuvrable($depart);
        $restant = $minutes;
        for ($i = 0; $i < 60 && $restant > 0; $i++) {
            $fermeture = $t->setTime($this->fin, 0);
            $disponible = intdiv($fermeture->getTimestamp() - $t->getTimestamp(), 60);
            if ($restant <= $disponible) {
                return $t->modify("+$restant minutes");
            }
            $restant -= $disponible;
            $t = $this->prochainInstantOuvrable($fermeture->modify('+1 minute'));
        }
        return $t;
    }

    /** Minutes ouvrables écoulées entre deux instants (0 si $fin précède $debut). */
    public function minutesOuvrables(\DateTimeImmutable $debut, \DateTimeImmutable $fin): int
    {
        $debut = $debut->setTimezone($this->tz);
        $fin = $fin->setTimezone($this->tz);
        if ($fin <= $debut) {
            return 0;
        }
        $total = 0;
        $jour = $debut->setTime(0, 0);
        for ($i = 0; $i < 3700 && $jour <= $fin; $i++) {
            if ($this->estJourOuvrable($jour)) {
                $a = max($jour->setTime($this->debut, 0)->getTimestamp(), $debut->getTimestamp());
                $b = min($jour->setTime($this->fin, 0)->getTimestamp(), $fin->getTimestamp());
                if ($b > $a) {
                    $total += intdiv($b - $a, 60);
                }
            }
            $jour = $jour->modify('+1 day');
        }
        return $total;
    }

    /** Nombre de jours ouvrables d'un mois (AAAA-MM), et ceux écoulés jusqu'à $jusqua inclus. */
    public function joursOuvrablesMois(string $mois, ?\DateTimeImmutable $jusqua = null): int
    {
        $jour = new \DateTimeImmutable($mois . '-01 00:00', $this->tz);
        $n = 0;
        while ($jour->format('Y-m') === $mois) {
            if ($jusqua !== null && $jour->format('Y-m-d') > $jusqua->setTimezone($this->tz)->format('Y-m-d')) {
                break;
            }
            if ($this->estJourOuvrable($jour)) {
                $n++;
            }
            $jour = $jour->modify('+1 day');
        }
        return $n;
    }

    /** Prochain jour ouvrable strictement après la date donnée, à l'heure indiquée. */
    public function jourOuvrableSuivant(\DateTimeImmutable $t, int $heure): \DateTimeImmutable
    {
        $t = $t->setTimezone($this->tz)->modify('+1 day');
        for ($i = 0; $i < 30 && !$this->estJourOuvrable($t); $i++) {
            $t = $t->modify('+1 day');
        }
        return $t->setTime($heure, 0);
    }

    /**
     * Échéance de premier contact selon la priorité (strategie §2.4) :
     * A : 2 h ouvrables ; B : le jour même si reçu avant 14 h, sinon le
     * lendemain ouvrable à 10 h ; C : 2 jours ouvrables ; hors cible : 1 jour ouvrable.
     */
    public function echeance(string $priorite, \DateTimeImmutable $recu): \DateTimeImmutable
    {
        $recu = $recu->setTimezone($this->tz);
        return match ($priorite) {
            'A' => $this->ajouterMinutesOuvrables($recu, 120),
            'B' => ($this->estJourOuvrable($recu) && (int) $recu->format('G') < 14)
                ? $recu->setTime($this->fin, 0)
                : $this->jourOuvrableSuivant($recu, 10),
            'C' => $this->ajouterMinutesOuvrables($recu, 2 * ($this->fin - $this->debut) * 60),
            default => $this->ajouterMinutesOuvrables($recu, ($this->fin - $this->debut) * 60),
        };
    }

    /**
     * Formulation honnête de l'échéance pour le prospect :
     * « aujourd'hui avant 16 h 30 », « demain avant 10 h », « lundi avant 9 h 15 ».
     * L'heure est arrondie au quart d'heure supérieur.
     */
    public function formulerEcheance(\DateTimeImmutable $echeance, \DateTimeImmutable $maintenant): string
    {
        $echeance = $echeance->setTimezone($this->tz);
        $maintenant = $maintenant->setTimezone($this->tz);
        $minutes = (int) $echeance->format('i');
        if ($minutes % 15 !== 0) {
            $echeance = $echeance->modify('+' . (15 - $minutes % 15) . ' minutes');
        }
        $heure = self::heure($echeance);
        $ecartJours = (int) $maintenant->setTime(0, 0)->diff($echeance->setTime(0, 0))->format('%r%a');
        return match (true) {
            $ecartJours <= 0 => "aujourd'hui avant $heure",
            $ecartJours === 1 => "demain avant $heure",
            $ecartJours < 7 => self::JOURS[(int) $echeance->format('w')] . " avant $heure",
            default => 'le ' . $echeance->format('j') . ' ' . self::MOIS[(int) $echeance->format('n')] . " avant $heure",
        };
    }

    /** 9 h, 16 h 30 */
    public static function heure(\DateTimeImmutable $t): string
    {
        $m = (int) $t->format('i');
        return $t->format('G') . ' h' . ($m ? ' ' . str_pad((string) $m, 2, '0', STR_PAD_LEFT) : '');
    }

    /** « vendredi 31 octobre 2026 à 14 h 05 » */
    public static function dateLongue(\DateTimeImmutable $t): string
    {
        $t = $t->setTimezone(new \DateTimeZone('Europe/Zurich'));
        return self::JOURS[(int) $t->format('w')] . ' ' . $t->format('j') . ' '
            . self::MOIS[(int) $t->format('n')] . ' ' . $t->format('Y') . ' à ' . self::heure($t);
    }
}
