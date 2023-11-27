import os
import subprocess
import io
from pathlib import Path
import select
from shutil import rmtree
import subprocess as sp
import sys
from typing import Dict, Tuple, Optional, IO
from pyannote.audio import Pipeline
import torch
import shutil

from pydub import AudioSegment
from pydub.silence import split_on_silence


def clean(local, file_path, project_name, acapella, token, single_speaker):
    project_dir = os.getcwd() + "/" + project_name + "/"
    if local == True:
        ext = file_path.split(".")[-1]
    else:
        ext = "mp3"
    
    print(f"Project Folder: {project_dir}; ext: {ext}")
    
    setup_project(local, file_path, project_name)
    separate(inp = project_dir + "input", outp = project_dir + "output")
    
    if single_speaker:
        if acapella == True:
            print(f"Isolated vocals and file saved at {project_dir}{project_name}/output/htdemucs/file/")
        else:
            remove_silences(project_dir, ext)
            print(f"Separated vocals, removed silences and saved file at {project_dir}{project_name}/output/htdemucs/file/")
    else:
        if acapella == False:
            diarize_dataset(token, project_dir, ext, acapella = False, silences = True)
            print(f"Separated speakers, vocals, removed silences and saved file at {project_dir}{project_name}/output/htdemucs/file/")
        else:
            diarize_dataset(token, project_dir, ext, acapella = True, silences = False)
            print(f"Separated speakers, vocals and saved file at {project_dir}{project_name}/output/htdemucs/file/")

def diarize_dataset(token, project_dir, ext, acapella, silences):
    if silences == True:
        remove_silences(project_dir, ext)
        file_path = f"{project_dir}output/htdemucs/file/silences_removed.{ext}"
    else:
        file_path = f"{project_dir}output/htdemucs/file/vocals.{ext}"

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0", use_auth_token=token)

    pipeline.to(torch.device("cuda"))
    #diarization = pipeline(file_path, embedding_exclude_overlap=True)
    diarization = pipeline(file_path)
    audio = AudioSegment.from_mp3(file_path)

    speakers = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speakers.append(speaker)

    speakers = list(set(speakers))

    buffer = {}
    for s in speakers:
        buffer[s] = AudioSegment.empty()


    list(set(speakers))
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        
        start = int(turn.start * 1000)
        end = int(turn.end * 1000)
        diff = end - start
        
        if acapella == False:
            speaker_audio = audio[start:end]
            buffer[speaker] += speaker_audio
        else:
            blank = AudioSegment.silent(diff)
            for iter in list(set(speakers)):
                if iter == speaker:
                    speaker_audio = audio[start:end]
                    buffer[speaker] += speaker_audio
                else:
                    buffer[iter] += blank

    for s in speakers:
        buffer[s].export(project_dir + "output/htdemucs/file/" + s + "." + ext)

    return speakers


def remove_silences(project_dir, ext):

    file_path = project_dir + "/output/htdemucs/file/vocals." + ext
    file_name = "silences_removed.mp3"
    audio_format = "mp3"
    sound = AudioSegment.from_file(file_path, format = audio_format)
    audio_chunks = split_on_silence(sound
                                ,min_silence_len = 100
                                ,silence_thresh = -45
                                ,keep_silence = 50
                            )

    combined = AudioSegment.empty()
    for chunk in audio_chunks:
        combined += chunk
    combined.export(f'{project_dir}output/htdemucs/file/{file_name}', format = audio_format)

def setup_project(local, file_path, project_name):
    
    pwd = os.getcwd()
    subprocess.run(f"mkdir {pwd}/{project_name}", shell = True)
    subprocess.run(f"mkdir {pwd}/{project_name}/input", shell = True)
    subprocess.run(f"mkdir {pwd}/{project_name}/output", shell = True)
    print(f"Created the project directory at {pwd}/{project_name}")
    
    if local:
        ext = file_path.split(".")[-1]
        shutil.copy(file_path, f"{pwd}/{project_name}/input/file.{ext}")
        print("Copied files from the given path to the working directory")
    else:
        out_dir = f"{pwd}/{project_name}/input/file.mp3"
        subprocess.run(f"yt-dlp -x --audio-format mp3 -o {out_dir} {file_path}", shell = True)
        print("Downloaded the YouTube video and saved it in the project directory")


def find_files(in_path):
    out = []
    for file in Path(in_path).iterdir():
        if file.suffix.lower().lstrip(".") in ["mp3", "wav", "ogg", "flac"]:
            out.append(file)
    return out

def copy_process_streams(process: sp.Popen):
    def raw(stream: Optional[IO[bytes]]) -> IO[bytes]:
        assert stream is not None
        if isinstance(stream, io.BufferedIOBase):
            stream = stream.raw
        return stream

    p_stdout, p_stderr = raw(process.stdout), raw(process.stderr)
    stream_by_fd: Dict[int, Tuple[IO[bytes], io.StringIO, IO[str]]] = {
        p_stdout.fileno(): (p_stdout, sys.stdout),
        p_stderr.fileno(): (p_stderr, sys.stderr),
    }
    fds = list(stream_by_fd.keys())

    while fds:
        ready, _, _ = select.select(fds, [], [])
        for fd in ready:
            p_stream, std = stream_by_fd[fd]
            raw_buf = p_stream.read(2 ** 16)
            if not raw_buf:
                fds.remove(fd)
                continue
            buf = raw_buf.decode()
            std.write(buf)
            std.flush()

def separate(inp=None, outp=None):
    inp = inp or in_path
    outp = outp or out_path
    cmd = ["python3", "-m", "demucs.separate", "-o", str(outp), "-n", "htdemucs"]
    cmd += ["--mp3", "--mp3-bitrate=320"]
    cmd += [f"--two-stems=vocals"]

    files = [str(f) for f in find_files(inp)]
    if not files:
        print(f"No valid audio files in {in_path}")
        return
    p = sp.Popen(cmd + files, stdout=sp.PIPE, stderr=sp.PIPE)
    copy_process_streams(p)
    p.wait()
    if p.returncode != 0:
        print("Command failed, something went wrong.")
