# import spacy
# from collections import defaultdict, Counter
# import io
# import base64
# import matplotlib.pyplot as plt
# import pandas as pd
# from django.shortcuts import render, get_object_or_404
# from encuestas.models import Encuesta, Respuesta

# # Cargar el modelo de spaCy para el idioma correspondiente
# nlp = spacy.load("es_core_news_sm")

# def generar_grafico_circular(clusters):
#     if clusters:
#         # Contar las ocurrencias de cada clúster
#         conteo_clusters = Counter(clusters.keys())

#         # Preparar datos para el gráfico
#         categorias = list(conteo_clusters.keys())
#         valores = list(conteo_clusters.values())

#         # Colores para los clústeres
#         colores = plt.cm.tab10.colors[:len(categorias)]

#         # Crear el gráfico circular
#         fig, ax = plt.subplots(figsize=(10, 6))
#         wedges, _ = ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90, colors=colores)
#         ax.axis('equal')  # radio igual para que sea un círculo

#         # Convertir el gráfico a imagen base64
#         buffer_imagen = io.BytesIO()
#         plt.savefig(buffer_imagen, format='png')
#         buffer_imagen.seek(0)
#         imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
#         imagen_base64 = f'data:image/png;base64,{imagen_base64}'

#         plt.close(fig)
#         return imagen_base64
#     else:
#         return None

# def generar_grafico_barras(datos, etiquetas=None):
#     if datos:
#         df_respuestas = pd.DataFrame(list(datos.items()), columns=['Respuesta', 'Cantidad'])
#         df_respuestas = df_respuestas.sort_values(by='Cantidad', ascending=False)
#         fig, ax = plt.subplots(figsize=(10, 6))
#         bars = ax.bar(df_respuestas['Respuesta'], df_respuestas['Cantidad'])
#         ax.set_xlabel('Respuesta')
#         ax.set_ylabel('Cantidad')
#         plt.xticks(rotation=45, ha="right")

#         # Agregar etiquetas en las barras si se proporcionan
#         if etiquetas:
#             for bar, etiqueta in zip(bars, [etiquetas.get(resp, '') for resp in df_respuestas['Respuesta']]):
#                 yval = bar.get_height()
#                 ax.text(bar.get_x() + bar.get_width()/2, yval, f'#{etiqueta}', va='bottom', ha='center')

#         fig.patch.set_alpha(0)
#         plt.tight_layout()
#         buffer_imagen = io.BytesIO()
#         plt.savefig(buffer_imagen, format='png', bbox_inches='tight')
#         buffer_imagen.seek(0)
#         imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
#         imagen_base64 = f'data:image/png;base64,{imagen_base64}'
#         plt.close(fig)
#         return imagen_base64
#     else:
#         return None

# def panel_encuesta_respuestas(request, encuesta_id):
#     encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
#     respuestas_filtradas = Respuesta.objects.filter(encuesta=encuesta)
#     if not respuestas_filtradas.exists():
#         return render(request, 'datastory/panel.html', {'error': 'No hay respuestas para esta encuesta.'})

#     preguntas_con_graficos = []

#     for pregunta in encuesta.preguntas.all():
#         if pregunta.tipo in ['seleccion_unica', 'seleccion_multiple']:
#             # Tu código existente para generar gráficos de barras
#             if pregunta.tipo in ['seleccion_unica', 'seleccion_multiple']:
#                 data_respuestas = Counter()
#                 for respuesta in respuestas_filtradas.filter(pregunta=pregunta):
#                     opciones = [opcion.strip() for opcion in respuesta.texto_respuesta.split(',')]
#                     data_respuestas.update(opciones)
#                 preguntas_con_graficos.append((pregunta.texto, generar_grafico_barras(data_respuestas), None, pregunta.tipo))

#         elif pregunta.tipo == 'texto_libre':
#             respuestas_texto_libre = [respuesta.texto_respuesta for respuesta in respuestas_filtradas.filter(pregunta=pregunta)]
            
#             # Agrupar las respuestas utilizando NLP
#             clusters = agrupar_respuestas_nlp(respuestas_texto_libre)
            
#             # Generar gráfico circular para mostrar la distribución de los clústeres
#             imagen_base64 = generar_grafico_circular(clusters)
            
