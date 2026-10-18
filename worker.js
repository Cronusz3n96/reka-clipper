export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    if (url.pathname.startsWith('/api/')) {
      return new Response(JSON.stringify({
        message: 'Backend API needs to be deployed separately.',
        instructions: 'Deploy backend to Render/Railway/Fly, then update frontend to call that URL.',
        current_frontend: 'https://reka-clipper.merrittjake65.workers.dev'
      }), {
        status: 501,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
      });
    }
    
    return env.ASSETS.fetch(request);
  }
};
