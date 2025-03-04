# Rationale - Validación de los Resultados

Este documento explica cómo se han validado los resultados obtenidos en el análisis de artículos utilizando Grobid y herramientas de visualización.

---

## 1. Validación del Número de Figuras 
- Se comparó la cantidad de figuras extraídas del XML con las figuras visibles en los artículos PDF.  
- Se imprimieron los valores de `num_figuras` antes de graficarlos para verificar que la extracción fue correcta.  

---

## 2. Validación de los Enlaces Extraídos 
- Se listaron todos los enlaces detectados en los XML con `print()`.  
- Se revisó que cada enlace encontrado en `ptr[@target]` correspondiera a una referencia real en el documento.  

---

## 3. Validación de la Nube de Palabras Clave 
- Se imprimieron los primeros 300 caracteres del resumen (`abstract_text[:300]`) para comprobar que contenían información relevante.  
- Si la nube no se generaba, se verificó `len(full_text)` antes de usar `WordCloud`.  

---

## 4. Herramientas Utilizadas
- **Grobid** para la extracción de texto estructurado.  
- **Python (matplotlib, wordcloud)** para la visualización de datos.  
- **GitHub** para el control de versiones.  

---

## Conclusión
Los resultados fueron validados mediante impresiones intermedias y comparaciones con los documentos originales. El código fue corregido iterativamente para asegurar su precisión.