#             # Agregar el gráfico circular a preguntas_con_graficos
#             preguntas_con_graficos.append(('Distribución de Clústeres', imagen_base64, clusters, pregunta.tipo))

#             # Mostrar una lista de respuestas relevantes agrupadas por clústeres
#             for cluster_id, respuestas_cluster in clusters.items():
#                 # Ordenar las respuestas por relevancia o cualquier otro criterio
#                 respuestas_cluster_ordenadas = sorted(respuestas_cluster, key=lambda x: x[0])
#                 preguntas_con_graficos.append((f'Cluster {cluster_id}', None, respuestas_cluster_ordenadas, pregunta.tipo))

#     context = {
#         'preguntas_con_graficos': preguntas_con_graficos,
#         'encuesta': encuesta,
#     }
#     return render(request, 'datastory/panel.html', context)

# def agrupar_respuestas_nlp(respuestas_texto_libre, num_clusters=3):
#     procesadas = [nlp(respuesta) for respuesta in respuestas_texto_libre]
#     # Asignar una clasificación a cada respuesta basada en la similitud con otras respuestas
#     # Utilizaremos el índice del cluster como clasificación
#     # Esta clasificación será útil para el gráfico y la lista desplegable
#     clusters = defaultdict(list)
#     for i, respuesta in enumerate(procesadas):
#         clusters[i % num_clusters].append((str(respuestas_texto_libre[i]), respuesta))

#     return clusters




# import spacy
# from collections import defaultdict, Counter
# import io
# import base64
# import matplotlib.pyplot as plt
# import pandas as pd
# from django.shortcuts import render, get_object_or_404
# from encuestas.models import Encuesta, Respuesta

# # Cargar el modelo de spaCy para el idioma correspondiente
# nlp = spacy.load("es_core_news_sm")

# def generar_grafico_barras(datos, etiquetas=None):
#     if datos:
#         df_respuestas = pd.DataFrame(list(datos.items()), columns=['Respuesta', 'Cantidad'])
#         df_respuestas = df_respuestas.sort_values(by='Cantidad', ascending=False)
#         fig, ax = plt.subplots(figsize=(10, 6))
#         bars = ax.bar(df_respuestas['Respuesta'], df_respuestas['Cantidad'])
#         ax.set_xlabel('Respuesta')
#         ax.set_ylabel('Cantidad')
#         plt.xticks(rotation=45, ha="right")

#         # Agregar etiquetas en las barras si se proporcionan
#         if etiquetas:
#             for bar, etiqueta in zip(bars, [etiquetas.get(resp, '') for resp in df_respuestas['Respuesta']]):
#                 yval = bar.get_height()
#                 ax.text(bar.get_x() + bar.get_width()/2, yval, f'#{etiqueta}', va='bottom', ha='center')

#         fig.patch.set_alpha(0)
#         plt.tight_layout()
#         buffer_imagen = io.BytesIO()
#         plt.savefig(buffer_imagen, format='png', bbox_inches='tight')
#         buffer_imagen.seek(0)
#         imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
#         imagen_base64 = f'data:image/png;base64,{imagen_base64}'
#         plt.close(fig)
#         return imagen_base64
#     else:
#         return None

# def agrupar_respuestas_nlp(respuestas_texto_libre, num_clusters=3):
#     procesadas = [nlp(respuesta) for respuesta in respuestas_texto_libre]
#     # Asignar una clasificación a cada respuesta basada en la similitud con otras respuestas
#     # Utilizaremos el índice del cluster como clasificación
#     # Esta clasificación será útil para el gráfico y la lista desplegable
#     clusters = defaultdict(list)
#     for i, respuesta in enumerate(procesadas):
#         clusters[i % num_clusters].append((str(respuestas_texto_libre[i]), respuesta))

#     return clusters

# def generar_grafico_circular(respuestas):
#     if respuestas:
#         # Contar las ocurrencias de cada respuesta
#         conteo_respuestas = Counter(respuestas)

#         # Preparar datos para el gráfico
#         categorias = list(conteo_respuestas.keys())
#         valores = list(conteo_respuestas.values())

