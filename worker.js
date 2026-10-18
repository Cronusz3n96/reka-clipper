export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // API routes - for now, return a message that backend needs to be deployed separately
    if (url.pathname.startsWith('/api/')) {
      return new Response(JSON.stringify({
        message: 'Backend API needs to be deployed separately. Run backend on a service with more resources or use Ollama API endpoint.',
        note: 'This is a static frontend deploy. Configure OLLAMA_BASE_URL to point to a hosted Ollama instance.'
      }), {
        status: 501,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }
    
    // Serve static assets
    return env.ASSETS.fetch(request);
  }
};
