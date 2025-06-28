document.addEventListener("DOMContentLoaded", function () {
    // Form elements
    const form = document.getElementById("youtube-form");
    const videoUrlInput = document.getElementById("video-url");
    const summaryLengthInput = document.getElementById("summary-length");
    const lengthButtons = document.querySelectorAll(".length-btn");
    
    // New: Summary Type buttons and hidden input
    const summaryTypeButtons = document.querySelectorAll(".summary-type-btn");
    const summaryTypeInput = document.getElementById("summary-type");
  
    // Results elements
    const loadingSpinner = document.getElementById("loading");
    const resultsContainer = document.getElementById("results");
    const summaryContent = document.getElementById("summary-content");
    const transcriptContent = document.getElementById("transcript-content");
  
    // Tab elements
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");
  
    // Format buttons
    const summaryFormatButtons = document.querySelectorAll(".summary-format-btn");
    const transcriptFormatButtons = document.querySelectorAll(".transcript-format-btn");
  
    // Download buttons
    const downloadSummaryBtn = document.getElementById("download-summary");
    const downloadTranscriptBtn = document.getElementById("download-transcript");
  
    // Ensure default values are set:
    // Default for summary length ("medium")
    const mediumButton = document.querySelector('.length-btn[data-length="medium"]');
    if (mediumButton) {
      mediumButton.classList.add("active");
      summaryLengthInput.value = "medium";
    }
    // Default for summary type ("paragraph")
    const defaultSummaryType = document.querySelector('.summary-type-btn[data-type="paragraph"]');
    if (defaultSummaryType) {
      defaultSummaryType.classList.add("active");
      summaryTypeInput.value = "paragraph";
    }
    
    // Handle length button clicks
    lengthButtons.forEach((button) => {
      button.addEventListener("click", function () {
        lengthButtons.forEach((btn) => btn.classList.remove("active"));
        this.classList.add("active");
        summaryLengthInput.value = this.dataset.length;
      });
    });
    
    // Handle summary type button clicks
    summaryTypeButtons.forEach((button) => {
      button.addEventListener("click", function () {
        summaryTypeButtons.forEach((btn) => btn.classList.remove("active"));
        this.classList.add("active");
        summaryTypeInput.value = this.dataset.type;
      });
    });
  
    // Handle summary format button clicks
    summaryFormatButtons.forEach((button) => {
      button.addEventListener("click", function () {
        summaryFormatButtons.forEach((btn) => btn.classList.remove("active"));
        this.classList.add("active");
      });
    });
  
    // Handle transcript format button clicks
    transcriptFormatButtons.forEach((button) => {
      button.addEventListener("click", function () {
        transcriptFormatButtons.forEach((btn) => btn.classList.remove("active"));
        this.classList.add("active");
      });
    });
  
    // Handle tab switching
    tabButtons.forEach((button) => {
      button.addEventListener("click", function () {
        const tabId = this.dataset.tab;
        tabButtons.forEach((btn) => btn.classList.remove("active"));
        this.classList.add("active");
        tabPanes.forEach((pane) => {
          pane.classList.remove("active");
          if (pane.id === tabId) {
            pane.classList.add("active");
          }
        });
      });
    });
  
    // Handle form submission for processing the video
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      // Show loading spinner and hide results
      loadingSpinner.style.display = "flex";
      resultsContainer.style.display = "none";
  
      const formData = new FormData(form);
      fetch("/process", {
        method: "POST",
        body: formData
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            throw new Error(data.error);
          }
          summaryContent.textContent = data.summary;
          transcriptContent.textContent = data.transcript;
          loadingSpinner.style.display = "none";
          resultsContainer.style.display = "flex";
          // Activate summary tab by default
          document.querySelector('[data-tab="summary-tab"]').click();
        })
        .catch((error) => {
          alert("Error: " + error.message);
          loadingSpinner.style.display = "none";
        });
    });
  
    // Handle download summary
    downloadSummaryBtn.addEventListener("click", function () {
      const activeFormatBtn = document.querySelector(".summary-format-btn.active");
      const format = activeFormatBtn ? activeFormatBtn.dataset.format : "text";
      downloadContent(summaryContent.textContent, format, "summary");
    });
  
    // Handle download transcript
    downloadTranscriptBtn.addEventListener("click", function () {
      const activeFormatBtn = document.querySelector(".transcript-format-btn.active");
      const format = activeFormatBtn ? activeFormatBtn.dataset.format : "text";
      downloadContent(transcriptContent.textContent, format, "transcript");
    });
  
    // Function to download content
    function downloadContent(content, format, contentType) {
      if (!content) {
        alert("No content to download");
        return;
      }
      const formData = new FormData();
      formData.append("content", content);
      formData.append("format", format);
      formData.append("content_type", contentType);
  
      fetch("/download", {
        method: "POST",
        body: formData
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Download failed");
          }
          return response.blob();
        })
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.style.display = "none";
          a.href = url;
          let extension = ".txt";
          if (format === "markdown") extension = ".md";
          if (format === "json") extension = ".json";
          a.download = contentType + extension;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        })
        .catch((error) => {
          alert("Error: " + error.message);
        });
    }
  });
  
