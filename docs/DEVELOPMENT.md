# Development Notes

## Browser-only prototype

The current prototype does not need Python dependencies. Open `index.html` directly in a browser.

## Optional local HTTP server

If Node.js is installed:

```bash
npm install
npm start
```

Then open `http://localhost:8080`.

## Tests

`npm test` is configured to run Node.js built-in tests when test files are added. The current prototype does not yet include automated test files.

## Suggested test areas

- A* returns a path for reachable goals and no path for blocked goals.
- Robot movement never enters obstacle cells.
- Task assignments do not assign the same task to multiple robots.
- Q-table synchronization preserves valid numeric values.
- Peer sharing only occurs within the configured radius.
- Reset clears simulation counters and state.
