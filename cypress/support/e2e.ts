import "./commands";

// Fail any test whose page logs a console.error (React/Next warnings, hydration
// mismatches, Cache Components validation errors in dev, etc.). Uncaught
// exceptions already fail tests by default.
const consoleErrors: string[] = [];

// Known noise that isn't from this app.
const IGNORED = [/ResizeObserver loop/, /Download the React DevTools/];

Cypress.on("window:before:load", (win) => {
  const original = win.console.error.bind(win.console);
  win.console.error = (...args: unknown[]) => {
    const text = args.map((a) => (a instanceof Error ? a.message : String(a))).join(" ");
    if (!IGNORED.some((re) => re.test(text))) consoleErrors.push(text.slice(0, 500));
    original(...args);
  };
});

beforeEach(() => {
  consoleErrors.length = 0;
});

afterEach(() => {
  cy.then(() => {
    expect(consoleErrors, "console.error calls on the page").to.deep.equal([]);
  });
});
