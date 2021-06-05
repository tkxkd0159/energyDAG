import sys
from os import path

from flask import Blueprint, render_template, abort, request, redirect, flash, current_app
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename


front = Blueprint('front', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'txt', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@front.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)


@front.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)


        myfiles = request.files.to_dict(flat=False)['file']
        # print(f'File result : {}', file=sys.stderr)
        for f in myfiles:
            if f.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return render_template('upload.html')
    elif request.method == 'GET':
        return render_template('upload.html')