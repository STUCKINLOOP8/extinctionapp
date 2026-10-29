from flask import Flask, request

app = Flask(__name__)
data_store = []

@app.route('/add', methods=['POST'])
def add_data():
    data = request.json or {}
    # Evolved Code: Safe key check prevents server crash
    item = data.get('item', 'default_item')
    data_store.append(item)
    return "Data added successfully!", 200

if __name__ == '__main__':
    app.run(port=5000)
