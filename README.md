# Análisis Multivariante

Materiales del curso de **Análisis Multivariante** (Licenciatura en Economía, Tecnológico de Monterrey). Contiene los datos, los cuadernos de Python y el código que acompañan a las *Notas de Clase: Análisis Multivariante*.

📄 **Notas del curso:** [`Notas_Analisis_Multivariante.pdf`](Notas_Analisis_Multivariante.pdf)

El curso trata las técnicas de **interdependencia**: componentes principales, análisis factorial, construcción de índices compuestos y análisis de conglomerados. Cada técnica se estudia con sus fundamentos matemáticos y se aplica a datos reales de México, sobre todo la ENIGH 2024 del INEGI.

## Temario

**Módulo 1. Introducción a la estadística multivariante de interdependencia (2 horas)**
1.1 Estadística multivariada de interdependencia contra de dependencia
1.2 Escalas de medición
1.3 Filosofía de trabajo de una técnica multivariada
1.4 Etapas en el desarrollo de una técnica multivariada

**Módulo 2. Análisis de factores (10 horas)**
2.1 Definición del problema, objetivos y plan de desarrollo (incluye componentes principales)
2.2 Supuestos y estimación del modelo
2.3 Interpretación y validación del modelo
2.4 Desarrollo de un análisis de factores con software (incluye índices compuestos)

**Módulo 3. Análisis de conglomerados (8 horas)**
3.1 Definición del problema, objetivos y plan de desarrollo
3.2 Supuestos y estimación del modelo
3.3 Interpretación y validación del modelo
3.4 Desarrollo de un análisis de conglomerados con software (incluye series de tiempo)

## Organización del repositorio

Cada carpeta corresponde a un capítulo de las notas. El cuaderno marcado con ★ reproduce, paso a paso, los ejemplos numéricos del capítulo; los demás son aplicaciones adicionales.

| Carpeta | Capítulo de las notas | Cuadernos |
|---|---|---|
| `01 Intro/` | 1. Fundamentos del análisis multivariante | ★ `03 Fundamentos/Fundamentos_Multivariante.ipynb` · `02 Aplicación de modelos clustering/` (k-medias con datos de COVID-19, se retoma en el cap. 5) |
| `02 PCA/` | 2. Análisis de componentes principales | ★ `PCA_Paises.ipynb` · `Principal_Component_Analysis.ipynb` |
| `03 Factor Analysis/` | 3. Análisis factorial | ★ `04 Entidades ENIGH/Factorial_Entidades_ENIGH.ipynb` · `01 Intro ENIGH/` · `02 Divorce/` · `03 ENIGH/` |
| `04 Indices/` | 4. Construcción de índices compuestos | ★ `01 Indice ENIGH/Indice_Compuesto_ENIGH.ipynb` |
| `05 Clustering/` | 5. Análisis de conglomerados | ★ `05 Tipologia Entidades/Tipologia_Entidades.ipynb` · `01 Intro Distancias/` · `02 Cluster Iris Data/` · `03 Clustering Customer/` · `04 Clustering Countries/` |
| `06 Clustering Time Series/` | 5. Análisis de conglomerados (series de tiempo) | `01 Prototipo/` (descarga de precios de la BMV) · `02 Clustering/` · `03_Unsupervised_Clusteing_Time_Series/` (precios marginales locales del Sistema Eléctrico Nacional) |
| `07 Evaluaciones/` | — | `Practica_Python_plantilla.ipynb` (práctica de la semana 2; colóquela en esta carpeta para que la ruta a los datos funcione) · `Trabajo_Final.pdf` (enunciado y rúbrica del trabajo final) |
| `utils/` | — | `factorial.py`: análisis factorial en `numpy`/`scipy` (adecuación, estimación, rotación, puntuaciones) |

### El hilo conductor: la ENIGH 2024

Los cuadernos ★ de los capítulos 3, 4 y 5 forman una secuencia y deben ejecutarse en ese orden:

1. `03 Factor Analysis/04 Entidades ENIGH/` construye seis indicadores por entidad federativa a partir del microdato y estima dos factores: nivel socioeconómico y envejecimiento. Escribe `enigh2024_entidades.csv` y `enigh2024_puntuaciones.csv`.
2. `04 Indices/01 Indice ENIGH/` convierte el primer factor en un índice compuesto, evalúa su robustez y lo valida.
3. `05 Clustering/05 Tipologia Entidades/` construye una tipología de las entidades con las puntuaciones factoriales.

## Instalación

```bash
pip install -r requirements.txt
jupyter notebook
```

Los cuadernos leen sus datos con rutas relativas, así que deben abrirse desde su propia carpeta. Los cuadernos ★ que usan `utils/factorial.py` lo importan con `sys.path.insert(0, "../../utils")`.

## Datos

| Archivo | Fuente |
|---|---|
| `03 Factor Analysis/*/enigh2024_ns_concentradohogar_csv.zip` | INEGI, Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2024, nueva serie, tabla `concentradohogar` |
| `05 Clustering/04 Clustering Countries/Country-data.csv` | HELP International, *Unsupervised Learning on Country Data* (Kaggle) |
| `03 Factor Analysis/02 Divorce/divorce.csv` | Yöntem et al. (2019), *Divorce Predictors* |
| `05 Clustering/02 Cluster Iris Data/IRIS.csv` | Fisher (1936), conjunto de datos Iris |
| `05 Clustering/03 Clustering Customer/marketing_campaign.csv` | *Customer Personality Analysis* (Kaggle) |
| `01 Intro/02 Aplicación de modelos clustering/` | Secretaría de Salud, datos abiertos de COVID-19 |
| `06 Clustering Time Series/03_.../Datos_PML*.csv` | CENACE, precios marginales locales |
| `06 Clustering Time Series/*/precios_5y.xlsx` | Yahoo Finance, emisoras de la BMV |

## Licencia

Las notas, los cuadernos y el código de este repositorio se dedican al dominio público bajo [CC0 1.0 Universal](LICENSE): pueden copiarse, modificarse y distribuirse, incluso con fines comerciales, sin pedir permiso. Citar la fuente es una buena práctica académica, aunque no es obligatorio.

**Excepción: los datos de terceros.** Los conjuntos de datos de la sección *Datos* (INEGI, Secretaría de Salud, CENACE, Kaggle, Yahoo Finance y otros) no son obra de este repositorio y conservan los términos de uso de su fuente original.
