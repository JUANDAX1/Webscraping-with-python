#!/usr/bin/env python
# coding: utf-8

# <div style="text-align: center;">
#     <img src="https://i.imgur.com/zTLujrk.png" alt="JPierre-DATA ANALIST" 
#          style="width:300px; float: right; margin: 30px 10px;"></img>
# 	<div style=""><p style="font-weight: bold; font-size: 26px; color: #444654; 
#       float:  left; margin: 50px 30px;">WebScraping con Python y BS4</p>
# 	</div>
# </div>

# <img src="https://i.imgur.com/4gX5WFr.png" alt="JPierre-DATA ANALIST"></img>

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Función-controladora" data-toc-modified-id="Función-controladora-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Función controladora</a></span></li><li><span><a href="#Función-de-Scraping" data-toc-modified-id="Función-de-Scraping-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Función de Scraping</a></span></li><li><span><a href="#Entrada-de-las-url-a-consultar" data-toc-modified-id="Entrada-de-las-url-a-consultar-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Entrada de las url a consultar</a></span></li><li><span><a href="#Lanzamiento-del-proceso" data-toc-modified-id="Lanzamiento-del-proceso-4"><span class="toc-item-num">4&nbsp;&nbsp;</span><strong>Lanzamiento del proceso</strong></a></span></li><li><span><a href="#EDA" data-toc-modified-id="EDA-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>EDA</a></span></li><li><span><a href="#Consideraciones-finales:" data-toc-modified-id="Consideraciones-finales:-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Consideraciones finales:</a></span></li></ul></div>

# <img src="https://i.imgur.com/4gX5WFr.png" alt="JPierre-DATA ANALIST"></img>

#  <p style="font-weight: bold; font-size: 26px; color: #444654; 
#       float:  left; margin: 20px 20px;">Introducción</p>

# **Problema que soluciona este proyecto**

# <span style="font-family: Arial; font-size: 12pt;">
#    
# Como analistas de datos, nos enfrentamos al desafío constante de obtener una cantidad suficiente de datos para llegar a conclusiones confiables. La obtención de datos se vuelve aún más complicada debido a la dificultad para acceder a fuentes actualizadas y a la necesidad de recopilar manualmente información de páginas que no ofrecen servicios de API.
# 
# Este proyecto aborda de manera efectiva estas dificultades al proporcionar una solución integral. Su objetivo principal es desarrollar una herramienta que nos permita adquirir datos de productos a gran escala. Estos datos se convertirán en la base para análisis de mercado, comparación de productos y seguimiento de variaciones de precios. A pesar de ser un proyecto experimental, destaca por su enorme potencial de escalabilidad. El resultado final es una solución completamente funcional.
# 
# Las tecnologías fundamentales utilizadas en este proyecto son Python, Pandas y Beautiful Soup.
#  
# 
# </span>

# **¿Cómo funciona?**

# <span style="font-family: Arial; font-size: 12pt;">
# El flujo de este proceso sigue el diseño de una aplicación que acepta URL de páginas para extraer datos específicos. Posteriormente, estos datos se almacenan en un único archivo como un DataFrame, lo que permite la aplicación de técnicas analíticas de negocio. Es crucial adaptar el código para una página específica, donde la extracción de datos se realiza a través de selectores de CSS.
#     
# 
# Este enfoque proporciona una solución eficiente y centrada en la personalización, permitiendo la flexibilidad necesaria para abordar las particularidades de cada página web objetivo. La adaptabilidad del código es esencial para asegurar la extracción precisa de datos según la estructura y los selectores específicos de CSS de la página en cuestión.
# </span>

# # Función controladora

# In[1]:


# paso 1

import requests
from bs4 import BeautifulSoup
import pandas as pd


def controladora(url_list, contador_ejecuciones):
    
    from IPython.display import Markdown, display

    # Inicializar variables
    url_consultar = None

    # Iterar mientras haya URLs en la lista y el contador sea mayor que cero
    while url_list and contador_ejecuciones > 0:
        # Obtener la siguiente URL de la lista
        url_consultar = url_list.pop(0)

        # Llamar a la función web_scraping con la URL actual
        try:
            respuesta = web_scraping(url_consultar)
            # Si la respuesta es exitosa, imprimir mensaje
            print(f"Consulta web exitosa para {url_consultar}")
        except Exception as e:
            # Si hay un error, imprimir mensaje de error en formato HTML y continuar con la siguiente URL
            mensaje_error = f"<font color='red'>Fallo en la consulta web para {url_consultar}. Mensaje de error: {e}</font>"
            display(Markdown(mensaje_error))
            continue

        # Actualizar el contador de ejecuciones
        contador_ejecuciones -= 1

    # Imprimir mensaje cuando se complete el proceso
    print('Proceso completado con éxito!')


# # Función de Scraping

# In[2]:


# paso 2

