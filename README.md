# Prueba técnica Fapro
Reto técnico para la empresa Fapro, el cuál consiste en hacer web scraping con Python a una página para consultar la unidad de fomento (SII) de Chile.

# ¿En que consiste?

El Servicio de Impuestos Internos (SII) de Chile mantiene una tabla con los valores de la Unidad de Fomento actualizados para cada año. Tu desafío consiste en crear una API en Python que permita a los usuarios consultar el valor de la Unidad de Fomento para una fecha específica utilizando scraping.

- La API debe estar desarrollada en Python utilizando la librería "requests" u otra similar.
- Para la API puedes usar el Framework que mas te guste.
- No se puede utilizar Selenium debido al alto consumo de recursos que estas herramientas implican.
- La API debe permitir consultar el valor de la Unidad de Fomento para una fecha específica, la cual debe ser ingresada como parámetro en la solicitud.
- La fecha mínima que se puede consultar es el 01-01-2013, y no hay fecha máxima, ya que la tabla se actualiza constantemente.
- La API debe devolver el valor de la Unidad de Fomento correspondiente a la fecha consultada.
- La respuesta de la API debe estar en formato JSON.

Para ayudarte en el desarrollo de este desafío, puedes utilizar la tabla de valores de la Unidad de Fomento actualizados para cada año que se encuentra en el siguiente enlace: https://www.sii.cl/valores_y_fechas/uf/uf2023.htm

# Requisitos de desarrollo

Se debe desarrollar una API para consultar la unidad de fomento (SII) por medio de un endpoint, el cuál tendrá como función hacer scrapping a la página de sii para obtener el valor de la tabla de registros de Unidad de Fomento que se actualiza cada año

Endpoint:

- GET: Obtiene el valor de unidad de fomento (SII) al pasarle la fecha como parámetro

# Requisitos del entorno de proyecto

- Django==3.0.8
- djangorestframework==3.11.0
- drf-yasg
- requests
- beautifulsoup4
- python-decouple

# Razonamiento

Este proyecto está desarrollado con Python 3.11.3, Django 3.0.8 y Django REST Framework 3.11.0 debido a su documentación y robustez para crear REST Apis mediante este framework.

- Para levantar el entorno se debe levantar la imagen por medio del contenedor Docker, para su fácil adaptación e instalación en nuevos equipos. 

- Se decidió usar Swagger para la documentación de la API y aumentar su facilidad de uso, con drf-yasg de Django Rest Framework.

![image](https://github.com/kike1996luis/Fapro-scraping/assets/44822982/04f1dbdc-2f93-4e12-ba8d-cc5789481d95)

- Se separararon las variables de entorno delicadas (SECRET_KEY) en un archivo .env con Python Decouple, con la finalidad de no mostrar datos sensibles en el entorno en el cual se despliega el proyecto (vease archivo .env.example), para asegurar que la aplicación cumpla con uno de los requisitos del Twelve Factor App el cuál es el de "Configuración".

- Se hicieron un total de 11 tests unitarios, el cuál se pueden correr localmente, y también se implementó un proceso CI/CD hook con GitHub actions, el cual tiene como objetivo correr los tests unitarios cada vez que un usuario haga un push o un pull request en el repositorio, esto debido para  procurar siempre que el sistema sea funcional.

![image](https://github.com/kike1996luis/Fapro-scraping/assets/44822982/04facdbf-0c08-4766-b458-0193e340f828)

# Instalación

- Por seguridad y para no mostrar datos sensibles a la hora de desplegar el código en GitHub, siguiendo parte de la metodología twelve-factor el archivo de configuración se establece con la variable de entorno de Django .env, el cuál está excluido del repositorio. Se debe crear el archivo .env en la raíz del proyecto y establecer tu SECRET_KEY para tu entorno, existe un archivo llamado .env.example de modo de ejemplo:

```SECRET_KEY = '....your secret key ....'```

- Para instalar el proyecto se usará Docker para hacer build de la imagen al contenedor.

- Una vez tengas instalado y encendido el entorno de docker, vete a la raíz del proyecto y ejecuta este comando para instalar la imagen de Python 3.11.3 y cada dependencia necesaria en el proyecto:

```docker compose build```

- Cuando finalice la instalación ejecuta el siguiente comando para correr el servidor:

```docker compose up```

- Ya corriendo el servidor dirígete a [http://localhost:8000/](url) y verás la documentación Swagger para poder probar la API

# Tests Unitarios

Como se mencionó anteriormente, el proyecto cuenta con un total de 11 tests unitarios para probar el funcionamiento de la aplicación. Para ejecutarlos debes introducir el siguiente comando:

```docker compose run web python manage.py test```

Para ejecutar un test unitario de manera individual puedes hacerlo de esta manera:

```docker compose run web python manage.py test src.tests.test_ufoment_service.FomentUnitServiceTest.test_correct_date```

Todos los tests se encuentran en la carpeta ```src\tests```

# Diseño y arquitectura de proyecto

Al trabajar con Django se establece la arquitectura MVC (Modelo Vista Controlador) el cual logra separar cada funcionalidad por responsabilidad única manteniendo la abstracción en cada uno.

La carpeta donde se establece la configuración principal ```settings.py``` está en la carpeta "fapro", la cual se encuentra separada del código fuente debido a que tiene una responsabilidad única para consulta.

El código fuente se encuentra almacenado en la carpeta "src", el cual para permitir la modulación tiene las siguientes carpetas:

- apps: Almacena las aplicaciones del proyecto
- core: Archivos que se usan como núcleo para el funcionamiento del proyecto
- services: Archivos que sirven como servicio para ser llamados desde los endpoint, permitiendo la segregación de interfaz
- tests: Carpeta que contiene los tests unitarios

# Principios SOLID utilizados

En este proyecto se procuró usar los principios SOLID para eliminar malos diseños, evitar la refactorización y construir un código más eficiente y fácil de mantener, debido a la simplicidad del proyecto solo se aplicaron algunos de éstos principios, los cuales son los más necesarios en el desarrollo de Software.

Entre los principios SOLID implementados en este proyecto se pueden destacar:

- Responsabilidad Única (Single Responsability):
Cada clase y método del proyecto tiene un único funcionamiento y responsabilidad.

- Principio de abierto y cerrado (Open/Closed Principle):
Cada entidad tiene un principio único el cuál puede heredarse más no modificarse, ya que éste perdería su propósito.

- Principio de inversión de Dependencias (Dependency Inversion Principle):
Ninguna clase depende de otra dependencia para poder funcionar, solo depende de la interfaz pública para su funcionamiento.

- Segregación de interfaz (Interface Segregation Principle):
Se procura no sobrecargar la clase con funcionalidades extensas y genéricas, si no que se divide en interfaces pequeñas y específicas.
