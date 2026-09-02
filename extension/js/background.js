// background.js - Redirection and Navigation Monitoring 
let redirectionHistory = {};

chrome.webRequest.onBeforeRedirect.addListener(
  (details) => {
    let tabId = details.tabId;
    if (tabId < 0) return; // Ignore background requests
    
    if (!redirectionHistory[tabId]) { 
      redirectionHistory[tabId] = 0;
    }
    redirectionHistory[tabId]++;
    console.log(`Redirection detected for tab ${tabId}: ${details.redirectUrl}`);
  },
  { urls: ["<all_urls>"] }
);

chrome.webNavigation.onCompleted.addListener((details) => { 
  if (details.frameId === 0) { // Main frame load
    const count = redirectionHistory[details.tabId] || 0; 
    
    // Check if we can inject to tab
    chrome.tabs.sendMessage(details.tabId, {
      type: "NAV_FINALIZED",
      redirectionCount: count
    }, (response) => {
      // Ignore errors for uninjectable pages (chrome:// etc)
      if (chrome.runtime.lastError) {}
    });
    
    // Reset for next navigation 
    redirectionHistory[details.tabId] = 0;
  }
});

// Listen for analysis results from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "ANALYZE_PAGE") {
    // Send to backend
    fetch("http://127.0.0.1:5000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        request_id: crypto.randomUUID(),
        client_meta: { os: "windows", ver: "1.0.4" },
        features: [
          request.features.redirect_count,
          request.features.roi_discrepancy,
          request.features.iframe_ratio,
          request.features.domain_age_days,
          request.features.ssl_active
        ]
      })
    })
    .then(res => res.json())
    .then(data => {
      if (data.verdict === "phish") {
        chrome.tabs.sendMessage(sender.tab.id, { action: "SHOW_ALERT" });
      }
    })
    .catch(err => console.error("API Error:", err));
  }
});
