import { useState } from 'react'
import { Scissors, Sparkles } from 'lucide-react'
import axios from 'axios'

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [clips, setClips] = useState([])
  const [options, setOptions] = useState({
    maxClips: 5,
    autoCaptions: true,
    vertical9x16: true
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim()) return
    setLoading(true)
    try {
      const res = await axios.post('http://localhost:8000/api/clips', {
        url,
        max_clips: options.maxClips,
        auto_captions: options.autoCaptions,
        vertical_9x16: options.vertical9x16
      })
      setClips(res.data.clips || [])
    } catch (err) {
      console.error(err)
      alert('Error generating clips')
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Scissors className="w-10 h-10 text-purple-400" />
            <h1 className="text-5xl font-bold text-white">Reka Clipper</h1>
            <Sparkles className="w-10 h-10 text-purple-400" />
          </div>
          <p className="text-xl text-gray-300">AI-powered YouTube clip generator</p>
          <p className="text-sm text-gray-400 mt-2">MiroFish-inspired virality scoring</p>
        </div>

        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 mb-8">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste a YouTube URL..."
            className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <div className="mt-4 flex flex-wrap gap-6 text-gray-300">
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={options.autoCaptions} onChange={(e) => setOptions({...options, autoCaptions: e.target.checked})} />
              Auto captions
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" checked={options.vertical9x16} onChange={(e) => setOptions({...options, vertical9x16: e.target.checked})} />
              9:16 vertical crop
            </label>
            <label className="flex items-center gap-3">
              Max clips
              <input type="range" min="1" max="10" value={options.maxClips} onChange={(e) => setOptions({...options, maxClips: parseInt(e.target.value)})} className="w-32" />
              <span>{options.maxClips}</span>
            </label>
          </div>
          <button type="submit" disabled={loading} className="mt-4 w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 disabled:opacity-50">
            {loading ? 'Generating clips...' : 'Generate Best Clips'}
          </button>
        </form>

        {clips.length > 0 && (
          <div className="max-w-4xl mx-auto grid gap-4">
            {clips.map((clip, idx) => (
              <div key={idx} className="bg-white/10 backdrop-blur-lg rounded-xl p-5 border border-white/20 text-white">
                <h3 className="text-lg font-semibold">{clip.title}</h3>
                <p className="text-sm text-gray-300 mt-1">{clip.hook}</p>
                <div className="flex gap-4 text-xs text-gray-400 mt-2">
                  <span>{clip.start.toFixed(1)}s - {clip.end.toFixed(1)}s</span>
                  <span>Virality: {clip.virality_score}/100</span>
                  <span>MiroFish: {(clip.score||0).toFixed(2)}</span>
                  <span>{clip.category}</span>
                </div>
                <p className="text-sm text-gray-300 mt-2">{clip.rationale}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
