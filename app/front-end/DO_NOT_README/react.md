# Notes on **React**

## Rendering

(Re-)render means **React** runs the component function (again) and updates the DOM (only where output changed).

Child components may also re-render unless optimized (`React.memo`, stable props, etc.).

## Hooks

### `useState()`

It triggers a re-render when you call its setter with a new value.
Note: React may skip work if the new value is considered equal to the old one (Object.is check).

### `useRef()`

`useRef()` creates a reference ---actually, it returns an object that refers--- to a mutable object that persists across renders.
This object is `{ current: value }` and the `.current` property oten holds a DOM Node.
With `useRef()` we can refer to a specific instance of an HTML element in a component, which we could not do with traditional **html** attributes.

`ref` is the preferred way to reference DOM elements (native HTML elements) in **React** to avoid issues of rendering, "ownership", mistakenly applying a class to multiple elements and using regular **html** `id`s which would break if the component cntaining the DOM element is reused (instantiated multiple times).

`useRef()` returns an object that makes reference to a DOM element and this object has attribute `.current` which refers to the current instance.

DOM elements have method `.contains()` that determines if the argument is contained in it.

`useRef()` is also used to store mutable values that do not trigger re-renders (e.g., timers, previous values).
Meanning it stores references to things that do not change or that change but are not displayed.

In **React**, components *own* elements, which means that they are responsible for rendering that element.
`useRef()` bypasses ownership by giving direct access to DOM elements and, for this, it should be used sparingly.

### `useEffect()`

```typescript
useEffect(() => {
    // effect logic
    return () => {
    // cleanup
    }
}, [
    // dependencies
])
```

`useEffect()` declares functions that execute when the component is mounted and when the dependencies (in `[]`) change.
With `[]`, the effect runs once after mount, and cleanup runs on dismount.
With `[dependency1, dependency2]`, cleanup runs before re-running the effect when either of the dependencies changes.

If eventListeners were added during mount, they should be removed before the effect runs again or when the component unmounts.
To achieve this we have `useEffect()` return a function that removes the listener.

## Events (**DOM**, not **React**-exclusive)

The `mousedown` event refers to pressing down the mouse button.
Conversely, the `mouseup` event refers to releasing the mouse button, and `click` = `mousedown`+ `mouseup`.
`mousedown`/`pointerdown` is preferable to `click` when we want the effect to occur asap on press (in case other effects are scheduled to occur on click).

`pointer` events refer to the same as `mouse` events but include not only mouse but touch, keyboard focus, and pen.
Some `pointer` events: `pointerdown`, `pointerup`, `pointermove`, `pointercancel` (e.g., canceling of a current mousedown because it became a scroll/drag).
