# API bonos IAMC
API para obtención de información acerca de los Bonos de Reestructuración de Deuda listados en IAMC.
Base de datos localizada en Alphacast.

## Descripción
Se trata de una API utilizada para obtener información sobre los distintos bonos de reestructuración de deuda que se encuentran listados en IAMC, base 2011.
La base de datos se encuentra alojada en Alphacast: https://www.alphacast.io/datasets/7961.
La API se encuentra montada en el servidor Heroku.

Cuenta con diferentes endpoints que permiten obtener mediante distintos filtros, la información correspondiente a los bonos mencionados.


## Endpoints
- HOME: https://fastapi-bonos.herokuapp.com/ --> WELCOME
- GET: /tickers --> Obtención de los códigos correspondientes a cada unos de los bonos del dataset
- GET: /bonos/{codigo} --> Obtención de la información correspondiente al bono seleccionado en base a su codigo
- GET: /tick_and_year --> Obtención de la información correspondiente al bono seleccionado en base a su codigo y año
- GET: /bonos/year/{year} --> Obtención de toda la serie correspondiente a los bonos, filtrado de acuerdo al año seleccionado
- GET: /currency_and_size --> Obtención de la información correspondiente a cada bono en base a la moneda (pesos/dolares) seleccionada como parametro. Adiionalmente se debe pasar como parámetro un size (ejemplo 100) para indicar la cantidad de datos a visualizar.
- GET: /parity --> Obtención de la serie de bonos, cuyos valores de paridad son mayores al valor seleccionado
- GET: /yield --> Obtención de la serie de bonos, cuyos valores de yield_anual son mayores al valor seleccionado

Para mayor detalle, acceder al la documentación de la API: https://fastapi-bonos.herokuapp.com/docs

![image](https://user-images.githubusercontent.com/69882938/176984045-fefb2bd9-8773-4f0f-8d79-3f357cec1de2.png)
