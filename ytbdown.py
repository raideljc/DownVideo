import yt_dlp
import os
import threading
from yt_dlp.postprocessor import (
    FFmpegExtractAudioPP,
    FFmpegVideoConvertorPP)


class _NullLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass
        
quality_map = {
    'Solo Audio': 'bestaudio/best',
    '360p': 'bestvideo[height<=360]+bestaudio/best',
    '480p': 'bestvideo[height<=480]+bestaudio/best',
    '720p': 'bestvideo[height<=720]+bestaudio/best',
'1080p': 'bestvideo[height<=1080]+bestaudio/best',
    'Mayor Calidad': 'bestvideo+bestaudio/best',
}

quality_map = {
    'Solo Audio': 'bestaudio/best',
    '360p': 'bestvideo[height<=360]+bestaudio/best',
    '480p': 'bestvideo[height<=480][height>360]+bestaudio/best',
    '720p': 'bestvideo[height<=720][height>480]+bestaudio/best',
'1080p': 'bestvideo[height<=1080][height>720]+bestaudio/best',
    'Mayor Calidad': 'bestvideo+bestaudio/best',
}

def getvideoinfo(url):
     optdlp = {
         'quiet': True,
          'no_warnings': True,   
          'skip_download': True,
          'ignoreerrors': False,  
          'playlist_items': '1', 
          'noplaylist': True, 
           "logger": _NullLogger(),
          }
     with yt_dlp.YoutubeDL(optdlp) as ydl:
        video_info = ydl.extract_info(url, download=False)
        if 'entries' in video_info:
            return (video_info['entries'][0])
        else:
            return (video_info)

def human(n):
    if not n: return "??"
    for u in ['B', 'KB', 'MB', 'GB']:
        if n < 1024: return f"{n:.2f} {u}"
        n /= 1024
    return f"{n:.2f} TB"          


def getformatsizes(info):
    with yt_dlp.YoutubeDL({}) as ydl:   
        if not info : return {}         
        try:
            sizeold = 0
            formats = info.get('formats', None)
            if not formats: return { 'Mayor Calidad': 'bestvideo+bestaudio/best'}
            qualdict = {}
            for name, fmt in quality_map.items():
                f = next(ydl.build_format_selector(fmt)({'formats': formats, 'incomplete_formats': False}))
                if 'requested_formats' in f:
                    size = sum(x.get('filesize') or x.get('filesize_approx') or 0
                               for x in f['requested_formats']) or None
                else:
                    size = f.get('filesize', 0) or f.get('filesize_approx')
                size = size if size else 0
                if size >= sizeold:
                    sizeold = size 
                    qualdict[f"{name} {human(size)}"] = fmt 
            return qualdict            
        except Exception as e:
            return ( { 'Mayor Calidad': 'bestvideo+bestaudio/best'})

def getffmppath():
    ffmpgdir = None
    try:
        ffmpgdir = "ffmpg/"
        
    finally: 
        return ffmpgdir

def downloadvideo(url, path, format='bestvideo+bestaudio/best', subtitles=None, progress_callback=None,postprocessor_callback=None, proxy=None,     retries=10, bypass_country=None, showsms =None):
    optsytp = {
        "logger": _NullLogger(),
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
       # 'ffmpeg_location': ffmpg_dir,
        #'ignoreerrors': True, 
        'retries': retries,  
         'merge_output_format': 'mp4', 
         'paths': {
              'temp': path,
              'home': path,
              }, 
        'noplaylist': True,     
        'restrictfilenames': True,
        'windowsfilenames': True,
        'overwrites': True, 
        'proxy': proxy,       
        }
    if subtitles: 
        optsytp.update({
            'writesubtitles': True,    
            'writeautomaticsub': True,
            'subtitleslangs': [subtitles],
            'subtitlesformat': 'srt/best',
        })
    if subtitles: 
        optsytp.update({
            'geo_bypass': True,
            'geo_bypass_country': bypass_country,
        })
    if progress_callback: optsytp[ 'progress_hooks'] =  [progress_callback] 
    if postprocessor_callback: optsytp[ 'postprocessor_hooks'] =  [postprocessor_callback] 
    if format == 'bestaudio/best': 
        optsytp.update({
             'format': 'bestaudio/best',
              'postprocessors': [{
                       #'key': 'FFmpegExtractAudio' ,
                        'preferredcodec': 'm4a',
                        'preferredquality': '192',
                   }],
        })
    else: 
        optsytp['format']: format
    #if isinstance(parms, dict): optsytp.update(parms)
    thread = threading.Thread(
        target=download_threading,
        args=(url, optsytp, showsms),
        )
    thread.daemon = True
    thread.start() 
    return(thread)
    
def seg_to_time(seg):
    min, seg = divmod(seg, 60)
    h, min = divmod(min, 60)
    return     f"{int(h)}:{int(min)}:{int(seg)}"  

    
def download_threading (url, parms, showsms =None ):    
    try:
        with yt_dlp.YoutubeDL(parms) as ydl:
            #inf = getvideoinfo(url)
            ydl.download([url])    
        showsms("Descarga realizada con exito", "succes", url)
    except Exception as e:
        error_msg = str(e)
        showsms(f"Error al descargar el video.", "error",error_msg)
        

        

ffmpg_dir = getffmppath()                                                