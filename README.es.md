# 🇨🇭 Asesor Fiscal Suizo (`swiss-tax-advisor`)

[English](README.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Italiano](README.it.md) | [Español](README.es.md) | [简体中文](README.zh.md)

---

> **Habilidad de Agente de código abierto para la declaración de impuestos en Suiza, radar de riesgo de auditoría y optimización fiscal proactiva.**  
> Compatible con **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **Google Antigravity**, **Cursor** y **OpenClaw**.

---

## 🚀 Capacidades Principales

1. **Cero Dependencias Externas**: Basado únicamente en la biblioteca estándar de Python 3.10+ (`math`, `argparse`, `json`, `sys`, `unittest`). No requiere `pip install`.
2. **Precisión Determinista a 5 Rappen**: Puerta estricta que impide que los LLM realicen cálculos mentales aproximados en las tarifas progresivas suizas.
3. **Radar de Riesgo de Auditoría Cantonal (0 a 100)**: Simula los algoritmos automáticos de las administraciones fiscales cantonales (*Risikobasierte Fallauswahl*) para corregir banderas rojas antes de la presentación.
4. **Arquitectura Hexa-Lingüe**: Adaptación dinámica de respuestas al español, inglés, alemán, francés, italiano o chino.
5. **Taxonomía Completa de Deducciones (S1 a S12)**: Límites legales vigentes (DBG, StHG, StG BE), deducciones por hijos (Kita), tercer pilar (Pillar 3a), pensión alimenticia y doble ingreso conyugal.
6. **Motores de Decisión Avanzados**:
   - **Evaluador de Retención en Origen (NOV)**: Decisión informada sobre si solicitar la declaración ordinaria o mantener la retención.
   - **Optimizador de Franquicia del Seguro Médico (300 vs. 2500)**: Cálculo actuarial del punto de equilibrio.
   - **Simulador de Reubicación Cantonal**: Comparativa del multiplicador fiscal (*Steuerfuss*) entre cantones.

---

## ⚡ Inicio Rápido y Pruebas

Ejecutar la suite de pruebas local:
```bash
python3 skills/swiss-tax-advisor/scripts/test_tax_engine.py
```

### Ejemplos de Comandos CLI

```bash
# 1. Calcular impuestos (Berna, Casado, Ingreso bruto 170k, con 3a y guardería)
python3 skills/swiss-tax-advisor/scripts/swiss_tax_math.py \
  --gross-income 170000 --canton BE --civil-status MARRIED --children 1 \
  --deductions '{"s1": 3300, "s4": 7258, "s6": 18000}' --json

# 2. Consultar tasa impositiva marginal y ahorro con Pilar 3a
python3 skills/swiss-tax-advisor/scripts/marginal_rate_calc.py \
  --income 120000 --canton ZH --deduction 7258 --category PILLAR_3A --json

# 3. Evaluar solicitud de tributación ordinaria posterior (NOV)
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py nov \
  --income 110000 --canton ZH --deductions '{"s4": 7258, "s1": 3300}'

# 4. Optimizar franquicia de seguro médico
python3 skills/swiss-tax-advisor/scripts/advanced_advisory.py franchise \
  --spend 1400 --premium-300 450 --premium-2500 310
```

---

## 📄 Licencia

Distribuido bajo la **Licencia MIT**. Consulte `LICENSE` para más detalles.
