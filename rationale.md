# Rationale - Validación de los Resultados

Este documento explica cómo se han validado los resultados obtenidos en el análisis de artículos utilizando Grobid y herramientas de visualización.

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 1. Validación del Número de Figuras 
- Primero comparé la cantidad de figuras extraídas del XML con las figuras visibles en los artículos PDF.  
- Al ser las mismas imprimi los valores de `num_figuras` antes de graficarlos para verificar que la extracción fue correcta.  

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 2. Validación de los Enlaces Extraídos 
- Aquí solamente liste todos los enlaces detectados en los XML con `print()`.  
- Y revisé que cada enlace encontrado en `ptr[@target]` correspondiera a una referencia real en el documento.  

-----------------------------------------------------------------------------------------------------------------------------------------------------

## 3. Validación de la Nube de Palabras Clave 
- Para validar este paso primero almacene todos los resumenes en una variable y comprobe que existiera dichos resumenes (que no estuvieran vacios)
 posteriormente con las palabras mas frecuentadas cree la nube de palabras poniendo las mas relevante mas grande y las menos relevantes mas pequeñas.  

-----------------------------------------------------------------------------------------------------------------------------------------------------


