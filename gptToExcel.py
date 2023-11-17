import csv
import io

data = "\" \",\"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"8983.33\", \"84295900\", \"Backhoe Loader\", \"8983.33\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"466.67\", \"84671900\", \"Hammer Chisel\", \"466.67\", \"2\", \"CHN\"\n \" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"266.67\", \"84314100\", \"4 in 1 Bucket\", \"266.67\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"83.33\", \"84314100\", \"Digging Bucket\", \"83.33\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"105.00\", \"40112000\", \"Tyre+Rim 14-17.5\", \"105.00\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"180.00\", \"40112000\", \"Tyre+Rim 19.5L-24\", \"180.00\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"1600.00\", \"87019010\", \"Farm Tractor\", \"1600.00\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11685.00\", \"84082010\", \"Diesel Engine\", \"11685.00\", \"1\", \"CHN\""
data2 = "\"SR-Z20230,706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"1200\",\"\",\"DHD3.5 hammer\",\"120\",\"10\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"1110\",\"\",\"DHD340 hammer\",\"185\",\"6\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"325\",\"\",\"DHD3.5-102mm bit\",\"65\",\"5\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"320\",\"\",\"tricone bit\",\"320\",\"1\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"450\",\"\",\"9 3/4 bit\",\"450\",\"1\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"40\",\"\",\"air filter assembly\",\"20\",\"2\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"60\",\"\",\"air filter main core\",\"10\",\"6\",\"CN\"\n\"SR-Z20230706A\",\"5/07/2023\",\"\",\"CN\",\"USD\",\"MX\",\"40\",\"\",\"air filter main core\",\"10\",\"4\",\"CN\"" 
data3 = "\" \", \"August 3, 2010\", \"\", USA, USD, USA, 25.00, \"\", \"Academic research samples\", 25.00, 1 box, USA"
data4 = "\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"84295900\", \"Backhoe Loader 388\", \"8983.33\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"84671900\", \"Hammer with Chisel Pick\", \"466.67\", \"2\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"84314100\", \"4 in 1 Bucket\", \"266.67\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"84314100\", \"300mm Width Bucket for Digging\", \"83.33\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"40112000\", \"Tyre+Rim 14-17.5\", \"105\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"40112000\", \"Tyre+Rim 19.5L-24\", \"180\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"87019010\", \"50 HP 4x4 Farm Tractor\", \"1600\", \"1\", \"CHN\"\n\" \", \"29/06/2023\", \"EXW\", \"CHN\", \"USD\", \"MEX\", \"11970\", \"84089099\", \"4 Cylinder Diesel Engine\", \"11685\", \"1\", \"CHN\""
data5 = "\"IdFactura\",\"FechaFactura\",\"Incoterm\",\"PaisFacturacion\",\"Moneda\",\"PaisFactor\",\"ValorFactura\",\"FraccionArancelaria\",\"Descripci\u00f3n\",\"ValorComercial\",\"Cantidad\",\"PaisOrigen\"\n\" \",\"August 3, 2010\",\" \",\"USA\",\"USD\",\"USA\",\"25.00\",\" \",\"Academic research samples\",\"25.00\",\"1 box\",\"USA\""


def convertToExcel(data):
# Replace double spaces with a single space, and then split the data into lines
    data = data.split('\n')

    print(data)

    # Create a CSV file in memory
    output = io.StringIO()
    csv_writer = csv.writer(output)

    headers = ["IdFactura", "FechaFactura", "Incoterm", "PaisFacturacion", "Moneda", "PaisFactor", "ValorFactura",
               "Fraccion Arancelaria", "Descripcion", "ValorComercial", "Cantidad", "PaisOrigen"]

    # Write the headers to the CSV file
    csv_writer.writerow(headers)

    # Write the data to the CSV file
    for line in data:
        excel_row = []
        if headers[0] in line:
            continue
        row = line.split('",')

        for cell in row: 
            newCell = cell.replace('"', '')
            newCell = f'{newCell}'
            excel_row.append(newCell)
        print(excel_row)
        csv_writer.writerow(excel_row)

    # Get the CSV data as a string
    csv_data = output.getvalue()

    print(csv_data)
