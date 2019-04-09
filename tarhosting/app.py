import os
import tarfile
from flask import Flask, request, flash, redirect, render_template
from flask import Blueprint
from flask_autoindex import AutoIndex
import shutil
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('tarhosting.config')
app.secret_key = app.config['SECRET_KEY']

auto_index = AutoIndex(app, browse_root=app.config['STATIC_DIR'],
                       add_url_rules=False)


@app.route("/")
def index():
    return render_template('index.html', URL=request.url)


@app.route('/browse')
@app.route('/browse/')
@app.route('/browse/<path:path>')
def autoindex(path='.'):
    return auto_index.render_autoindex(path)


@app.route('/deploy/<path:name>', methods=['POST'])
def deploy(name):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')

        upload_file = request.files['file']
        if upload_file and (upload_file.filename.endswith('.tar.gz') or
                            upload_file.filename.endswith('.tgz') or
                            upload_file.filename.endswith('.tar')):
            filename = secure_filename(upload_file.filename)
            out_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            upload_file.save(out_file)
            tar_dir = "%s/%s" % (app.config['STATIC_DIR'], name)
            tar = tarfile.open(out_file)
            root = tar.getnames()[0]
            if root.startswith('/') or root.startswith('../'):
                return "Tarball not rooted properly using '/' or '../'\n"
            shutil.rmtree('{}/{}'.format(tar_dir, root), ignore_errors=True)
            tar.extractall(path=tar_dir)
            tar.close()
            os.unlink(out_file)
        else:
            return "Wrong extention\n"
        return 'Upload complete\n'
    return "wrong method\n"


@app.route('/undeploy/<path:name>', methods=['GET'])
def undeploy(name):
    tar_dir = "%s/%s" % (app.config['STATIC_DIR'], name)
    shutil.rmtree(tar_dir, ignore_errors=True)
    return 'Done'
