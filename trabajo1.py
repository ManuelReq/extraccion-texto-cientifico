import os
import xml.etree.ElementTree as ET
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Especifico la ruta en donde se encuentran los archivos XML generados por Grobid.
# Es importante que cambies esta ruta si no es la correcta en tu caso.
xml_folder = r"C:\Users\Manuel\output_files"  

# Aquí voy a guardar los datos que voy a extraer de los archivos XML:
# - Los títulos de los artículos
# - El número de figuras que tiene cada artículo
# - Los enlaces encontrados en cada artículo
# - Los resúmenes de los artículos
articulos = []
num_figuras = []
enlaces_globales = []
resumenes = []

# Empiezo a recorrer cada archivo XML que está en la carpeta indicada.
# Esto me permite procesar todos los archivos XML de manera automática.
for filename in os.listdir(xml_folder):
    if filename.endswith(".xml"):  # Solo me interesan los archivos con extensión .xml
        xml_path = os.path.join(xml_folder, filename)  # Obtengo la ruta completa del archivo

        # Abro el archivo XML, especificando que se ignore cualquier error de codificación.
        # Esto puede suceder si el archivo tiene caracteres extraños o no esperados.
        with open(xml_path, "r", encoding="utf-8", errors="ignore") as f:
            xml_content = f.read()

        # Elimino cualquier carácter no válido en el archivo XML. Esto ayuda a evitar errores
        # si hay caracteres que no son parte del conjunto ASCII estándar.
        xml_content = re.sub(r'[^\x09\x0A\x0D\x20-\x7F]', '', xml_content)

        # Ahora convierto el contenido del archivo en un objeto XML que puedo procesar.
        # Utilizo el espacio de nombres (namespace) adecuado para poder buscar los elementos correctamente.
        root = ET.fromstring(xml_content)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        # Extraigo el título principal del artículo.
        # Si no hay un título, le asigno un nombre genérico como "Artículo 1", "Artículo 2", etc.
        title = root.find(".//tei:title[@level='a'][@type='main']", ns)
        title_text = title.text if title is not None else f"Artículo {len(articulos) + 1}"

        # Verifico si el título ya está en la lista de artículos. Si no está, lo añado.
        # Esto previene que se repitan artículos con el mismo título.
        if title_text not in articulos:
            articulos.append(title_text)

            # Extraigo las figuras del artículo. Si el artículo tiene figuras, las cuento.
            figures = root.findall(".//tei:figure", ns)
            num_figuras.append(len(figures))

            # Extraigo los enlaces dentro del artículo. Si no hay enlaces, guardo un valor "Sin enlaces".
            links = root.findall(".//tei:ptr[@target]", ns)
            article_links = [l.attrib["target"] for l in links] if links else ["Sin enlaces"]
            enlaces_globales.append({"Título": title_text, "Enlaces": article_links})

            # Extraigo el resumen del artículo.
            # Si no hay resumen, dejo el campo vacío.
            abstract = root.find(".//tei:abstract", ns)
            abstract_text = " ".join(p.text for p in abstract.findall(".//tei:p", ns) if p.text) if abstract is not None else ""
            resumenes.append(abstract_text)

# Ahora hago una verificación final de los datos que extraje.
# Imprimo la cantidad de artículos y la cantidad de entradas de figuras.
print("\nVerificación final de datos:")
print(f"Cantidad de artículos: {len(articulos)}")
print(f"Cantidad de entradas en num_figuras: {len(num_figuras)}")

# Si el número de artículos es igual al número de figuras y es mayor a 0, genero el gráfico.
# Este gráfico mostrará cuántas figuras tiene cada artículo.
if len(articulos) == len(num_figuras) and len(articulos) > 0:
    plt.figure(figsize=(10,5))
    plt.bar(articulos, num_figuras, color='skyblue')
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Artículo")
    plt.ylabel("Número de Figuras")
    plt.title("Número de Figuras por Artículo")
    plt.show()
else:
    print("Error: Las listas no tienen la misma cantidad de elementos. Revisa los datos antes de graficar.")

# Imprimo los enlaces que encontré en cada artículo.
# Esto me permitirá ver todos los enlaces asociados a cada artículo.
print("\nLista de enlaces por artículo:")
for item in enlaces_globales:
    print(f"\n{item['Título']}")
    for enlace in item['Enlaces']:
        print(f"   - {enlace}")

# Ahora, si los resúmenes no están vacíos, genero una nube de palabras clave.
# Esto me dará una representación visual de las palabras más frecuentes en los resúmenes.
full_text = " ".join(resumenes)
if full_text.strip():  # Primero verifico que haya texto para generar la nube
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(full_text)

    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de Palabras Clave del Resumen")
    plt.show()
else:
    print("No hay suficiente texto para generar una nube de palabras.")

