"""AUTLEN 2026/27 - Práctica 1.

Integrantes: Martín Darío Marmolejo Díaz, 
Completa los patrones y las sustituciones. Añade una explicación breve de cada uno.
Pruebas: python3 -m unittest -v test_p1
"""

# Ejemplo: cadenas no vacías sobre {a,b} que empiezan por a.
RE0 = r"a[ab]*"

# 1. Número impar de ceros.
RE1 = r"1*0(1*01*01*)*"

# 2. Sin dos unos consecutivos; se admite la cadena vacía.
RE2 = r"1?(0+1?)*"

# 3. Importes con signo opcional y parte decimal opcional de dos cifras.
RE3 = r"[-+]?([1-9][0-9]*|0)(,[0-9]{2})?"

# 4. Archivos nombre_apellido.txt o .csv, con datos/ opcional.
RE4 = r"(datos/)?[a-z]+_[a-z]+(\.txt|\.csv)"

# 5. hh:mm:ss; grupos: hora, minutos, segundos.
RE5 = r"([01][0-9]|2[0123]):([0-5][0-9]):([0-5][0-9])"

# 6. rgb(r,g,b); grupos: rojo, verde, azul.
RE6 = r"rgb\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\)"

# 7. Cada secuencia de espacios/tabuladores se sustituye por un espacio.
RE7 = r"[ ]*\t[ ]*|( [ ]+)"
SUB7 = r" "

# 8. Cadena completa apellido, nombre -> nombre apellido.
RE8 = r"\A([a-z]+), ([a-z]+)\Z"
SUB8 = r"\2 \1"
