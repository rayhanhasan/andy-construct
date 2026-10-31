<?php
declare(strict_types=1);

namespace AndyConstruct\Api;

/** Référence de demande lisible au téléphone : AC-2026-0042 (compteur annuel). */
final class Reference
{
    public static function suivante(Stockage $stockage, string $prefixe, ?int $annee = null): string
    {
        $annee ??= (int) date('Y');
        $fichier = $stockage->dossier('compteurs') . "/$annee.txt";
        $numero = $stockage->sousVerrou("compteur-$annee", static function () use ($fichier, $stockage): int {
            $n = is_file($fichier) ? (int) trim((string) file_get_contents($fichier)) : 0;
            $n++;
            $stockage->ecrireAtomique($fichier, (string) $n);
            return $n;
        });
        $prefixe = preg_replace('/[^A-Z0-9]/', '', strtoupper($prefixe)) ?: 'AC';
        return sprintf('%s-%d-%04d', $prefixe, $annee, (int) $numero);
    }
}
