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
    """Escapa caracteres especiales de LaTeX de forma más precisa"""
    # Primero proteger los que ya están escapados
    texto = texto.replace('\\', '\\textbackslash{}')
    
    # Caracteres especiales que deben escaparse
    reemplazos = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    
    for char, reemplazo in reemplazos.items():
        texto = texto.replace(char, reemplazo)
    
    # Caracteres Unicode especiales
    unicode_reemplazos = {
        '□': r'$\square$',  # Checkbox vacío
        '☑': r'$\boxtimes$',  # Checkbox marcado
        '≠': r'$\neq$',  # No igual
        '≤': r'$\leq$',  # Menor o igual
        '≥': r'$\geq$',  # Mayor o igual
        '→': r'$\rightarrow$',  # Flecha derecha
        '←': r'$\leftarrow$',  # Flecha izquierda
        '⇒': r'$\Rightarrow$',  # Flecha doble derecha
    }
    
    for char, reemplazo in unicode_reemplazos.items():
        texto = texto.replace(char, reemplazo)
    
    # Corregir comillas
    texto = texto.replace('"', "``")
    texto = texto.replace('"', "''")
    texto = texto.replace('«', '``')
    texto = texto.replace('»', "''")
    texto = texto.replace('"', "''")
    
    # Restaurar backslash de comandos LaTeX
    texto = texto.replace('\\textbackslash{}', '\\textbackslash ')
    
    return texto

def procesar_linea_markdown(linea):
    """Procesa una línea individual detectando su tipo"""
    linea = linea.rstrip()
    
    # Detectar títulos markdown
    if linea.startswith('# '):
        return ('titulo1', linea[2:].strip())
    elif linea.startswith('## '):
        return ('titulo2', linea[3:].strip())
    elif linea.startswith('### '):
        return ('titulo3', linea[4:].strip())
    elif linea.startswith('#### '):
        return ('titulo4', linea[5:].strip())
    elif linea.startswith('---'):
        return ('separador', '')
    elif linea.startswith('- ') or linea.startswith('* '):
        return ('item', linea[2:].strip())
    elif re.match(r'^\d+\.\s', linea):
        return ('item_num', re.sub(r'^\d+\.\s', '', linea).strip())
    elif linea.strip() == '':
        return ('vacio', '')
    elif linea.startswith('|'):
        return ('tabla', linea)
    else:
        return ('texto', linea)

def convertir_enfasis(texto):
    """Convierte énfasis de markdown a LaTeX"""
    # Negritas **texto** o __texto__
    texto = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', texto)
    texto = re.sub(r'__(.+?)__', r'\\textbf{\1}', texto)
    
    # Cursivas *texto* (pero no sobre guiones bajos que ya están escapados)
    texto = re.sub(r'\*(.+?)\*', r'\\textit{\1}', texto)
    # NO convertir guiones bajos escapados a cursiva
    # texto = re.sub(r'(?<!\w)_([^_]+?)_(?!\w)', r'\\textit{\1}', texto)
    
    return texto

def procesar_charla(archivo, directorio="."):
    """Lee y procesa un archivo de charla con mejor estructura"""
    ruta = os.path.join(directorio, archivo)
    
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return contenido
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta}")
        return ""

