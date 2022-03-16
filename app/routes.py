from app import app
from flask import render_template, request, send_file
from .parser import get_seminars, html_to_png, html_to_pdf, Seminar
import base64

@app.route("/", methods=['post', 'get'])
def main():
    if request.method == 'POST':
        week_forward = request.form.get('week_forward', default=0, type=int)
        friday_name = request.form.get('fr_name', default=None, type=str)
        friday_photo = request.files.get('fr_photo', default=None)
        a = friday_photo.read()
        if len(a) != 0:
            friday_photo = f"data:{friday_photo.content_type};base64,{base64.b64encode(a).decode('utf-8')}"
        else:
            friday_photo = None
        friday_seminar = Seminar(friday_name, photo_src=friday_photo)
    else:
        week_forward = 0
        friday_seminar = Seminar()
    return render_template('editor.html', seminars=get_seminars(week_forward), friday_seminar=friday_seminar)


@app.route("/html")
def get_html():
    week_forward = request.args.get('week_forward', default=0, type=int)
    friday_name = request.args.get('fr_name', default=None, type=str)
    friday_photo = request.args.get('fr_photo', default=None, type=str)
    friday_seminar = Seminar(friday_name, photo_src=friday_photo)

    return render_template('table.html', seminars=get_seminars(week_forward), friday_seminar=friday_seminar)


@app.route("/png")
def get_png():
    week_forward = request.args.get('week_forward', default=0, type=int)
    friday_name = request.args.get('fr_name', default=None, type=str)
    friday_photo = request.args.get('fr_photo', default=None, type=str)
    friday_seminar = Seminar(friday_name, photo_src=friday_photo)

    html = render_template('table.html', seminars=get_seminars(week_forward), friday_seminar=friday_seminar)
    return send_file(html_to_png(html), attachment_filename='python.png')


@app.route("/pdf")
def get_pdf():
    week_forward = request.args.get('week_forward', default=0, type=int)
    friday_name = request.args.get('fr_name', default=None, type=str)
    friday_photo = request.args.get('fr_photo', default=None, type=str)
    friday_seminar = Seminar(friday_name, photo_src=friday_photo)

    html = render_template('table.html', seminars=get_seminars(week_forward), friday_seminar=friday_seminar)
    return send_file(html_to_pdf(html), attachment_filename='python.pdf')
