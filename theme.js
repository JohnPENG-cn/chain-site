(function(){var t=localStorage.getItem('t');if(t)document.documentElement.dataset.t=t})();
function toggleTheme(){var d=document.documentElement,cur=d.dataset.t||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');d.dataset.t=cur=='dark'?'light':'dark';localStorage.setItem('t',d.dataset.t);if(window.redraw)redraw()}
function isDark(){var t=document.documentElement.dataset.t;return t?t=='dark':matchMedia('(prefers-color-scheme: dark)').matches}
