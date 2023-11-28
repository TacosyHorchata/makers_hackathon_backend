import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

datos = ''

def chatgpt_req(datos, csvHeaders, example):

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": f"""
        I will provide you with disorganized data from a commercial invoice for an international logistics operation 
        and need you to rearrange it following the structure: 
        {csvHeaders}. Omit fields that do not exist in the data.\n\n
        Remove double quotes within descriptions and add external quotes to each cell.\n\n
        Finally, I need you to deliver the CSV file in text format so that I can automatically convert it to CSV for use in Excel. 
        It is crucial that you do not explain the result; I only need the CSV file.\n\n
        An example of the expected result would be:\n\n
        {example}
        \n\nBelow, I provide you with the disorganized data:\n\n{datos}"""
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

#1er prompt
#"Te proporcionaré datos desorganizados de una factura comercial para una operacion de logistica internacional y necesito que los reorganices siguiendo la estructura: {csvHeaders}. Omite los campos que no existan en los datos.\n\nPor favor, calcula la fracción arancelaria para cada descripción y añádela al archivo csv en el campo FraccionArancelaria.\n\nElimina las comillas dobles internas de las descripciones y agrega comillas externas a cada celda.\n\nFinalmente, necesito que me entregues el archivo csv en formato de texto de tal manera que pueda convertirlo automáticamente a csv para usarlo en Excel. Es crucial que no expliques el resultado, solo necesito el archivo \ncsv.\n\nUn ejemplo del resultado esperado sería(IdFactura e Incoterm no estaban en la data):\n\nIdFactura, FechaFactura, Incoterm, PaisFacturacion, Moneda, PaisFactor, ValorFactura, Fracción Arancelaria, Descripción, ValorComercial, Cantidad, PaisOrigen\n\" \",\"6/07/2023\", \"\", \"CHN\", \"USD\", \"USA\", \"2802\", \"85021100\", \"Diesel generator 30kva\", \"800\", \"1 set\", \"CHN\"\n\" \",\"6/07/2023\", \"\", \"CHN\", \"USD\", \"USA\", \"2802\", \"85021100\", \"Diesel generator 50kva\", \"950\", \"1 set\", \"CHN\"\n\" \",\"6/07/2023\", \"\", \"CHN\", \"USD\", \"USA\", \"2802\", \"85021100\", \"Diesel generator 55kva\", \"1052\", \"1 set\", \"CHN\"\n\nA continuación, te proporciono los datos desorganizados:\n\n{datos}"