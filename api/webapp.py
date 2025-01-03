from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import razorpay
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):  
    ID = db.Column(db.Integer, primary_key=True) 
    Station_Name = db.Column(db.String(500), nullable=False)
    Line = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Station {self.Station_Name}, Line {self.Line}>"


@app.route("/")
def main():
    
    stations = Data.query.all()
    return render_template("index1.html", stations=stations)

@app.route("/cost", methods=["POST", "GET"])
def cost_cal():
    if request.method == "POST":
        selected_source = request.form.get('source')
        selected_destination = request.form.get('destination')

        source_station = Data.query.filter_by(Station_Name=selected_source).first()
        destination_station = Data.query.filter_by(Station_Name=selected_destination).first()

        if source_station and destination_station:
            source_id = source_station.ID
            destination_id = destination_station.ID

            # Calculate the cost (for simplicity, the difference between IDs)
            cost = abs(destination_id - source_id)

            # Pass data to the HTML template
            return render_template("cost.html", 
                                   selected_source=selected_source, 
                                   selected_destination=selected_destination, 
                                   cost=cost)
        else:
            error_msg = "Source or Destination not found."
            return render_template("error.html", error_msg=error_msg)
    else:
        return "Invalid request method.", 405








razorpay_client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))

@app.route('/create-order', methods=['POST','GET'])
def create_order():
    data = {
        "amount": 50000,  # Amount in paise (₹500.00)
        "currency": "INR",
        "receipt": "order_rcptid_11",
    }
    try:
        order = razorpay_client.order.create(data)
        return jsonify(order)
    except Exception as e:
        return str(e)


# Run the app
if __name__ == "__main__":
    app.run()