#         # Crear el gráfico circular
#         fig, ax = plt.subplots(figsize=(10, 6))
#         ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)
#         ax.axis('equal')  # radio igual para que sea un círculo

#         # Convertir el gráfico a imagen base64
#         buffer_imagen = io.BytesIO()
#         plt.savefig(buffer_imagen, format='png')
#         buffer_imagen.seek(0)
#         imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
#         imagen_base64 = f'data:image/png;base64,{imagen_base64}'
        
#         plt.close(fig)
#         return imagen_base64
#     else:
#         return None

# def panel_encuesta_respuestas(request, encuesta_id):
#     encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
#     respuestas_filtradas = Respuesta.objects.filter(encuesta=encuesta)
#     if not respuestas_filtradas.exists():
#         return render(request, 'datastory/panel.html', {'error': 'No hay respuestas para esta encuesta.'})

#     preguntas_con_graficos = []

#     for pregunta in encuesta.preguntas.all():
#         if pregunta.tipo in ['seleccion_unica', 'seleccion_multiple']:
#             data_respuestas = Counter()
#             for respuesta in respuestas_filtradas.filter(pregunta=pregunta):
#                 opciones = [opcion.strip() for opcion in respuesta.texto_respuesta.split(',')]
#                 data_respuestas.update(opciones)
#             preguntas_con_graficos.append((pregunta.texto, generar_grafico_barras(data_respuestas), None, pregunta.tipo))
#         elif pregunta.tipo == 'texto_libre':
#             respuestas_texto_libre = [respuesta.texto_respuesta for respuesta in respuestas_filtradas.filter(pregunta=pregunta)]
            
#             # Agrupar las respuestas utilizando NLP
#             clusters = agrupar_respuestas_nlp(respuestas_texto_libre)
            
#             # Generar gráfico circular para mostrar la distribución de los clústeres
#             imagen_base64 = generar_grafico_circular(list(range(len(clusters))))
            
#             # Agregar cada clúster como una entrada en preguntas_con_graficos
#             for cluster_id, respuestas_cluster in clusters.items():
#                 preguntas_con_graficos.append((f'Cluster {cluster_id}', None, respuestas_cluster, pregunta.tipo))

#             # Agregar el gráfico circular a preguntas_con_graficos
#             preguntas_con_graficos.append(('Distribución de Clústeres', imagen_base64, None, pregunta.tipo))

#     context = {
#         'preguntas_con_graficos': preguntas_con_graficos,
#         'encuesta': encuesta,
#     }
#     return render(request, 'datastory/panel.html', context)



# import spacy
# from collections import defaultdict, Counter
# import io
# import base64
# import matplotlib.pyplot as plt
# import pandas as pd
# from django.shortcuts import render, get_object_or_404
# from encuestas.models import Encuesta, Respuesta

# # Cargar el modelo de spaCy para el idioma correspondiente
# nlp = spacy.load("es_core_news_sm")

# def generar_grafico_barras(datos, etiquetas=None):
#     if datos:
#         df_respuestas = pd.DataFrame(list(datos.items()), columns=['Respuesta', 'Cantidad'])
#         df_respuestas = df_respuestas.sort_values(by='Cantidad', ascending=False)
#         fig, ax = plt.subplots(figsize=(10, 6))
#         bars = ax.bar(df_respuestas['Respuesta'], df_respuestas['Cantidad'])
#         ax.set_xlabel('Respuesta')
#         ax.set_ylabel('Cantidad')
#         plt.xticks(rotation=45, ha="right")

#         # Agregar etiquetas en las barras si se proporcionan
#         if etiquetas:
#             for bar, etiqueta in zip(bars, [etiquetas.get(resp, '') for resp in df_respuestas['Respuesta']]):
#                 yval = bar.get_height()
#                 ax.text(bar.get_x() + bar.get_width()/2, yval, f'#{etiqueta}', va='bottom', ha='center')

#         fig.patch.set_alpha(0)
#         plt.tight_layout()
#         buffer_imagen = io.BytesIO()
#         plt.savefig(buffer_imagen, format='png', bbox_inches='tight')
#         buffer_imagen.seek(0)
#         imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
#         imagen_base64 = f'data:image/png;base64,{imagen_base64}'
#         plt.close(fig)
#         return imagen_base64
#     else:
#         return None

