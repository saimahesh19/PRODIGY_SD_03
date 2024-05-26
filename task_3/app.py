from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Function to load contacts from a CSV file
def load_contacts(filename):
    contacts = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                contacts[row[0]] = [row[1], row[2]]
    except FileNotFoundError:
        pass
    return contacts

# Function to save contacts to a CSV file
def save_contacts(contacts, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for name, info in contacts.items():
            writer.writerow([name, info[0], info[1]])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = load_contacts("contacts.csv")
    return jsonify(contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    contacts = load_contacts("contacts.csv")
    contacts[data['name']] = [data['phone'], data['email']]
    save_contacts(contacts, "contacts.csv")
    return jsonify({"message": "Contact added successfully!"})

@app.route('/edit_contact', methods=['PUT'])
def edit_contact():
    data = request.get_json()
    contacts = load_contacts("contacts.csv")
    if data['name'] in contacts:
        contacts[data['name']] = [data['phone'], data['email']]
        save_contacts(contacts, "contacts.csv")
        return jsonify({"message": "Contact edited successfully!"})
    else:
        return jsonify({"error": "Contact not found."}), 404

@app.route('/delete_contact', methods=['DELETE'])
def delete_contact():
    data = request.get_json()
    contacts = load_contacts("contacts.csv")
    if data['name'] in contacts:
        del contacts[data['name']]
        save_contacts(contacts, "contacts.csv")
        return jsonify({"message": "Contact deleted successfully!"})
    else:
        return jsonify({"error": "Contact not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
