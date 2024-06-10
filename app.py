from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash
from pony.orm import db_session, commit, ObjectNotFound
from models import Volonter, VolonterskaAktivnost


app = Flask(__name__, template_folder="templates")
app.secret_key = 'tajni_kljuc'


def add_volontera(json_request):
    try:
        ime = json_request["ime"]
        prezime = json_request["prezime"]
        email_volontera = json_request["email_volontera"]
        kontakt_broj_volontera = json_request["kontakt_broj_volontera"]
        aktivnost_ime = json_request["aktivnost_ime"]

        with db_session:
            aktivnost = VolonterskaAktivnost.get(naziv_aktivnosti=aktivnost_ime)
            Volonter(ime=ime, prezime=prezime, email_volontera=email_volontera, kontakt_broj_volontera=kontakt_broj_volontera, aktivnost_id=aktivnost.aktivnost_id)
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def add_aktivnost(json_request):
    try:
        naziv_aktivnosti = json_request["naziv_aktivnosti"]
        opis_aktivnosti = json_request["opis_aktivnosti"]
        lokacija_aktivnosti = json_request["lokacija_aktivnosti"]
        datum_vrijeme_aktivnosti = json_request["datum_vrijeme_aktivnosti"]
        broj_volontera = json_request["broj_volontera"]

        with db_session:
            VolonterskaAktivnost(naziv_aktivnosti=naziv_aktivnosti, opis_aktivnosti=opis_aktivnosti, lokacija_aktivnosti=lokacija_aktivnosti, datum_vrijeme_aktivnosti=datum_vrijeme_aktivnosti, broj_volontera=broj_volontera)
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


def izbrisi_aktivnosti(aktivnost_id):
    try:
        with db_session:
            aktivnost = VolonterskaAktivnost[aktivnost_id]
            aktivnost.delete()
            response = {"response": "Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error": str(e)}


@app.route('/volonter/add', methods=['POST', 'GET'])
@db_session
def dodaj_volontera():
    aktivnost_ime = request.args.get('aktivnost_ime')

    if request.method == "POST":
            try:
                json_request = {}
                for key, value in request.form.items():
                    if value == "":
                        json_request[key] = None
                    else:
                        json_request[key] = value
                json_request['aktivnost_ime'] = aktivnost_ime
            except Exception as e:
                response = {"response": str(e)}
                return make_response(jsonify(response), 400)

            aktivnosti = [aktivnost.naziv_aktivnosti for aktivnost in VolonterskaAktivnost.select()]
            response = add_volontera(json_request)

            if response["response"] == "Success":
                return render_template('dodajv1.html', aktivnosti=aktivnosti, aktivnost_ime=aktivnost_ime), 200
            return make_response(jsonify(response), 400)
    else:
        aktivnosti = [aktivnost.naziv_aktivnosti for aktivnost in VolonterskaAktivnost.select()]
        return render_template('dodajv1.html', aktivnosti=aktivnosti, aktivnost_ime=aktivnost_ime), 200


@app.route('/volonteri', methods=['GET'])
@db_session
def prikazi_volontere_po_aktivnosti():
    aktivnosti = VolonterskaAktivnost.select()
    volonteri = []
    aktivnost = None
    if 'aktivnost_id' in request.args:
        aktivnost_id = request.args['aktivnost_id']
        aktivnost = VolonterskaAktivnost.get(aktivnost_id=int(aktivnost_id))
        if aktivnost:

            volonteri = aktivnost.volonter
            print("Volonteri:", volonteri)

    return render_template('prikaziv1.html', aktivnosti=aktivnosti, volonteri=volonteri, aktivnost=aktivnost)


