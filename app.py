from flask import Flask, request, jsonify
from procesos_web.obtener_folios_paperless import lista_series_folios, documentos
from procesos_web.codigos_series import series_codigos

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/test')
def test():
    return "This is a test endpoint!"

@app.route('/folios/')
def folios_base():
    base_url = request.base_url
    documentos = series_codigos.keys()
    urls = {doc: f"{base_url}{doc}" for doc in documentos}
    
    html_content = "<html><body><h1>Folios Disponibles segun Documento:</h1><ul>"
    for doc, url in urls.items():
        html_content += f'<li><a href="{url}">{doc.capitalize()}</a></li>'
    html_content += "</ul></body></html>"
    
    return html_content

@app.route('/folios/<tipo_documento>')
def folios(tipo_documento):
    if tipo_documento not in series_codigos.keys():
        return jsonify({"error": "Tipo de documento no válido"}), 400

    df = lista_series_folios(tipo_documento)
    #ultimo_folio = request.args.get('ultimo_folio', 'False').lower() == 'true'
    ultimo_folio = 'ultimo_folio' in request.args
    
    if ultimo_folio:
        # Obtener el valor de la columna "Folio Final" donde "Id" tiene el mayor valor
        ultimoFolio = int(df.loc[df['Id'].idxmax()]['Folio_Final'])
        return jsonify({'Folio_Final': ultimoFolio})
    else:
        # Devolver el DataFrame completo en forma de tabla HTML
        return df.to_html(index=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)