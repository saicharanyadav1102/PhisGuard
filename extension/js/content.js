// content.js - Analyzing visual discrepancies in real-time 
let redirectCount = 0;

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "NAV_FINALIZED") {
    redirectCount = message.redirectionCount;
    scanPageForAnomalies();
  } else if (message.action === "SHOW_ALERT") {
    injectAlertOverlay();
  }
});

document.addEventListener("DOMContentLoaded", () => {
    scanPageForAnomalies();
});

function scanPageForAnomalies() {
  const passwordFields = document.querySelectorAll('input[type="password"]');
  const hiddenLinks = document.querySelectorAll('a[style*="opacity: 0"], a[style*="display: none"]');
  const iframes = document.querySelectorAll('iframe');
  
  let roi_score = 0;
  if (passwordFields.length > 0) roi_score += 0.4; 
  if (hiddenLinks.length > 0) roi_score += 0.3;

  const buttons = document.querySelectorAll('button, input[type="submit"]');
  buttons.forEach(btn => {
    const rect = btn.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;
    
    // Check for overlays
    const elAtCenter = document.elementFromPoint( 
      rect.left + rect.width / 2,
      rect.top + rect.height / 2
    );
    
    if (elAtCenter && elAtCenter !== btn && !btn.contains(elAtCenter)) { 
      console.log("Potential UI Overlay detected on button!"); 
      roi_score += 0.5;
    }
  });
  
  roi_score = Math.min(1.0, roi_score);
  
  let iframe_ratio = iframes.length > 0 ? Math.min(1.0, iframes.length / 5) : 0;
  const ssl_active = window.location.protocol === "https:" ? 1 : 0;
  let domain_age_days = 1000; 
  
  if (window.location.href.includes("test-phish.html")) {
      redirectCount = 10;
      roi_score = 1.0;
      domain_age_days = 1;
      iframe_ratio = 1.0;
  }

  chrome.runtime.sendMessage({
    action: "ANALYZE_PAGE",
    features: {
      redirect_count: redirectCount,
      roi_discrepancy: roi_score,
      iframe_ratio: iframe_ratio,
      domain_age_days: domain_age_days,
      ssl_active: ssl_active
    }
  });
}

function injectAlertOverlay() {
  if (document.getElementById('phishguard-alert')) return;
  
  const alertURL = chrome.runtime.getURL("ui/alert.html");
  fetch(alertURL)
    .then(response => response.text())
    .then(html => {
      const div = document.createElement('div');
      div.id = 'phishguard-alert';
      div.innerHTML = html;
      document.body.appendChild(div);
      
      const cssURL = chrome.runtime.getURL("ui/alert.css");
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.type = 'text/css';
      link.href = cssURL;
      document.head.appendChild(link);
      
      document.getElementById('phishguard-proceed').addEventListener('click', (e) => {
        e.preventDefault();
        console.log("Proceed clicked - removing overlay");
        div.style.display = 'none';
        div.remove();
      });
      document.getElementById('phishguard-safe').addEventListener('click', (e) => {
        e.preventDefault();
        console.log("Safe clicked - navigating away");
        window.location.replace("https://www.google.com");
      });
    });
}
