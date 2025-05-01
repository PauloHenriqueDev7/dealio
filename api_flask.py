from flask import Flask, jsonify
from scraper import raspar_cuponomia

app = Flask(__name__)

@app.route('/')
def home():
    return "API de Cupons Online! Acesse /cupons para ver os descontos."

@app.route('/cupons')
def listar_cupons():
    cupons = raspar_cuponomia()
    return jsonify(cupons)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Força a porta 5080

@app.route('/cupons')
def listar_cupons():
    try:
        cupons = raspar_cuponomia()
        return jsonify({"status": "success", "data": cupons})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/cupons/<loja>')
def cupons_por_loja(loja):
    cupons = [c for c in raspar_cuponomia() if loja.lower() in c['loja'].lower()]
    return jsonify(cupons)       