import os
import json
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
RESULT_FOLDER = os.getenv('RESULT_FOLDER')

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

current_dir = os.path.dirname(os.path.abspath(__file__))
result_path = os.path.join(current_dir, RESULT_FOLDER)

for folder in [result_path]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def ejecutar_script_deteccion(file_path,user):
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    filename, image_extension = os.path.splitext(os.path.basename(file_path))

    # Crear una carpeta por usuario
    result_file =  os.path.join(result_path, user,now)
    if not os.path.exists(result_file):
        os.makedirs(result_file)

    resultado_filename = f'image_analyzed{image_extension}'
    resultado_path = os.path.join(result_file, resultado_filename)
    return_path= RESULT_FOLDER+'/'+user+'/'+now+'/'+resultado_filename

    json_filename = f'{now}_resultados.json'
    json_output_path = os.path.join(result_file, json_filename)
    
    os.system(f'python analyzer.py "{file_path}" "{json_output_path}" "{resultado_path}"')

    # Leer el archivo JSON de resultados
    with open(json_output_path, 'r') as json_file:
        result = json.load(json_file)

    # Guardar los resultados en Supabase
    # guardar_resultados_en_supabase(user, resultado_path, result)

    return return_path, result

# def guardar_resultados_en_supabase(user, resultado_path, result):
#     # Prepara los datos a insertar
#     data = {
#         'user': user,
#         'result_path': resultado_path,
#         'results': json.dumps(result),
#         'created_at': datetime.now()
#     }

#     # Inserta los datos en la tabla 'analyses' (cambia esto por tu nombre de tabla)
#     response = supabase.table('analyses').insert(data).execute()

#     if response.status_code == 201:
#         print("Resultados guardados correctamente en Supabase.")
#     else:
#         print("Error al guardar en Supabase:", response.data)
