
function copyTextById(id){
  const el = document.getElementById(id);
  if(!el) return;
  const text = (el.innerText || el.textContent || '').trim();
  if(!text) return;
  navigator.clipboard.writeText(text).then(()=>{
    try { alert('Copied!'); } catch(e) {}
  });
}

// No client-side conversion; server will send original to OpenAI Whisper when enabled.
document.addEventListener('DOMContentLoaded', ()=>{});
