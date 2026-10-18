from moviepy import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
from typing import List, Dict, Any
import os

def cut_and_caption(video_path: str, clip: Dict[str, Any], output_path: str, add_captions: bool = True, vertical: bool = True) -> str:
    video = VideoFileClip(video_path)
    subclip = video.subclip(clip['start'], clip['end'])
    
    if vertical:
        w, h = subclip.size
        target_w = h * 9 / 16
        if target_w < w:
            x1 = (w - target_w) / 2
            x2 = w - (w - target_w) / 2
            subclip = subclip.crop(x1=x1, y1=0, x2=x2, y2=h)
        else:
            target_h = w * 16 / 9
            y1 = (h - target_h) / 2
            y2 = h - (h - target_h) / 2
            subclip = subclip.crop(x1=0, y1=y1, x2=w, y2=y2)
    
    if add_captions:
        txt = TextClip(clip.get('hook', ''), fontsize=40, color='white', bg_color='rgba(0,0,0,0.6)', size=subclip.size)
        txt = txt.set_position(('center', 'bottom')).set_duration(subclip.duration)
        subclip = CompositeVideoClip([subclip, txt])
    
    subclip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=30)
    video.close()
    return output_path
