# Notes on **TailwindCSS**

## **CSS**

### Positioning

#### `position`

<!-- markdownlint-disable MD029 -->
1. `static` (default)

- Element flows normally in the document (`block` elements from the beginning of the "line" occupying the whole width of the viewport, `inline` elements from the beginning of the "line" or right next to the previous `inline` element)
- `top`, `right`, `bottom`, `left` have no effect
- `z-index` is ignored
- This is the baseline behavior

2. `relative`

- Element flows normally but can be offset from its normal position
- `top`, `right`, `bottom`, `left` move it relative to where it would normally be
- `z-index` works (can layer on top of other elements)
- Doesn't remove the element from flow: the space it would occupy is preserved
- Use case: small adjustments to position without breaking layout
- **Creates a positioning context for absolutely-positioned children**

3. `absolute`

- Element is removed from document flow entirely
- Positioned relative to the nearest positioned ancestor (`relative`, `absolute`, `fixed`, or `sticky`)
- If no positioned ancestor exists, positioned relative to the document root
- `top`, `right`, `bottom`, `left` set the offset
- `z-index` works
- Use case: dropdowns, tooltips, overlays, modals

4. `fixed`

- Element is removed from document flow
- Positioned relative to the viewport (the visible window), not the page
- Stays in place even when scrolling
- `top`, `right`, `bottom`, `left` set the offset from viewport edges
- `z-index` works
- Use case: sticky headers, fixed sidebars, notification badges

5. `sticky`

- Hybrid of `relative` and `fixed`
- Flows normally until it hits a scroll threshold
- Then "sticks" to that position while its container scrolls past
- Requires at least one of `top`, `right`, `bottom`, `left` to define where it sticks
- Stays within its parent container (doesn't escape)
- `z-index` works
- Use case: sticky table headers, persistent section titles during scroll

<!-- markdownlint-enable MD029 -->

## CSS Property Grouping Guide

Use this when writing custom CSS (or reading Tailwind utility groups) so property intent stays clear.

### MDN-style categories

1. Positioning

- `position`
- `top`, `right`, `bottom`, `left`
- `z-index`

1. Display and Flow Layout

- `display`
- `float`, `clear`
- `overflow`

1. Flexible Box Layout

- `flex-*`
- `order`
- `gap`

1. Grid Layout

- `grid-*`
- `gap`

1. Box Model

- `box-sizing`
- `margin`
- `padding`
- `width`, `height`, `min/max-*`

1. Text and Fonts

- `font-*`
- `line-height`
- `letter-spacing`
- `text-*`
- `white-space`, `word-break`, `text-overflow`

1. Colors and Backgrounds

- `color`
- `background-*`

1. Borders

- `border-*`
- `border-radius`

1. Visual Effects

- `opacity`
- `box-shadow`
- `filter`, `backdrop-filter`
- `mix-blend-mode`

1. Transforms

- `transform`

1. Transitions and Animations

- `transition-*`
- `animation-*`

1. User Interface

- `cursor`
- `pointer-events`
- `user-select`
- `resize`
- `scroll-behavior`

1. Visibility and Containment

- `visibility`
- `content-visibility`

1. Outlines

- `outline`
- `outline-offset`

1. Custom Properties

- `--*` design tokens

### Tailwind mental model categories

<!-- markdownlint-disable MD029 -->
1. Layout

- `display`
- `position`, `top/right/bottom/left`
- `z-index`
- `float`, `clear`
- `overflow`

2. Flexbox and Grid

- `flex-*`
- `grid-*`
- `order`
- `gap`

3. Sizing

- `width`, `height`, `min/max-*`
- `box-sizing`

4. Spacing

- `margin`
- `padding`

5. Typography

- `font-*`
- `line-height`
- `letter-spacing`
- `text-*`
- `white-space`, `word-break`, `text-overflow`

6. Backgrounds

- `background-*`

7. Borders

- `border-*`
- `border-radius`

8. Effects

- `box-shadow`
- `opacity`
- `filter`, `backdrop-filter`
- `mix-blend-mode`

9. Transforms

- `transform`

10. Transitions and Animation

- `transition-*`
- `animation-*`

11. Interactivity

- `cursor`
- `pointer-events`
- `user-select`
- `resize`
- `scroll-behavior`

12. Accessibility

- `visibility`
- `outline`, `outline-offset`
- `content-visibility`

13. Theme and Tokens

- `--*` custom properties
<!-- markdownlint-enable MD029 -->

## Recommended Property Order (for custom CSS blocks)

Use this order top to bottom inside each rule:

1. Layout (`display`, `position`, `inset`, `z-index`, flow)
2. Flexbox/Grid (`flex-*`, `grid-*`, `gap`, `order`)
3. Box Model (`box-sizing`, sizing, margin, padding)
4. Typography (`font-*`, `line-height`, text)
5. Visuals (`color`, `background-*`, `border-*`, `shadow`, `opacity`)
6. Effects and Motion (`transform`, `transition-*`, `animation-*`)
7. Interaction and A11y (`cursor`, `pointer-events`, `outline`, `visibility`)
8. Custom properties (`--*`) when local overrides are needed

### Example

```css
.card {
  display: grid;
  position: relative;
  gap: 0.75rem;

  width: 100%;
  max-width: 28rem;
  padding: 1rem;

  font-size: 0.95rem;
  line-height: 1.4;

  color: var(--color-fg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 0.75rem;
  box-shadow: 0 8px 24px rgb(0 0 0 / 0.08);

  transition: box-shadow 150ms ease, transform 150ms ease;
  cursor: pointer;
}
```
