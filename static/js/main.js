// Function to toggle a section's visibility
function toggleSection(button) {
  const section = button.nextElementSibling;
  const icon = button.querySelector(".toggle-icon");
  const isExpanded = section.classList.contains("show");

  // Toggle visibility
  section.classList.toggle("show");
  icon.style.transform = isExpanded ? "rotate(0deg)" : "rotate(180deg)";

  // Update ARIA attributes
  button.setAttribute("aria-expanded", !isExpanded);
}

// Handle keyboard events
function handleKeyPress(event) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    toggleSection(event.target);
  }
}

// Initialize all sections on page load
document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".section-header");

  buttons.forEach((button) => {
    // Set up initial state (collapsed)
    const section = button.nextElementSibling;
    const icon = button.querySelector(".toggle-icon");

    section.classList.remove("show");
    button.setAttribute("aria-expanded", "false");
    icon.style.transform = "rotate(0deg)";
  });
});