@app.route('/volonter/update/<int:volonter_id>', methods=['POST', 'GET'])
@db_session
def izmjeni_volontera(volonter_id):
    try:
        volonter = Volonter.get(volonter_id=volonter_id)
        if not volonter:
            flash('Volonter nije pronađen', 'danger')
            return redirect(url_for('prikazi_volontere_po_aktivnosti'))

        if request.method == "POST":
            with db_session():
                volonter.ime = request.form['ime']
                volonter.prezime = request.form['prezime']
                volonter.email_volontera = request.form['email_volontera']
                volonter.kontakt_broj_volontera = request.form['kontakt_broj_volontera']
                commit()

            flash('Volonter uspješno ažuriran!', 'success')
            return redirect(url_for('prikazi_volontere_po_aktivnosti'))
        else:
            return render_template('urediv1.html', volonter=volonter)
    except Exception as e:
        db_session.rollback()
        flash(f'Došlo je do greške pri ažuriranju volontera: {str(e)}', 'danger')
        return redirect(url_for('prikazi_volontere_po_aktivnosti'))


@app.route('/volonter/delete/<int:volonter_id>', methods=['DELETE'])
@db_session
def obrisi_volontera(volonter_id):
    try:
        volonter = Volonter[volonter_id]
    except ObjectNotFound:
        return make_response(jsonify({'error': 'Volonter nije pronađen'}), 404)

    volonter.delete()
    commit()
    uspjesna_poruka = {"response": "Success"}
    return make_response(jsonify(uspjesna_poruka), 200)


@app.route('/', methods=["GET"])
def home():
    return make_response(render_template("index1.html"))


# ------------------------------------------------------------------------------ #

@app.route('/aktivnost/add', methods=['POST', 'GET'])
@db_session
def dodaj_aktivnost():
    if request.method == "POST":
            try:
                json_request = {}
                for key, value in request.form.items():
                    if value == "":
                        json_request[key] = None
                    else:
                        json_request[key] = value
            except Exception as e:
                response = {"response": str(e)}
                return make_response(jsonify(response), 400)

            response = add_aktivnost(json_request)

            if response["response"] == "Success":
                return render_template('dodaj1.html'), 200
            return make_response(jsonify(response), 400)
    else:
        return render_template('dodaj1.html'), 200


@app.route('/aktivnosti/popis', methods=['GET'])
@db_session
def prikazi_popis_aktivnosti():
    aktivnosti = VolonterskaAktivnost.select()
    if aktivnosti:
        return render_template('popis1.html', aktivnosti=aktivnosti)
    else:
        flash('Nema dostupnih aktivnosti.', 'info')
        return render_template('popis1.html', aktivnosti=[])


@app.route('/aktivnost/<int:aktivnost_id>', methods=['POST', 'GET'])
@db_session
def izmjeni_aktivnost(aktivnost_id):
    try:
        aktivnost = VolonterskaAktivnost.get(aktivnost_id=aktivnost_id)
        if not aktivnost:
            flash('Aktivnost nije pronađena', 'danger')
            return redirect(url_for('prikazi_popis_aktivnosti'))

        if request.method == "POST":
            with db_session():
                aktivnost.naziv_aktivnosti = request.form['naziv_aktivnosti']
                aktivnost.opis_aktivnosti = request.form['opis_aktivnosti']
                aktivnost.lokacija_aktivnosti = request.form['lokacija_aktivnosti']
                aktivnost.datum_vrijeme_aktivnosti = request.form['datum_vrijeme_aktivnosti']
                aktivnost.broj_volontera = request.form['broj_volontera']

            flash('Aktivnost uspješno ažurirana!', 'success')
            return redirect(url_for('prikazi_popis_aktivnosti'))
        else:
            return render_template('uredi1.html', aktivnost=aktivnost)  # Dodajte return ovdje
    except Exception as e:
        db_session.rollback()
        flash(f'Došlo je do greške pri ažuriranju aktivnosti: {str(e)}', 'danger')
        return redirect(url_for('prikazi_popis_aktivnosti'))


@app.route('/aktivnost/<int:aktivnost_id>', methods=['DELETE', 'GET'])
@db_session
def obrisi_aktivnost(aktivnost_id):
    if request.method == 'DELETE':
        try:
            with db_session:
                aktivnost = VolonterskaAktivnost[aktivnost_id]
                aktivnost.delete()
                return jsonify({"response": "Success"})
        except Exception as e:
            return jsonify(
                {"response": "Fail", "error": str(e)})
    else:
        return redirect(url_for('prikazi_popis_aktivnosti'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
