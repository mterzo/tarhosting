import os
import tarfile
from flask import Flask, request, flash, redirect
from flask import send_from_directory
import shutil
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object('tarhosting.config')
app.secret_key = app.config['SECRET_KEY']


@app.route("/")
def index():
   return 'hello world'


@app.route('/deploy/<path:name>', methods=['POST'])
def deploy(name):
    if request.method == 'POST':
    	# check if the post request has the file part
    	if 'file' not in request.files:
            flash('No file part')
            return redirect('/')

        file = request.files['file']
        if file and (file.filename.endswith('.tar.gz') or
                     file.filename.endswith('.tgz') or
                     file.filename.endswith('.tar')):
            filename = secure_filename(file.filename)
            out_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(out_file)
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


# not used by docker container
@app.route('/static/<path:filename>')
def send_from(filename):
    return "%s/%s" % (app.config['STATIC_DIR'], filename)
