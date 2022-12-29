# API-Web Scrapping
## Archivos
- main.py: fichero de python que contiene el código para la extracción de datos de las apis, la web y la creación del pdf.
- requirements.txt: fichero que contiene las librerías necesarias para el correcto funcionamiento del código.
- config.txt: fichero que contiene los urls necesarios para el funcionamiento de main.py, además de los headers necesarios para la extracción de datos de las apis.
- team.pdf: fichero que contiene los datos de cada jugador del equipo introducido
---
## Descripción del script de python
El script se ha desarrollado con una estructura de ETL, en la cual se extraen los datos primero (tanto de las APIs como de las webs), se transforman, y se cargan en un pdf y por pantalla.
El programa funciona de la siguiente forma: se le pide al usuario una clave del equipo del que desea ver la predicción y las estadísticas por jugador. La entrada será un string de 3 caracteres mayúsculas que deban coincidir con la clave del equipo deseado (Ejemplo: Los Angeles Lakers = LAL). Lo siguiente que va a hacer es un scrapping para obtener el logo de dicho equipo y adjuntarlo como cabecera del pdf. Luego, filtramos los datos extraídos de la API para quedarnos únicamente con los jugadores de dicho equipo. En el pdf se mostrarán únicamente las estadñisticas que se han considerado más importantes para el análisis. Por último, se creará el pdf con las estadísticas de cada jugador del equipo introducido y se enseñará por pantalla el próximo partido del equipo introducido, así como la predicción de dicho partido. Dicha predicción está basada en el scrapping realizado en una página de apuestas deportivas.
