# Modelo Actuarial para la Industria Audiovisual  
### Proyecto académico-experimental · Enfoque Bayesiano · Riesgo · Colas largas · Greenlight

---

## 1. Introducción

Este proyecto construye un **modelo actuarial para la industria audiovisual**, inspirado en metodologías reales del sector asegurador (SCR, riesgo de mercado, riesgo de cartera, riesgo extremo) y técnicas estadísticas avanzadas (GLM, análisis bayesiano, inferencia posterior).

El objetivo principal **no es predecir taquillas**, sino modelizar:

- **El riesgo del greenlight** (decidir si financiar / producir un proyecto).
- **Las colas largas** de la distribución del éxito cinematográfico.
- **La probabilidad de pérdida extrema**.
- **Cómo se comporta una cartera de proyectos** (major, plataforma o productora independiente).
- **El riesgo de quiebra y el capital necesario** para sostener una estrategia dada.

Este README actúa como **hoja de ruta estricta**, para evitar desviaciones del proyecto.

---

## 2. Filosofía del proyecto

Este trabajo opera bajo tres ideas centrales:

### 2.1. **Mirar colas, no medias**
La media del rendimiento cinematográfico no tiene ningún valor operativo.  
El modelo se centra en:
- Outliers
- Riesgos extremos
- Colas pesadas
- Pareto / Lognormal / mixtures

### 2.2. **Rigor actuarial aplicado a un sector creativo**
Las majors operan como aseguradoras:
- Invierten en muchas “pólizas” llamadas películas
- Cobran en forma de ingresos potenciales
- El riesgo está concentrado en la cola derecha (hits)
- El riesgo de quiebra está en la cola izquierda (flops críticos)
- Hacen *hedging* mediante géneros, ventanas, y franquicias

### 2.3. **Greenlight como pricing**
El greenlight es equivalente al pricing actuarial de un producto:
- presupuesto ↔ capital requerido  
- riesgo ↔ severidad potencial  
- probabilidad de éxito ↔ frecuencia  
- adquisición por plataformas ↔ prima  

El objetivo final es definir:  
👉 **¿Qué precio justo tendría pagar una major por una película con unas características dadas, según su riesgo?**

---

## 3. Fuentes de datos previstas

El proyecto distingue entre **fuentes primarias**, **secundarias** y **indicadores externos**.

### 3.1. **SCRAPING RAW (fase actual del proyecto)**

#### TMDB (API oficial)
- Budget
- Revenue
- Keywords
- Géneros
- Países y productoras
- Popularidad
- Votes, ratings
- Status (Released, Post-production…)
- Colecciones / franquicias
- Idioma

**Cobertura actual:**  
Se scrapearon 2015–2024 (≈10000 películas/año).

#### IMDb (scraping vía HTML)
A obtener próximamente:
- Rating IMDb
- n_votos
- Género
- País producción
- Año
- Director
- Cast (solo principal)
- Duración
- Certificación (PG-13, R…)
- Metascore si disponible

---

### 3.2. **Fuentes secundarias**
No se scrapearán ahora, pero se integrarán más adelante:

- Wikipedia data sobre box office histórico  
- Kaggle / datasets públicos cinematográficos  
- Websites de festivales (Sundance, Cannes, Sitges)  
- The Numbers (solo cuando tengamos dataset base)

---

### 3.3. **Factores externos para stress testing**
No entran ahora pero se documentan:

- Recesiones globales  
- Pandemias / cierres de salas  
- Huelgas (WGA, SAG-AFTRA)  
- Shifts tecnológicos (streaming → AI → AR)  
- Riesgo geopolítico  
- Riesgo de marketing / RRSS

---

## 4. Estructura del repo
/modelo_actuarial_audiovisual
│
├── src/
│   ├── tmdb_client.py
│   ├── tmdb_details.py
│   ├── enrich_tmdb_year.py
│   ├── enrich_tmdb_range.py
│
├── data_raw/
│   ├── tmdb/
│   ├── imdb/
│   ├── tnumbers/
│   └── bom/
│
├── data_clean/
│
├── notebooks/
│   ├── exploracion_tmdb.ipynb
│
├── README.md
└── .gitignore
---

## 5. Roadmap del proyecto (v1.0)

### **FASE 1 — Obtención de datos (RAW)**
✔ TMDB completo (10 años)  
⬜ IMDb scraping  
⬜ Consolidación RAW

### **FASE 2 — Limpieza y fusión de datasets**
⬜ Normalización de nombres  
⬜ Parseo de keywords  
⬜ Construcción de dataset unificado  
⬜ Eliminación de películas no relevantes (microproducciones sin datos)

### **FASE 3 — Análisis exploratorio**
⬜ Distribución del presupuesto  
⬜ Distribución del revenue  
⬜ Relación budget/revenue  
⬜ Identificación de colas y outliers  
⬜ Análisis por género

### **FASE 4 — Modelos estadísticos**
⬜ GLM (Poisson, Gamma, Lognormal)  
⬜ Enfoque Bayesiano  
⬜ Pósterior predictiva  
⬜ Intervalos HPD  
⬜ Scoring de greenlight

### **FASE 5 — Modelo actuarial**
⬜ “SCR cinematográfico”  
⬜ Riesgo de cartera (Majors)  
⬜ Simulaciones Monte Carlo  
⬜ Riesgo de quiebra  
⬜ Capital económico (VaR y TVaR)  
⬜ Stress scenarios

### **FASE 6 — Aplicación práctica**
⬜ Motor de pricing del greenlight  
⬜ Motor de adquisición para plataformas  
⬜ Informe final académico estilo working paper

---

## 6. Justificación del enfoque

### 6.1. ¿Por qué actuarial?
Porque el cine:
- Es incierto
- Tiene colas extremas
- Requiere capital upfront
- Se gestiona por cartera
- Tiene ciclos económicos
- Tiene parámetros no observables

### 6.2. ¿Por qué bayesiano?
Porque:
- Permite actualizar creencias proyecto a proyecto  
- Funciona incluso con información incompleta  
- Es ideal para riesgo extremo  
- Genera predicciones con incertidumbre realista  

---

## 7. Limitaciones iniciales

- El 90% de los datos RAW no contiene revenue (normal en la industria).
- Una parte del dataset corresponde a producciones micro que deberán filtrarse.
- Los datos de plataformas no son públicos.
- Keywords pueden estar incompletas.
- IMDb no proporciona ingresos reales.
- No existe acceso a marketing spend (variable oculta crítica).

Estas limitaciones forman parte **fundamental** del modelo bayesiano, no son errores.

---

## 8. Estado actual del proyecto

- ✓ Scraper TMDB completado 2015–2024  
- ✓ Almacén RAW estructurado  
- ⬜ Scraper IMDb pendiente  
- ⬜ Limpieza y fusión pendiente  
- ⬜ Desarrollo GLM pendiente  
- ⬜ Desarrollo bayesiano pendiente

---

## 9. Aviso metodológico

Este README funciona como **guardarraíl del proyecto**.  
Si en el futuro se quiere agregar, modificar o ampliar algo:

Toda decisión debe pasar tres filtros:
1. **¿Aumenta rigor o reduce ruido?**
2. **¿Es reproducible?**
3. **¿Es coherente con el enfoque actuarial-bayesiano?**

Sólo si las tres respuestas son “sí”, la modificación es válida.

---

## 10. Autoría

Proyecto desarrollado por **Javier Castillo** con apoyo de un sistema tutor especializado para estructurar, validar y asegurar la rigurosidad técnica del proceso.