// Function to toggle the station list visibility
function toggleStations() {
  const content = document.querySelector(".station-content");
  const icon = document.querySelector(".toggle-icon");
  const header = document.querySelector(".station-header");
  const isExpanded = content.classList.contains("show");

  content.classList.toggle("show");
  icon.classList.toggle("rotated");

  // Update ARIA attributes
  header.setAttribute("aria-expanded", !isExpanded);
}

// Handle keyboard events
function handleKeyPress(event) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    toggleStations();
  }
}

// Initialize the station list on page load
document.addEventListener("DOMContentLoaded", function () {
  const content = document.querySelector(".station-content");
  const header = document.querySelector(".station-header");

  content.classList.add("show");
  header.setAttribute("aria-expanded", "true");
});