# def agrupar_respuestas_mejorado(respuestas_texto_libre, num_clusters=3):
#     procesadas = [nlp(respuesta) for respuesta in respuestas_texto_libre]
#     # Ahora vamos a asignar una clasificación a cada respuesta basada en la similitud con otras respuestas
#     # Utilizaremos el índice del cluster como clasificación
#     # Esta clasificación será útil para el gráfico y la lista desplegable
#     clusters = defaultdict(list)
#     for i, respuesta in enumerate(procesadas):
#         clusters[i % num_clusters].append((str(respuestas_texto_libre[i]), respuesta))

#     return clusters


# def generar_grafico_circular(respuestas):
#     if respuestas:
#         # Contar las ocurrencias de cada respuesta
#         conteo_respuestas = Counter(respuestas)

#         # Preparar datos para el gráfico
#         categorias = list(conteo_respuestas.keys())
#         valores = list(conteo_respuestas.values())

#         # Crear el gráfico circular
#         fig, ax = plt.subplots(figsize=(10, 6))
#         ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)
#         ax.axis('equal')  # radio igual para que sea un círculo

#         # Convertir el gráfico a imagen base64
#         buffer_imagen = io.BytesIO()
#         plt.savefig(buffer_imagen, format='png')
#         buffer_imagen.seek(0)
#         imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
#         imagen_base64 = f'data:image/png;base64,{imagen_base64}'
        
#         plt.close(fig)
#         return imagen_base64
#     else:
#         return None

# def panel_encuesta_respuestas(request, encuesta_id):
#     encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
#     respuestas_filtradas = Respuesta.objects.filter(encuesta=encuesta)
#     if not respuestas_filtradas.exists():
#         return render(request, 'datastory/panel.html', {'error': 'No hay respuestas para esta encuesta.'})

#     preguntas_con_graficos = []

#     for pregunta in encuesta.preguntas.all():
#         if pregunta.tipo in ['seleccion_unica', 'seleccion_multiple']:
#             data_respuestas = Counter()
#             for respuesta in respuestas_filtradas.filter(pregunta=pregunta):
#                 opciones = [opcion.strip() for opcion in respuesta.texto_respuesta.split(',')]
#                 data_respuestas.update(opciones)
#             preguntas_con_graficos.append((pregunta.texto, generar_grafico_barras(data_respuestas), None, pregunta.tipo))
#         elif pregunta.tipo == 'texto_libre':
#             respuestas_texto_libre = [respuesta.texto_respuesta.lower().strip() for respuesta in respuestas_filtradas.filter(pregunta=pregunta)]
#             preguntas_con_graficos.append((pregunta.texto, generar_grafico_circular(respuestas_texto_libre), None, pregunta.tipo))

#             clasificacion_respuestas = agrupar_respuestas_mejorado(respuestas_texto_libre)

#     context = {
#         'preguntas_con_graficos': preguntas_con_graficos,
#         'encuesta': encuesta,
#     }
#     return render(request, 'datastory/panel.html', context)









from django.shortcuts import render, get_object_or_404
from encuestas.models import Encuesta, Respuesta
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from collections import defaultdict, Counter
import re

def generar_grafico_barras(datos, etiquetas=None):
    if datos:
        df_respuestas = pd.DataFrame(list(datos.items()), columns=['Respuesta', 'Cantidad'])
        df_respuestas = df_respuestas.sort_values(by='Cantidad', ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df_respuestas['Respuesta'], df_respuestas['Cantidad'])
        ax.set_xlabel('Respuesta')
        ax.set_ylabel('Cantidad')
        plt.xticks(rotation=45, ha="right")

        # Agregar etiquetas en las barras si se proporcionan
        if etiquetas:
            for bar, etiqueta in zip(bars, [etiquetas.get(resp, '') for resp in df_respuestas['Respuesta']]):
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval, f'#{etiqueta}', va='bottom', ha='center')

        fig.patch.set_alpha(0)
        plt.tight_layout()
        buffer_imagen = io.BytesIO()
        plt.savefig(buffer_imagen, format='png', bbox_inches='tight')
        buffer_imagen.seek(0)
        imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
        imagen_base64 = f'data:image/png;base64,{imagen_base64}'
        plt.close(fig)
        return imagen_base64
    else:
        return None



