/**
 * Dark Fractal Pattern Generator
 * Based on dark-fractal-theme-spec.md
 * Renders recursive branching fractal patterns on canvas
 */

(function() {
  'use strict';

  let canvas, ctx;
  let animationId = null;

  // Initialize fractal pattern
  function initFractal() {
    // Only run in dark mode
    const theme = document.documentElement.getAttribute('data-theme');
    if (theme !== 'dark') {
      if (canvas) {
        canvas.style.display = 'none';
      }
      return;
    }

    // Create canvas if it doesn't exist
    if (!canvas) {
      const container = document.createElement('div');
      container.className = 'fractal-canvas-container';

      canvas = document.createElement('canvas');
      canvas.id = 'fractal-pattern';

      container.appendChild(canvas);
      document.body.insertBefore(container, document.body.firstChild);

      ctx = canvas.getContext('2d');
    } else {
      canvas.style.display = 'block';
    }

    // Set canvas size
    resizeCanvas();

    // Draw fractal
    drawFractal();
  }

  // Resize canvas to match window
  function resizeCanvas() {
    if (!canvas) return;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  // Draw single branch recursively
  function drawBranch(startX, startY, angle, length, depth) {
    if (depth <= 0 || length < 5) return;

    const endX = startX + Math.cos(angle) * length;
    const endY = startY + Math.sin(angle) * length;

    // Calculate opacity and line width based on depth
    const opacity = (depth / 4.0) * 0.3;
    const lineWidth = depth * 0.8;

    // Set line style
    ctx.strokeStyle = `rgba(255, 255, 255, ${opacity})`;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';

    // Draw line
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.stroke();

    // Recursive branches
    const angleVariation = Math.PI / 6; // 30 degrees
    const newLength = length * 0.7;

    drawBranch(endX, endY, angle - angleVariation, newLength, depth - 1);
    drawBranch(endX, endY, angle + angleVariation, newLength, depth - 1);
  }

  // Draw complete fractal pattern
  function drawFractal() {
    if (!canvas || !ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Branch origin points (from spec)
    const branchPoints = [
      { x: 0.2, y: 0.3, depth: 3 },   // Point 1
      { x: 0.7, y: 0.2, depth: 3 },   // Point 2
      { x: 0.5, y: 0.7, depth: 3 },   // Point 3
      { x: 0.85, y: 0.6, depth: 2 }   // Point 4
    ];

    // Reduce complexity on mobile
    const isMobile = window.innerWidth < 768;
    if (isMobile) {
      // Use only 3 points on mobile
      branchPoints.pop();
    }

    // Initial branch length (scaled to canvas size)
    const baseLength = Math.min(canvas.width, canvas.height) * 0.08; // 8% of smaller dimension

    // Draw from each origin point
    branchPoints.forEach(point => {
      const startX = canvas.width * point.x;
      const startY = canvas.height * point.y;

      // 6 branches radiating outward at 60° intervals
      for (let i = 0; i < 6; i++) {
        const angle = (i * Math.PI) / 3; // 60° intervals (0°, 60°, 120°, 180°, 240°, 300°)

        // Limit depth on mobile for performance
        const maxDepth = isMobile ? 2 : point.depth;

        drawBranch(startX, startY, angle, baseLength, maxDepth);
      }
    });
  }

  // Handle window resize
  function handleResize() {
    if (animationId) {
      cancelAnimationFrame(animationId);
    }

    animationId = requestAnimationFrame(() => {
      resizeCanvas();
      drawFractal();
      animationId = null;
    });
  }

  // Initialize on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFractal);
  } else {
    initFractal();
  }

  // Handle window resize
  window.addEventListener('resize', handleResize);

  // Reinitialize when theme changes
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
        initFractal();
      }
    });
  });

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
  });

})();