def convertir_markdown_a_latex_mejorado(contenido):
    """Convierte Markdown a LaTeX con mejor manejo de estructura"""
    lineas = contenido.split('\n')
    salida = []
    en_lista = False
    en_lista_num = False
    en_tabla = False
    primer_titulo = True
    
    i = 0
    while i < len(lineas):
        tipo, valor = procesar_linea_markdown(lineas[i])
        
        # Cerrar listas si es necesario
        if tipo not in ['item', 'item_num']:
            if en_lista:
                salida.append('\\end{itemize}')
                en_lista = False
            if en_lista_num:
                salida.append('\\end{enumerate}')
                en_lista_num = False
        
        if tipo == 'titulo1':
            # El primer título (# ...) se ignora porque ya está en el chapter
            if not primer_titulo:
                salida.append(f'\n\\section{{{escapar_latex(valor)}}}')
            primer_titulo = False
            
        elif tipo == 'titulo2':
            # ## se convierte en section o subsection según contexto
            if primer_titulo:  # Si es el primer subtítulo después del título
                salida.append(f'\n\\section*{{{escapar_latex(valor)}}}')
                salida.append('\\addcontentsline{toc}{section}{' + escapar_latex(valor) + '}')
            else:
                salida.append(f'\n\\section{{{escapar_latex(valor)}}}')
            primer_titulo = False
            
        elif tipo == 'titulo3':
            salida.append(f'\n\\subsection{{{escapar_latex(valor)}}}')
            
        elif tipo == 'titulo4':
            salida.append(f'\n\\subsubsection{{{escapar_latex(valor)}}}')
            
        elif tipo == 'item':
            if not en_lista:
                salida.append('\\begin{itemize}[leftmargin=*]')
                en_lista = True
            # Escapar LaTeX primero, luego aplicar énfasis
            valor_escapado = escapar_latex(valor)
            valor_procesado = convertir_enfasis(valor_escapado)
            salida.append(f'    \\item {valor_procesado}')
            
        elif tipo == 'item_num':
            if not en_lista_num:
                salida.append('\\begin{enumerate}[leftmargin=*]')
                en_lista_num = True
            valor_escapado = escapar_latex(valor)
            valor_procesado = convertir_enfasis(valor_escapado)
            salida.append(f'    \\item {valor_procesado}')
            
        elif tipo == 'separador':
            # Ignorar líneas ---
            pass
            
        elif tipo == 'tabla':
            # Procesar tablas markdown (simplificado)
            if not en_tabla:
                # Detectar inicio de tabla
                salida.append('\\begin{center}')
                salida.append('\\small')
                en_tabla = True
            # Aquí podrías implementar procesamiento completo de tablas
            # Por ahora las ignoramos o las dejamos como están
            
        elif tipo == 'texto':
            if valor.strip():
                # Escapar primero, luego aplicar énfasis
                valor_escapado = escapar_latex(valor)
                valor_procesado = convertir_enfasis(valor_escapado)
                salida.append(valor_procesado)
            
        elif tipo == 'vacio':
            # Línea vacía = nuevo párrafo en LaTeX
            salida.append('')
        
        i += 1
    
    # Cerrar listas abiertas al final
    if en_lista:
        salida.append('\\end{itemize}')
    if en_lista_num:
        salida.append('\\end{enumerate}')
    if en_tabla:
        salida.append('\\end{center}')
    
    return '\n'.join(salida)

def generar_latex_completo_mejorado(directorio="."):
    """Genera el documento LaTeX completo con mejor estructura"""
    
    # Preámbulo mejorado
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
\usepackage{parskip}

% Configuración de márgenes
\geometry{
    left=3cm,
    right=2.5cm,
    top=2.5cm,
    bottom=2.5cm,
    headheight=30pt
}

% Configuración de hipervínculos
\hypersetup{
    colorlinks=true,
    linkcolor=blue!50!black,
    filecolor=magenta,
    urlcolor=cyan!50!black,
    pdftitle={Charlas sobre Altas Capacidades en Adultos},
    pdfauthor={AlumniPEAC},
    pdfsubject={Superdotación Adulta}
}

% Configuración de encabezados y pies de página
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\leftmark}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

% Formato de capítulos
\titleformat{\chapter}[display]
{\normalfont\huge\bfseries\color{blue!70!black}}
{\chaptertitlename\ \thechapter}{20pt}{\Huge}

\titleformat{\section}
{\normalfont\Large\bfseries\color{blue!60!black}}
{\thesection}{1em}{}

\titleformat{\subsection}
{\normalfont\large\bfseries\color{blue!50!black}}
{\thesubsection}{1em}{}

% Espaciado entre párrafos
\setlength{\parskip}{0.5em}
\setlength{\parindent}{0pt}

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
    for i, (archivo, titulo, label) in enumerate(charlas_orden, 1):
        print(f"Procesando {i}/{len(charlas_orden)}: {archivo}")
        contenido = procesar_charla(archivo, directorio)
        
        if contenido:
            # Agregar capítulo
            latex += f"\n\\chapter{{{escapar_latex(titulo)}}}\n"
            latex += f"\\label{{chap:{label}}}\n\n"
            
            # Convertir contenido con el nuevo método mejorado
            contenido_latex = convertir_markdown_a_latex_mejorado(contenido)
            latex += contenido_latex
            latex += "\n\n\\newpage\n\n"
    
    # Final del documento
    latex += r"\end{document}"
    
    return latex

# Directorio donde están los archivos
directorio_charlas = r"c:\Users\devin\OneDrive\AlumniPEAC"

# Generar el LaTeX
print("=" * 60)
print("Generando documento LaTeX MEJORADO con estructura correcta...")
print("=" * 60)
documento_latex = generar_latex_completo_mejorado(directorio_charlas)

# Guardar el archivo
archivo_salida = os.path.join(directorio_charlas, "charlas_completas_mejorado.tex")
with open(archivo_salida, 'w', encoding='utf-8') as f:
    f.write(documento_latex)

print(f"\n✓ Documento generado: {archivo_salida}")
print(f"✓ Tamaño: {len(documento_latex):,} caracteres")
print("\nPara compilar el documento:")
print("  pdflatex charlas_completas_mejorado.tex")
print("  pdflatex charlas_completas_mejorado.tex  (segunda pasada)")
print("  pdflatex charlas_completas_mejorado.tex  (tercera pasada)")
