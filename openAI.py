import os
import openai
openai.api_key = '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'

datos = ''

def chatgpt_req(datos):

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": f"Te proporcionaré datos desorganizados de una factura comercial para una operacion de logistica internacional y necesito que los reorganices siguiendo la estructura: IdFactura,FechaFactura, Incoterm, PaisFacturacion, Moneda, PaisFactor, ValorFactura(valor total de la factura), FraccionArancelaria, Descripción (incluye solo 2 o 3 palabras para describir el producto), ValorComercial, Cantidad, PaisOrigen. Omite los campos que no existan en los datos.\n\nPor favor, calcula la fracción arancelaria para cada descripción y añádela al archivo csv en el campo FraccionArancelaria.\n\nElimina las comillas dobles internas de las descripciones y agrega comillas externas a cada celda.\n\nFinalmente, necesito que me entregues el archivo csv en formato de texto de tal manera que pueda convertirlo automáticamente a csv para usarlo en Excel. Es crucial que no expliques el resultado, solo necesito el archivo \ncsv.\n\nUn ejemplo del resultado esperado sería(IdFactura e Incoterm no estaban en la data):\n\nIdFactura, FechaFactura, Incoterm, PaisFacturacion, Moneda, PaisFactor, ValorFactura, Fracción Arancelaria, Descripción, ValorComercial, Cantidad, PaisOrigen\n\" \",\"6/07/2023\", \"\", \"CHN\", \"USD\", \"USA\", \"2802\", \"85021100\", \"Diesel generator 30kva\", \"800\", \"1 set\", \"CHN\"\n\" \",\"6/07/2023\", \"\", \"CHN\", \"USD\", \"USA\", \"2802\", \"85021100\", \"Diesel generator 50kva\", \"950\", \"1 set\", \"CHN\"\n\" \",\"6/07/2023\", \"\", \"CHN\", \"USD\", \"USA\", \"2802\", \"85021100\", \"Diesel generator 55kva\", \"1052\", \"1 set\", \"CHN\"\n\nA continuación, te proporciono los datos desorganizados:\n\n{datos}"
        },
        {
        "role": "user",
        "content": ""
        }
    ],
    temperature=0,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    print(response)
    print(response.choices[0].message)

    return(response.choices[0].message.content)