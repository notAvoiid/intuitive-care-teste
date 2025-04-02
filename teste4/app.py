from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import unicodedata

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '../teste3/downloads/Relatorio_cadop.csv')

def normalize_text(text):
    """Remove acentos e caracteres especiais"""
    return unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('ASCII').lower()

try:
    df = pd.read_csv(
        CSV_PATH,
        sep=';',
        encoding='utf-8',
        dtype=str
    ).dropna(how='all').fillna('')
    
    if 'Nome_Fantasia' in df.columns:
        df['Nome_Fantasia_normalized'] = df['Nome_Fantasia'].apply(normalize_text)
except Exception as e:
    print(f"Erro ao carregar o arquivo CSV: {e}")
    df = pd.DataFrame()

@app.route('/search', methods=['GET'])
def search():
    query = normalize_text(request.args.get('q', ''))
    field = request.args.get('field', 'Nome_Fantasia')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    if page < 1: page = 1
    if limit < 1 or limit > 100: limit = 10
    offset = (page - 1) * limit

    if not query:
        filtered_df = df.copy()
    else:
        if field == 'Nome_Fantasia' and 'Nome_Fantasia_normalized' in df.columns:
            filtered_df = df[df['Nome_Fantasia_normalized'].str.contains(query)]
        else:
            filtered_df = df[df.apply(lambda row: query in normalize_text(str(row[field])), axis=1)] if field in df.columns else pd.DataFrame()

    total_items = len(filtered_df)
    total_pages = (total_items + limit - 1) // limit

    # Paginar mantendo a ordenação original
    paginated_df = filtered_df.iloc[offset:offset + limit]

    return jsonify({
        'results': paginated_df.drop(columns=['Nome_Fantasia_normalized'], errors='ignore').to_dict('records'),
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'total_items': total_items,
            'per_page': limit
        }
    })

if __name__ == '__main__':
    app.run(debug=True)