from flask import Flask, render_template, redirect, url_for, request
from models import db, Complaint
from forms import ComplaintForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()




@app.route('/', methods=['GET', 'POST'])
def index():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(name=form.name.data, message=form.message.data)
        db.session.add(complaint)
        db.session.commit()
        return redirect(url_for('index'))
    complaints = Complaint.query.all()
    return render_template('index.html', form=form, complaints=complaints)

@app.route('/admin')
def admin():
    complaints = Complaint.query.all()
    total = Complaint.query.count()
    resolved = Complaint.query.filter_by(resolved=True).count()
    return render_template('admin.html', complaints=complaints, total=total, resolved=resolved)

@app.route('/resolve/<int:id>')
def resolve(id):
    complaint = Complaint.query.get_or_404(id)
    complaint.resolved = True
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete/<int:id>')
def delete(id):
    complaint = Complaint.query.get_or_404(id)
    db.session.delete(complaint)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
