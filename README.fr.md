# 🇨🇭 Conseiller Fiscal Suisse (`swiss-tax-advisor`)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [简体中文](README.zh.md)

---

> **Compétence Agent open-source pour la déclaration d'impôt suisse, le radar de risque fiscal et l'optimisation fiscale proactive.**  
> Compatible avec **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor** et **OpenClaw**.

---

## 🚀 Capacités Clés

1. **Zéro Dépendance Externe** : Conçu exclusivement avec la bibliothèque standard Python 3.10+ (`math`, `argparse`, `json`, `sys`, `unittest`). Aucun `pip install` requis.
2. **Précision Déterministe à 5 Rappen** : Élimine les hallucinations de calcul mental des LLM sur les barèmes progressifs suisses.
3. **Radar de Risque Cantonal (Score 0 à 100)** : Simule les contrôles automatiques de l'administration fiscale cantonale (*Risikobasierte Fallauswahl*).
4. **Taxonomie Complète S1 à S12** : Déductions pour frais professionnels, frais de garde, 3e pilier A, double gain et pensions alimentaires.
5. **Moteurs de Décision Stratégiques** :
   - **Évaluateur NOV Impôt à la Source** : Analyse du gain fiscal vs. risque de rattrapage pour les titulaires de permis B.
   - **Optimiseur de Franchise LAMal (300 vs 2500)** : Seuil de rentabilité actuariel.
   - **Simulateur de Déménagement** : Comparaison financière des coefficients d'impôt cantonaux et communaux.

---

## ⚡ Démarrage Rapide

Exécuter la suite de tests :
```bash
python3 skills/swiss-tax-advisor/scripts/test_tax_engine.py
```

### Exemples de Commandes CLI

```bash
# 1. Calculer les impôts (Vaud, Marié, 170k brut, 3e pilier et crèche)
python3 skills/swiss-tax-advisor/scripts/swiss_tax_math.py \
  --gross-income 170000 --canton VD --civil-status MARRIED --children 1 \
  --deductions '{"s1": 3300, "s4": 7258, "s6": 18000}' --json

# 2. Évaluer la demande de taxation ordinaire ultérieure (NOV)
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 110000 --canton GE --deductions '{"s4": 7258, "s1": 3300}'

# 3. Optimiser la franchise d'assurance maladie
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py franchise \
  --spend 1400 --premium-300 450 --premium-2500 310
```

---

## 📄 Licence

Distribué sous **Licence MIT**. Voir `LICENSE` pour les détails.