def web_scraping(url):
    # Hacer la solicitud HTTP a la URL
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Crear el objeto BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Definir los selectores para cada variable
        selector_nombre = 'div.ui-search-item__group.ui-search-item__group--title > a > h2'
        selector_precio = 'span.andes-money-amount__fraction'
        selector_raiting = 'span.ui-search-reviews__rating-number'
        selector_url_img = 'div.andes-carousel-snapped__controls-wrapper > div > div > div > img'
        selector_descuento = 'div.container-promotion > div > div'
        selector_envio = 'div.ui-search-item__group.ui-search-item__group--shipping > div > p'

        # Inicializar listas para almacenar valores
        nombres = []
        precios = []
        ratings = []
        urls_img = []
        descuentos = []
        envios = []

        # Obtener todas las secciones con la etiqueta 'li.ui-search-layout__item'
        secciones = soup.find_all('li', class_='ui-search-layout__item')

        # Iterar sobre cada sección
        for seccion in secciones:
            # Obtener el nombre del producto
            nombre = seccion.select_one(selector_nombre)
            nombres.append(nombre.text.strip() if nombre else 'nd')

            # Obtener el precio del producto
            precio = seccion.select_one(selector_precio)
            precios.append(precio.text.strip() if precio else 'nd')

            # Obtener el rating del producto
            rating = seccion.select_one(selector_raiting)
            ratings.append(rating.text.strip() if rating else 'nd')

            # Obtener la URL de la imagen del producto
            url_img = seccion.select_one(selector_url_img)
            urls_img.append(url_img['data-src'].strip() if url_img else 'nd')

            # Obtener el descuento del producto
            descuento = seccion.select_one(selector_descuento)
            descuentos.append(descuento.text.strip() if descuento else 'nd')

            # Obtener el tipo de envío del producto
            envio = seccion.select_one(selector_envio)
            envios.append(envio.text.strip() if envio else 'nd')

        # Crear un diccionario con las listas obtenidas
        datos_dict = {
                'Nombre': nombres,
                'Precio': precios,
                'Rating': ratings,
                'URL Imagen': urls_img,
                'Descuento': descuentos,
                'Envío': envios
            }
        
        try:
            # Intentar cargar el DataFrame existente con datos externos
            #esto funciona como una carga continua de datos.
            data = pd.read_pickle('Proj_ML_3.pkl')

            # Si el DataFrame existe, agregar nuevos datos y junta lo nuevo y lo externo aqui
            data = pd.concat([data, pd.DataFrame.from_dict(datos_dict)])

        except FileNotFoundError:
            # Si el DataFrame no existe, crear uno nuevo con los datos
            data = pd.DataFrame.from_dict(datos_dict)

        # Guardar el DataFrame en un archivo pickle para futuras ejecuciones
        data.to_pickle('Proj_ML_3.pkl')
        
        return 'exitosa'
    else:
        print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        return 'falla conexión'
    


# # Entrada de las url a consultar

# In[3]:


# pso 3
# Lista de url a consultar - ingresa el listado de las url sin olvidar separalas por comas
urls_a_consultar = [
    'https://listado.mercadolibre.cl/funko-pops#D[A:funko%20pops]',
    'https://listado.mercadolibre.cl/juegos-juguetes/munecos-munecas/figuras-accion/funko-pops_Desde_51_NoIndex_True',
    'https://listado.mercadolibre.cl/juegos-juguetes/munecos-munecas/figuras-accion/funko-pops_Desde_101_NoIndex_True',
    'https://listado.mercadolibre.cl/juegos-juguetes/munecos-munecas/figuras-accion/funko-pops_Desde_151_NoIndex_True',
    'https://listado.mercadolibre.cl/juegos-juguetes/munecos-munecas/figuras-accion/funko-pops_Desde_201_NoIndex_True'
]


# **Monitreo previo al controlador**

# In[4]:


#  paso 4
contador_inicial = len(urls_a_consultar)
print(f'Cantidad de paginas a consultar= {contador_inicial}')


# # **Lanzamiento del proceso**

# In[5]:


# paso 5 lamada a la funcion principal
controladora(urls_a_consultar, contador_inicial)


# .

# # EDA

# In[6]:


mlscrap = pd.read_pickle('Proj_ML_3.pkl')
mlscrap.head()


# In[7]:


mlscrap.info()


# In[8]:


precio_df = mlscrap[['Precio']].astype(float)
precio_df.describe().T


# In[9]:


mlscrap.duplicated().sum()


# In[10]:


mlscrap.drop_duplicates(inplace=True)


# .

# # Consideraciones finales:

# <span style="font-family: Arial; font-size: 12pt; color: #444654;">     
# Los proyectos de Scraing deben utilizarse con rsponsabilidad y precausión para no causar daños al propietrio de la pagina web. SI una pagina web ofrece API, es mejor utilzar esa opción en lugar de metodos de Scraping. Este proyecto, aunque es funcional, fue hecho con una finalidad experimental y académica. </span>

# <div style="text-align: center; background: linear-gradient(to right, #8E44AD, #3498DB); padding: 10px;">
#     <a href="https://github.com/JUANDAX1" style="color: #fff; text-decoration: none; font-size: 18px;">
#         Visita mi perfil en GitHub ➡️
#     </a>
# </div>
# 

# .
