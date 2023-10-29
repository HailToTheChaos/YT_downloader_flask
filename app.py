from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pytube import YouTube, exceptions
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración para servir archivos estáticos desde el directorio 'static'
app.static_folder = 'static'

DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        resolution = request.form['resolution-select']

        try:
            video = YouTube(youtube_url)
            # Selecciona la primera corriente de video disponible (la mejor calidad disponible)
            video_stream = video.streams.filter(res=resolution).first()
            # Descarga el video
            video_stream.download(DOWNLOAD_FOLDER)
            return redirect(url_for('download_file', filename=video_stream.default_filename))
        except exceptions.RegexMatchError:
            flash(f'Formato no válido', 'error')
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
            app.logger.error(str(e))
    return render_template('index.html')


@app.route('/download_mp3', methods=['POST'])
def download_mp3():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        try:
            video = YouTube(youtube_url)
            # Descarga el audio en formato MP3
            audio_stream = video.streams.filter(only_audio=True).first()
            audio_stream.download(DOWNLOAD_FOLDER, audio_stream.title+".mp3")

            flash('El audio se ha descargado con éxito.', 'success')
            return redirect(url_for('download_file', filename=audio_stream.default_filename))
        except exceptions.RegexMatchError:
            flash(f'Formato no válido', 'error')
        except Exception as e:
            flash(f'Ocurrió un error: {str(e)}', 'danger')
            app.logger.error(str(e))
    return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
