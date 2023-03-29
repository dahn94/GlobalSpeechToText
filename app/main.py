import subprocess
from app.funcoes import *
from fastapi import FastAPI, UploadFile
import glob
import os
import speech_recognition as sr
from pydub import AudioSegment

app = FastAPI()


@app.post("/speech-to-text/")
async def audio_file(file: UploadFile):
    full_transcription_str = ''

    extension: str = file.filename.split(".")[-1]
    if extension in ("wav", "mp3", "m4a"):
        split_time = 50000 # milisegundos
        # criar pasta para audios separados (se nao existir) 
        if not os.path.exists('audios_separados'):
            os.makedirs('audios_separados')

        # criar pasta audios (se nao existir)
        if not os.path.exists('audios'):
            os.makedirs('audios')

        # copiar arquivo para pasta audios
        with open(f'audios/{file.filename}', 'wb') as f:
            content = await file.read()
            f.write(content)      

        # Finds all audio files in the audios directory
        audio_files = glob.glob('audios/*.mp3')
        audio_files.extend(glob.glob('audios/*.wav'))
        audio_files.extend(glob.glob('audios/*.m4a'))
        convert_audio_to_flac(audio_files)
        flac_files = glob.glob('audios/*.flac')

        for flac_file in flac_files:
            try:
                name_file = flac_file.split('/')[-1].split('.')[0]
                audios_file_path_dict = split_audio_and_return_file_path(flac_file, split_time)
                full_transcription_str = transcribe_each_audio_files_on_recognize_google(audios_file_path_dict)
                remove_audios_separados()
                remove_audios_transcritos(name_file)     
            except Exception as e:
                print(f'Erro ao processar {flac_file}')
                print(e)
                with open('audios_que_nao_foram_convertidos_com_sucesso.txt', 'a') as f:
                    f.write(flac_file + '\n')
        # # retorne a transcrição vindo de dentro da pasta textos
        # result = subprocess.run(['cat', 'textos/{name_file}.txt'], stdout=subprocess.PIPE)
        # file_content = result.stdout.decode('utf-8')
        return {"transcription": f'{full_transcription_str}'}
    else:
        return {"error": "Invalid file type"}








