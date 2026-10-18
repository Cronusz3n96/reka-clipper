import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Try to proxy API requests to local backend if running
    if (url.pathname.startsWith('/api/')) {
      try {
        const backendUrl = new URL(url.pathname + url.search, 'http://localhost:8000');
        const res = await fetch(backendUrl, {
          method: request.method,
          headers: request.headers,
          body: request.body,
          duplex: 'half'
        });
        return res;
      } catch (e) {
        return new Response(JSON.stringify({
          error: 'Backend not available in this environment. Backend must be deployed separately.',
          detail: e.message
        }), { status: 503, headers: { 'Content-Type': 'application/json' } });
      }
    }
    return env.ASSETS.fetch(request);
  }
};
