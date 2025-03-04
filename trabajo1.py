import os
import xml.etree.ElementTree as ET
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 📌 Ruta donde están los archivos XML generados por Grobid
xml_folder = r"C:\Users\Manuel\output_files"  # Asegúrate de cambiar esto a la carpeta correcta

# 📌 Listas para almacenar datos de todos los artículos
articulos = []
num_figuras = []
enlaces_globales = []
resumenes = []

# 📌 Procesar cada archivo XML en la carpeta
for filename in os.listdir(xml_folder):
    if filename.endswith(".xml"):
        xml_path = os.path.join(xml_folder, filename)

        # 📂 Cargar el XML con manejo de errores
        with open(xml_path, "r", encoding="utf-8", errors="ignore") as f:
            xml_content = f.read()

        # 🧹 Limpiar caracteres no válidos
        xml_content = re.sub(r'[^\x09\x0A\x0D\x20-\x7F]', '', xml_content)

        # 📖 Procesar XML
        root = ET.fromstring(xml_content)
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        # 📌 Extraer título (evitar duplicados)
        title = root.find(".//tei:title[@level='a'][@type='main']", ns)
        title_text = title.text if title is not None else f"Artículo {len(articulos) + 1}"

        # **EVITAR DUPLICADOS**
        if title_text not in articulos:
            articulos.append(title_text)

            # 📌 Extraer número de figuras
            figures = root.findall(".//tei:figure", ns)
            num_figuras.append(len(figures))

            # 📌 Extraer enlaces
            links = root.findall(".//tei:ptr[@target]", ns)
            article_links = [l.attrib["target"] for l in links] if links else ["Sin enlaces"]
            enlaces_globales.append({"Título": title_text, "Enlaces": article_links})

            # 📌 Extraer resumen
            abstract = root.find(".//tei:abstract", ns)
            abstract_text = " ".join(p.text for p in abstract.findall(".//tei:p", ns) if p.text) if abstract is not None else ""
            resumenes.append(abstract_text)

# 📌 Verificación final de datos
print("\n✅ Verificación final de datos:")
print(f"Cantidad de artículos: {len(articulos)}")
print(f"Cantidad de entradas en num_figuras: {len(num_figuras)}")

# 📊 **Gráfico de cantidad de figuras por artículo**
if len(articulos) == len(num_figuras) and len(articulos) > 0:
    plt.figure(figsize=(10,5))
    plt.bar(articulos, num_figuras, color='skyblue')
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Artículo")
    plt.ylabel("Número de Figuras")
    plt.title("Número de Figuras por Artículo")
    plt.show()
else:
    print("⚠️ Error: Las listas no tienen la misma cantidad de elementos. Revisa los datos antes de graficar.")

# 🔗 **Lista de enlaces encontrados en cada artículo**
print("\n🔗 Lista de enlaces por artículo:")
for item in enlaces_globales:
    print(f"\n📖 {item['Título']}")
    for enlace in item['Enlaces']:
        print(f"   - {enlace}")

# ☁️ **Nube de palabras clave basada en los resúmenes**
full_text = " ".join(resumenes)
if full_text.strip():  # Verificar que hay texto
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(full_text)

    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de Palabras Clave del Resumen")
    plt.show()
else:
    print("⚠️ No hay suficiente texto para generar una nube de palabras.")
