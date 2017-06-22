import os
import tarfile
from flask import Flask, request, flash, redirect, render_template
from flask import Blueprint
from flask.ext.autoindex import AutoIndexBlueprint
import shutil
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('tarhosting.config')
app.secret_key = app.config['SECRET_KEY']

auto_bp = Blueprint('auto_bp', __name__)
AutoIndexBlueprint(auto_bp, browse_root=app.config['STATIC_DIR'])
app.register_blueprint(auto_bp, url_prefix='/browse')


@app.route("/")
def index():
    return render_template('index.html', URL=request.url)


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
            shutil.rmtree(tar_dir, ignore_errors=True)
            tar = tarfile.open(out_file)
            tar.extractall(path=tar_dir)
            tar.close()
            os.unlink(out_file)
        else:
            return "Wrong extention"
        return 'Upload complete'
    return "wrong method"


@app.route('/undeploy/<path:name>', methods=['GET'])
def undeploy(name):
    tar_dir = "%s/%s" % (app.config['STATIC_DIR'], name)
    shutil.rmtree(tar_dir, ignore_errors=True)
    return 'Done'
