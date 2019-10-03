import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all')) # this will give you the URL /donations/ cuz all is the function with that extension

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/new', methods=['GET', 'POST'])
def new_d():
    if request.method == 'GET':
        return render_template('new_d.jinja2')

    if request.method == 'POST':
        donated_value = int(request.form['amount'])
        donor_name = request.form['name'].strip()

        try:
            donor = Donor.select().where(Donor.name == donor_name).get()
        except Donor.DoesNotExist as e:
            donor = Donor(name=donor_name)
            donor.save()

        donation_made = Donation(value=donated_value, donor=donor)
        donation_made.save()

        return render_template('new_d.jinja2')

    else:
        return home()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)

