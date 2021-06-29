import sys
from os import path, scandir

from flask import Blueprint, render_template, abort, request, redirect, flash, current_app, send_from_directory
from flask.helpers import send_from_directory
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename


front = Blueprint('front', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'txt', 'json', 'md', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def search_files(dir) -> list:
    scope_list = scandir(dir)
    filepaths = []
    filepaths_sub = []
    for f in scope_list:
        if f.is_dir():
            filepaths_sub = search_files(f)
        else:
            newf = f.path.replace('\\', '/')
            newf = newf.lstrip('/download')
            filepaths.append(newf)

    return filepaths + filepaths_sub


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
        new_flie_list = []
        print(f'File result : {myfiles}', file=sys.stderr)
        for f in myfiles:
            if f.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                new_flie_list.append(filename)
                f.save(path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return render_template('file.html', myval=new_flie_list)
    elif request.method == 'GET':
        return render_template('upload.html')

@front.route('/download')
@front.route('/download/<path:filename>')
def download_file(filename=None):
    if filename is not None:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        filepaths = search_files('download')
        file_tuple = []
        for f in filepaths:
            if "/" in f:
                file_tuple.append((f, f.rsplit("/", 1)[1]))
            else:
                file_tuple.append((f, f))
        return render_template('file.html', paths=file_tuple)



@front.route('/cdn/<path:filename>')
def ftp_static(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)