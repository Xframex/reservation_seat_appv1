from flask import Flask, render_template, request, jsonify, send_file
from flask_bootstrap import Bootstrap
import datetime
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

total_seats = 20
seats = {str(i): None for i in range(1, total_seats + 1)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve-seat', methods=['GET', 'POST'])
def reserve_seat():
    if request.method == 'POST':
        name = request.form.get('name')
        seat_number = request.form.get('seatNumber')

        if seat_number.isdigit() and 1 <= int(seat_number) <= total_seats:
            seat_number = int(seat_number)
            if seats[str(seat_number)] is None:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                seats[str(seat_number)] = {'name': name, 'time': current_time}
                return jsonify({'success': True, 'message': f'Seat {seat_number} has been reserved for {name}.'}), 200
            else:
                return jsonify({'success': False, 'error': 'Seat is already reserved.'}), 400
        else:
            return jsonify({'success': False, 'error': 'Invalid seat number.'}), 400
    return render_template('reserve_seat.html', total_seats=total_seats)

@app.route('/cancel-reservation/<seat_number>', methods=['POST'])
def cancel_reservation(seat_number):
    if seat_number.isdigit() and 1 <= int(seat_number) <= total_seats:
        if seats[str(seat_number)]:
            seats[str(seat_number)] = None
            return jsonify({'success': True, 'message': f'Reservation for seat {seat_number} has been canceled.'}), 200
        else:
            return jsonify({'success': False, 'error': 'No reservation found for this seat.'}), 400
    else:
        return jsonify({'success': False, 'error': 'Invalid seat number.'}), 400

@app.route('/download-ticket/<seat_number>')
def download_ticket(seat_number):
    reservation = seats.get(seat_number)
    if reservation:
        name = reservation['name']
        time_stamp = reservation['time']
        ticket_data = f"Name: {name}, Seat Number: {seat_number}, Time: {time_stamp}\n Bon Voyage\n"
        filename = f'ticket_{seat_number}.txt'
        with open(filename, 'w') as file:
            file.write(ticket_data)
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'success': False, 'error': 'Seat is not reserved.'}), 400

@app.route('/about-us')  # New route for about us
def about_us():
    return render_template('about_us.html')

if __name__ == '__main__':
    app.run(debug=True)