def contar_palabras_comunes(respuesta1, respuesta2):
    palabras_respuesta1 = set(respuesta1.lower().split())
    palabras_respuesta2 = set(respuesta2.lower().split())
    return len(palabras_respuesta1.intersection(palabras_respuesta2))

def clasificar_respuestas(respuestas):
    clasificacion = {}
    for i, respuesta1 in enumerate(respuestas):
        conteo_palabras_comunes = 0
        for j, respuesta2 in enumerate(respuestas):
            if i != j:
                conteo_palabras_comunes += contar_palabras_comunes(respuesta1, respuesta2)
        clasificacion[respuesta1] = conteo_palabras_comunes
    return sorted(clasificacion.items(), key=lambda x: x[1], reverse=True)



def generar_grafico_circular(clasificacion_respuestas):
    if clasificacion_respuestas:
        # Definir las categorías y umbrales de coincidencia
        categorias = ['Pocas Coincidencias', 'Coincidencias Moderadas', 'Muchas Coincidencias']
        umbrales = [1, 3, 5]  # Define los umbrales para cada categoría
        
        # Clasificar las respuestas en las categorías correspondientes
        valores = [sum(value >= umbral for value in clasificacion_respuestas.values()) for umbral in umbrales]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # radio igual para que sea un circulo
        buffer_imagen = io.BytesIO()
        plt.savefig(buffer_imagen, format='png')
        buffer_imagen.seek(0)
        imagen_base64 = base64.b64encode(buffer_imagen.read()).decode('utf-8')
        imagen_base64 = f'data:image/png;base64,{imagen_base64}'
        plt.close(fig)
        return imagen_base64
    else:
        return None

def panel_encuesta_respuestas(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    respuestas_filtradas = Respuesta.objects.filter(encuesta=encuesta)
    if not respuestas_filtradas.exists():
        return render(request, 'datastory/panel.html', {'error': 'No hay respuestas para esta encuesta.'})

    preguntas_con_graficos = []

    for pregunta in encuesta.preguntas.all():
        if pregunta.tipo in ['seleccion_unica', 'seleccion_multiple']:
            data_respuestas = Counter()
            for respuesta in respuestas_filtradas.filter(pregunta=pregunta):
                opciones = [opcion.strip() for opcion in respuesta.texto_respuesta.split(',')]
                data_respuestas.update(opciones)
                print("Tipo de data_respuestas:", type(data_respuestas))
                print("Contenido de data_respuestas:", data_respuestas)
            preguntas_con_graficos.append((pregunta.texto, generar_grafico_barras(data_respuestas), None, pregunta.tipo))
        elif pregunta.tipo == 'texto_libre':
            respuestas_texto_libre = [respuesta.texto_respuesta.lower().strip() for respuesta in respuestas_filtradas.filter(pregunta=pregunta)]
            clasificacion_respuestas = defaultdict(int)
            for respuesta in respuestas_texto_libre:
                palabras = set(re.findall(r'\b\w+\b', respuesta))
                num_coincidencias = sum(any(palabra in otra_respuesta for palabra in palabras) for otra_respuesta in respuestas_texto_libre if otra_respuesta != respuesta)
                if num_coincidencias >= 5:
                    clasificacion_respuestas['Muchas Coincidencias'] += 1
                elif num_coincidencias >= 3:
                    clasificacion_respuestas['Coincidencias Moderadas'] += 1
                elif num_coincidencias >= 1:
                    clasificacion_respuestas['Pocas Coincidencias'] += 1

            # Si no hay respuestas, clasificacion_respuestas será un defaultdict(int) vacío
            preguntas_con_graficos.append((pregunta.texto, generar_grafico_circular(clasificacion_respuestas), clasificacion_respuestas, pregunta.tipo))

    context = {
        'preguntas_con_graficos': preguntas_con_graficos,
        'encuesta': encuesta,
        'coincidentes': clasificacion_respuestas,  # Pasamos siempre el diccionario al contexto
    }
    return render(request, 'datastory/panel.html', context)





