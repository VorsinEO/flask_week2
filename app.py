from flask import Flask, render_template
from data import title, subtitle, description, departures, tours
import random

app = Flask(__name__)

@app.route('/')
def main():
    random_dict = dict(random.sample(tours.items(), 6))
    output = render_template('index.html', tours = tours, title = title, subtitle = subtitle, description = description, departures = departures, r_tours=random_dict)
    return output

@app.route('/departures/<departure>/')
def get_departure(departure):
    #фильтрация туров по направлению
    f_tours={k:v for (k,v) in tours.items() if v['departure']==departure}
    # костыль, чтобы первый символ в названии направления перевести в нижний регистр как в образце - "из" вместо "Из"
    new_title = str(departures[departure][0]).lower()+str(departures[departure][1:])
    #формируем список цен для направления
    prices= (list({k:v["price"] for (k,v) in f_tours.items()}.values()))
    #формируем список количества ночей для направления
    nights= (list({k:v["nights"] for (k,v) in f_tours.items()}.values()))
    # костыль, чтобы сделать формат вывода стоимости как в образце "ЧЧ ЧЧЧ"
    min_price = str(min(prices))[:2]+' ' + str(min(prices))[2:]
    max_price = str(max(prices))[:2]+' ' + str(max(prices))[2:]
    output = render_template('departure.html', f_tours = f_tours, new_title=new_title, nights=nights, prices=prices, \
            min_price= min_price, max_price=max_price, title=title, departures=departures)
    return output

@app.route('/tours/<id>/')
def get_tour(id):
    #фильтр тура по id
    tour = tours.get(int(id))
    # костыль, чтобы сделать формат вывода стоимости как в образце "ЧЧ ЧЧЧ"
    price = str(tour["price"])[:2]+' ' + str(tour["price"])[2:]
    output =render_template('tour.html', tour = tour, departures=departures, price=price, title=title)
    return output

if __name__ == '__main__':
    app.run()