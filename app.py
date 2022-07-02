# Python
import json
import pandas as pd

# FastApi

from fastapi import FastAPI, HTTPException
from fastapi import status
from fastapi import Path, Query

# Modulos

from queries.data import df_bonos_iamc, df_pesos, df_dolares, list_tickers
# from queries.data import df_bonos_iamc_json

tags_metadata = [
  {
    "name": "bonos",
    "description": "bonos endpoint",
    "externalDocs": {
            "description": "Fuente: Alphacast",
            "url": "https://www.alphacast.io/datasets/7961",
        }, 
  }
]

app = FastAPI(title="API bonos IAMC (base=2011)", 
              description= "Obtencion de información sobre bonos argentinos listados en IAMC",
              version= "0.0.2",
              openapi_tags=tags_metadata
                )

# Welcome

@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    summary="Welcome",
    tags=["Welcome"]
    )
async def welcome_api():
    return "Welcome to API from IAMC_Bonds"

# Tickers

@app.get(
    path='/tickers',
    status_code=status.HTTP_200_OK,
    summary="Get Tickers",    
    tags=["Bonos_IAMC"]
    )
async def get_tickers():
    """
        Obtención de los códigos correspondientes a cada unos de los bonos del dataset
    """       
    return list_tickers

# Por el momento queda deprecada ya que es mucha información la que muestra

# @app.get(
#     path='/bonos',
#     status_code=status.HTTP_200_OK,
#     summary="Get all information"
#     )
# async def get_all_bonds():
#     """
#         Obtención de toda la serie correspondiente a la totalidad de los bonos del dataset
#     """        
#     return df_bonos_iamc_json

# Bonos por Codigo

@app.get(
    path='/bonos/{codigo}',
    status_code=status.HTTP_200_OK,
    summary="Get information about a ticker",
    tags=["Bonos_IAMC"]
    )
async def get_bond(
    codigo:str = Path(...,
                      title="Ticker",
                      description="Ingresar un bono listado en la base de datos", 
                      min_length=1,
                      example="GD46D")                                    
    ):
    """
        Obtención de la información correspondiente al bono seleccionado en base a su codigo
    """        
    df = df_bonos_iamc[df_bonos_iamc["Codigo"]==codigo]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono no encontrado")

# Bonos por Codigo y Año

@app.get(
    # path='/bonos/data/{codigo}/{year}',
    path='/tick_and_year',
    status_code=status.HTTP_200_OK,
    summary="Get information by year and ticker",
    tags=["Bonos_IAMC"]
    )
async def get_bond_by_tick_year(
    codigo:str = Query(..., min_length=1, title="Bono solicitado",
                      description="Ticker del bono solicitado", example="GD46D"),
    year:int = Query(...,title="Año solicitado",
                      description="Año solicitado", example=2022)
    ):

    """
        Obtención de la información correspondiente al bono seleccionado en base a su codigo y año
    """        
    df = df_bonos_iamc[(df_bonos_iamc["Codigo"]==codigo) & (df_bonos_iamc["year"]==year)]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Bono o año no encontrado")

# Bonos por Año

@app.get(
    path='/bonos/year/{year}',
    status_code=status.HTTP_200_OK,
    summary="Get all information about tickers filter by year",
    tags=["Bonos_IAMC"]
    )
async def get_bond_by_year(
    year:int = Path(...,
                    title="Year",
                    description="Ingresar un año para obtener toda la informacion del año seleccionado",                     
                    example=2022)
    ):
    """
        Obtención de toda la serie correspondiente a los bonos, filtrado de acuerdo al año
        seleccionado
    """        
    df = df_bonos_iamc[df_bonos_iamc["year"]==year]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js        
    raise HTTPException(status_code=404, detail="Fecha no encontrada")

# Bonos por moneda y tamaño

@app.get(
    # path='/bonos/moneda/{moneda}/{size}',
    path='/currency_and_size',
    status_code=status.HTTP_200_OK,
    summary="Get information by currency and size",
    tags=["Bonos_IAMC"]
    )
async def get_bond_by_currency(
    moneda:str = Query(..., title="Moneda a seleccionar",
                        description="Seleciionar la moneda del boto dolares o pesos",
                        example="dolares"),
    size:int = Query(..., title="Cantidad de registros",
                        description="Seleciionar la cantidad de registros que desea obtener",
                        example=50)
    ):
    """
        Obtención de la información correspondiente a cada bono en base a la moneda (pesos/dolares)
        seleccionada como parametro. Adiionalmente se debe pasar como parámetro un size (ejemplo 100)
        para indicar la cantidad de datos a visualizar.
    """    
    if moneda=="pesos":        
        df = df_pesos.iloc[:size]
        if len (df)!=0:            
            js = json.loads(df.to_json(orient = 'records'))            
            return js
    elif moneda=="dolares":        
        df = df_dolares.iloc[:size]
        if len (df)!=0:            
            js = json.loads(df.to_json(orient = 'records'))            
            return js
    raise HTTPException(status_code=404, detail="Moneda no encontrada")

# Bonos por paridad

@app.get(
    # path='/bonos/paridad/{valor_paridad}',
    path='/parity',       
    status_code=status.HTTP_200_OK,
    summary="Get information by parity",
    tags=["Bonos_IAMC"]
    )
def get_bond_by_parity(
    valor_paridad:int = Query(..., title="Bonos por Paridad",
                            description="Seleccionar Bonos en los cuales su paridad sea mayor a la indicada",
                            example=40)
    ):
    """
        Obtención de la serie de bonos, cuyos valores de paridad son mayores al valor
        seleccionado
    """        
    df = df_bonos_iamc[df_bonos_iamc["Paridad"]>valor_paridad]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Valor de paridad no encontrado")

# Bonos por yield

@app.get(
    # path='/bonos/yield/{yield_}',
    path='/yield',
    status_code=status.HTTP_200_OK,
    summary="Get information by yield",
    tags=["Bonos_IAMC"]
    )
def get_bond_by_Yield_Anual(
    yield_:int = Query(..., title="Bonos por Yield",
                     description="Seleccionar Bonos en los cuales su yield anual sea mayor a la indicada",
                     example=40)
    ):
    """
        Obtención de la serie de bonos, cuyos valores de yield_anual son mayores al valor
        seleccionado
    """        
    df = df_bonos_iamc[df_bonos_iamc["Yield_Anual"]>yield_]    
    if len (df)!=0:
        js =  json.loads(df.to_json(orient = 'records'))
        return js
    raise HTTPException(status_code=404, detail="Valor de paridad no encontrado")
 


