from flask import Flask, render_template, request
from forms import BuildingForm

app = Flask(__name__)
app.secret_key = 'development key'

@app.route('/')
def index():
    form = BuildingForm()
    return render_template('index.html', form=form)

@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    form = BuildingForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('index.html', form=form)
        else:
            return render_template('prediction.html', form=form)


if __name__  ==  '__main__':
    app.run()