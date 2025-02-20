from flask import Flask, render_template, request
import math

app = Flask(__name__)


def calculate_deq(D12, D23, D31):
    return (D12 * D23 * D31) ** (1 / 3)


def calculate_inductance(Deq, DS, d, length):
    DSL = math.sqrt(DS * d)
    L = 2e-7 * math.log(Deq / DSL) * 1000 * length
    return L


def calculate_capacitance(Deq, r, d, length):
    DSC = math.sqrt(r * d)
    epsilon_0 = 8.854e-12
    C = (2 * math.pi * epsilon_0) / math.log(Deq / DSC) * 1000 * length
    return C


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            D12 = float(request.form['D12'])
            D23 = float(request.form['D23'])
            D31 = float(request.form['D31'])
            DS = float(request.form['DS'])
            r = float(request.form['r'])
            d = float(request.form['d'])
            length = float(request.form['length'])

            Deq = calculate_deq(D12, D23, D31)
            L = calculate_inductance(Deq, DS, d, length)
            C = calculate_capacitance(Deq, r, d, length)

            return render_template('index.html', Deq=Deq, L=L, C=C)
        except ValueError:
            return render_template('index.html', error="Invalid input. Please enter numeric values.")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
