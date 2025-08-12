from flask import Flask, render_template, request
from pymongo import MongoClient
import re
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb+srv://iago:PDJnyuuWFhQjm250@cluster0.8gjkuug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["Price-checker"]
collection = db["Pcs"]

@app.route('/', methods=['GET', 'POST'])
def index():
    pc_names = collection.distinct("name")  # get all PC names for dropdown
    selected_pc = None
    pc_data = []
    img_data = None  # initialize img_data for template

    if request.method == 'POST':
        selected_pc = request.form.get('pc_name')
        if selected_pc:
            # Query MongoDB for that PC's data (case-insensitive exact match)
            pc_data = list(collection.find({"name": re.compile(f"^{re.escape(selected_pc)}$", re.IGNORECASE)}))

            if pc_data:
                # Extract dates and prices, sorting by date ascending
                dates = [doc['date'] for doc in pc_data]
                prices = [doc['price'] for doc in pc_data]

                # If dates are stored as strings, convert to datetime objects
                if isinstance(dates[0], str):
                    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

                # Sort data by date
                combined = sorted(zip(dates, prices))
                dates_sorted, prices_sorted = zip(*combined)

                # Plot the price history
                plt.figure(figsize=(10,5))
                plt.plot(dates_sorted, prices_sorted, marker='o')
                plt.title(f"Price History for {selected_pc}")
                plt.xlabel("Date")
                plt.ylabel("Price (R$)")
                plt.grid(True)

                # Save plot to PNG image in memory
                img = io.BytesIO()
                plt.savefig(img, format='png')
                plt.close()
                img.seek(0)

                # Encode PNG image to base64 string
                img_data = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', pc_names=pc_names, selected_pc=selected_pc, pc_data=pc_data, img_data=img_data)

if __name__ == '__main__':
    app.run(debug=True)
