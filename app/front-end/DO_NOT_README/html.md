# Notes on **html**

## Attributes

### `data-*`

These are custom HTML attributes meant for storing extra metadata on elements.

Example:

```html
<button data-role="logout" data-user-id="42">Log out</button>
```

How they work:

In **HTML/JSX**, you can add any `data-...` name.
In **JS**, you can read them through `dataset`.
In **CSS** or selectors, you can target them with `[data-...]`.

In **JS**:

```javascript
const btn = document.querySelector('[data-role="logout"]') as HTMLButtonElement | null

if (btn) {
  console.log(btn.dataset.role) // "logout"
  console.log(btn.dataset.userId) // "42"
}
```

Key detail about names:

`data-user-id` becomes `dataset.userId`
`data-long-example-name` becomes `dataset.longExampleName`

Common uses:

- Stable selectors for tests (`data-testid`)
- **JS** hooks (instead of brittle class selectors)
- Lightweight metadata on elements.
