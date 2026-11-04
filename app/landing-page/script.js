// Scroll-triggered fade-in animations
// (A JavaScript comment starts with // and lasts until the end of the line.)
// IntersectionObserver is a browser feature that TELLS YOU when an element enters or leaves
// the screen, without you having to check on every scroll. "const observer" stores it in a
// constant named observer.
const observer = new IntersectionObserver(
  // The callback: a function (written as an arrow function "(...) => { ... }") that the browser
  // calls whenever watched elements cross the visibility threshold.
  // "entries" is a list of what changed.
  (entries) => {
    // Loop over each changed element.
    entries.forEach((entry) => {
      // "Is this element now on screen?"
      if (entry.isIntersecting) {
        // entry.target is the HTML element: add the class "visible", so the CSS animation plays.
        entry.target.classList.add('visible');
        // Stop watching it, so the animation happens only ONCE
        // (it won't fade out again when you scroll back up).
        observer.unobserve(entry.target);
      // Close the if, the loop and the callback.
      }
    });
  },
  // Options: trigger when 10% of the element is visible.
  { threshold: 0.1 }
);

// Find every element with the class fade-in ("." = class selector, like in CSS)
// and start watching each one.
document.querySelectorAll('.fade-in').forEach((el) => observer.observe(el));

// Navbar shadow on scroll
// Find the element with id="navbar" and keep it in a constant.
const navbar = document.getElementById('navbar');
// "Every time the window scrolls, run this function."
window.addEventListener('scroll', () => {
  // window.scrollY = how many pixels the page is scrolled down.
  // classList.toggle(name, condition) ADDS the class if the condition is true and REMOVES it if
  // false: more than 10px scrolled = shadow; back at the top = no shadow.
  navbar.classList.toggle('scrolled', window.scrollY > 10);
});
