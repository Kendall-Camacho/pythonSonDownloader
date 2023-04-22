import pytube
# pip install pytube
import os
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def song_list():
    song_list = []
    with open("SongList.txt", "r") as f:
        for line in f:
            song_list.append(line.strip())
    return song_list

def download_songs():
    ruta = "Ruta/Donde/Quieres/Guardar/Las/Canciones"
    for song in song_list():
        try:
            video = pytube.YouTube(song)
            audio = video.streams.filter(only_audio=True).first()
            if audio is None:
                raise ValueError("No se encontró una instancia de Stream para el audio")
            file_name = f"{video.title}.mp3"
            if os.path.isfile(os.path.join(ruta, file_name)):
                logging.warning(f"La canción {file_name} ya existe en la carpeta de destino. Se omitirá la descarga.")
                continue
            logging.info(f"Descargando la canción: {video.title}")
            audio.download(output_path=ruta, filename=file_name)
            logging.info(f"Descarga de la canción {video.title} completada")
        except Exception as e:
            logging.error(f"Error al descargar la canción {song}: {e}")

    # remove all the mp4 files
    for file in os.listdir(ruta):
        if file.endswith(".mp4") and file != "temp.mp4":
            os.remove(os.path.join(ruta, file))

if __name__ == "__main__":
    download_songs()