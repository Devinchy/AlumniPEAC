import os
import re

# Diccionario con el orden de las charlas
charlas_orden = [
    ("charla_gestion_emocional.md", "Altas Capacidades en la Edad Adulta: Emociones y Bienestar", "gestion-emocional"),
    ("charla-comorbilidad.md", "Comorbilidad y Neurodiversidad en Adultos Superdotados", "comorbilidad"),
    ("charla-creatividad-sentido.md", "Creatividad, Búsqueda de Sentido y Realización Personal", "creatividad"),
    ("charla-doble-excepcionalidad.md", "Doble Excepcionalidad (2E) en Adultos", "doble-excepcionalidad"),
    ("charla-educacion-permanente.md", "Educación Permanente y Aprendizaje a lo Largo de la Vida", "educacion-permanente"),
    ("charla-estigma-mitos.md", "Estigma, Mitos y Comunicación Pública sobre Superdotación", "estigma"),
    ("charla-identificacion-adultez.md", "Identificación en la Adultez", "identificacion"),
    ("charla-impostorismo.md", "Impostorismo y Subrendimiento", "impostorismo"),
    ("charla-interseccionalidad.md", "Aspectos Interculturales e Interseccionales", "interseccionalidad"),
    ("charla-investigacion.md", "Investigación y Metodologías para Estudiar Adultos Superdotados", "investigacion"),
    ("charla-parentalidad.md", "Parentalidad: Ser Padre/Madre Superdotado", "parentalidad"),
    ("charla-politicas.md", "Políticas Públicas, Detección y Recursos en España", "politicas"),
    ("charla-relaciones.md", "Relaciones Íntimas y Sociales en la Adultez Superdotada", "relaciones"),
    ("charla-sobreexcitabilidad.md", "Sobreexcitabilidad Emocional y Dabrowski", "sobreexcitabilidad"),
    ("charla-vida-laboral.md", "Vida Laboral: Encaje, Elección de Carrera y Emprendimiento", "vida-laboral")
]

def escapar_latex(texto):
    """Escapa caracteres especiales de LaTeX"""
    reemplazos = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '"': "''",
        '"': "``",
        '"': "''",
        '«': r'``',
        '»': r"''"
    }
    
    for char, reemplazo in reemplazos.items():
        texto = texto.replace(char, reemplazo)
    
    return texto

def convertir_markdown_a_latex(contenido):
    """Convierte Markdown simple a LaTeX"""
    
    # Eliminar líneas de formato markdown como ### o ---
    contenido = re.sub(r'^#{1,6}\s+(.+)$', r'\1', contenido, flags=re.MULTILINE)
    contenido = re.sub(r'^---+$', '', contenido, flags=re.MULTILINE)
    
    # Convertir listas con viñetas
    contenido = re.sub(r'^-\s+(.+)$', r'\\item \1', contenido, flags=re.MULTILINE)
    contenido = re.sub(r'^\*\s+(.+)$', r'\\item \1', contenido, flags=re.MULTILINE)
    
    # Convertir negritas y cursivas
    contenido = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', contenido)
    contenido = re.sub(r'\*(.+?)\*', r'\\textit{\1}', contenido)
    
    # Eliminar líneas vacías múltiples
    contenido = re.sub(r'\n{3,}', '\n\n', contenido)
    
    return contenido

def procesar_charla(archivo, directorio="."):
    """Lee y procesa un archivo de charla"""
    ruta = os.path.join(directorio, archivo)
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return contenido
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return ""

def generar_latex_completo(directorio="."):
    """Genera el documento LaTeX completo con todas las charlas"""
    
    # Preámbulo
    latex = r"""\documentclass[12pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{titlesec}

% Configuración de márgenes
\geometry{
    left=3cm,
    right=2.5cm,
    top=2.5cm,
    bottom=2.5cm
}

% Configuración de hipervínculos
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={Charlas sobre Altas Capacidades en Adultos},
    pdfauthor={AlumniPEAC},
    pdfsubject={Superdotación Adulta}
}

% Configuración de encabezados y pies de página
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}

% Formato de capítulos
\titleformat{\chapter}[display]
{\normalfont\huge\bfseries\color{blue!70!black}}
{\chaptertitlename\ \thechapter}{20pt}{\Huge}

\titleformat{\section}
{\normalfont\Large\bfseries\color{blue!60!black}}
{\thesection}{1em}{}

\title{
    \vspace{2cm}
    {\Huge\bfseries Charlas sobre Altas Capacidades}\\
    \vspace{0.5cm}
    {\Large en la Edad Adulta}\\
    \vspace{2cm}
}
\author{AlumniPEAC}
\date{\today}

\begin{document}

\maketitle
\thispagestyle{empty}
\newpage

\tableofcontents
\newpage

"""
    
    # Procesar cada charla
    for archivo, titulo, label in charlas_orden:
        print(f"Procesando: {archivo}")
        contenido = procesar_charla(archivo, directorio)
        
        if contenido:
            # Escapar y convertir
            contenido_escapado = escapar_latex(contenido)
            contenido_latex = convertir_markdown_a_latex(contenido_escapado)
            
            # Agregar capítulo
            latex += f"\n\\chapter{{{titulo}}}\n"
            latex += f"\\label{{chap:{label}}}\n\n"
            latex += contenido_latex
            latex += "\n\\newpage\n\n"
    
    # Final del documento
    latex += r"\end{document}"
    
    return latex

# Directorio donde están los archivos
directorio_charlas = r"c:\Users\devin\OneDrive\AlumniPEAC"

# Generar el LaTeX
print("Generando documento LaTeX completo...")
documento_latex = generar_latex_completo(directorio_charlas)

# Guardar el archivo
archivo_salida = os.path.join(directorio_charlas, "charlas_completas_autogenerado.tex")
with open(archivo_salida, 'w', encoding='utf-8') as f:
    f.write(documento_latex)

print(f"Documento generado: {archivo_salida}")
print("Para compilar el documento, ejecuta: pdflatex charlas_completas_autogenerado.tex")
