from app.services.mirofish import mirofish_score_clip

def test_mirofish_score():
    clip = {
        'start': 0,
        'end': 30,
        'title': 'Why this matters',
        'hook': 'Why this matters',
        'virality_score': 80
    }
    score = mirofish_score_clip(clip, [])
    assert score > 0
