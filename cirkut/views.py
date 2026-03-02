from django.http import HttpResponse

def index(request):
    html = """
    <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cirkut - Connecting the world . In your Circle</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: #0d0d0d;
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .container {
    text-align: center;
    max-width: 520px;
    width: 100%;
  }

  .status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
  }

  .status {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #22c55e;
    margin-bottom: 2.5rem;
  }

  h1 {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #fff;
    margin-bottom: 0.5rem;
  }

  .tagline {
    font-size: 0.875rem;
    color: #666;
    font-weight: 300;
    margin-bottom: 2.5rem;
  }

  .footer-note {
    font-size: 0.75rem;
    color: #444;
  }
  .footer-note a { color: #555; text-decoration: none; }
  .footer-note a:hover { color: #22c55e; }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
</style>
</head>
<body>

<div class="container">

  <div class="status">
    <span class="status-dot"></span>All systems operational
  </div>

  <h1>Cirkut</h1>
  <p class="tagline">Connecting the world . In your Circle</p>

  
  <p class="footer-note">
    For full documentation visit <a href="#">docs.yourdomain.com</a>
  </p>

</div>

<script>
  function copyUrl() {
    const url = document.getElementById('baseUrl').textContent;
    navigator.clipboard.writeText(url).then(() => {
      const btn = document.querySelector('.copy-btn');
      btn.textContent = 'Copied!';
      btn.style.color = '#22c55e';
      btn.style.borderColor = '#22c55e';
      setTimeout(() => {
        btn.textContent = 'Copy';
        btn.style.color = '';
        btn.style.borderColor = '';
      }, 2000);
    });
  }
</script>

</body>
</html>

    """
    return HttpResponse(html)