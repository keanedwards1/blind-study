/* eslint-disable @typescript-eslint/no-namespace */

type MonacoWin = Window & {
  monaco?: { editor: { getModels(): { getValue(): string; setValue(v: string): void; isDisposed(): boolean }[] } };
};

declare global {
  namespace Cypress {
    interface Chainable {
      /** Wait until the Pyodide worker reports it's ready. */
      waitForPython(): Chainable<void>;
      /** Replace the editor contents. */
      setCode(code: string): Chainable<void>;
      /** Read the editor contents. */
      getCode(): Chainable<string>;
      /** Click Run / Submit (or "Submit & explain" in the mock). */
      clickRun(): Chainable<void>;
      clickSubmit(label?: string): Chainable<void>;
      /** Set a (React-controlled) textarea's value in one go. */
      fillTextarea(value: string): Chainable<void>;
      /** Assert the results panel verdict, e.g. "Accepted". */
      verdict(text: string | RegExp): Chainable<void>;
    }
  }
}

function liveModel(win: MonacoWin) {
  const models = win.monaco?.editor.getModels().filter((m) => !m.isDisposed()) ?? [];
  return models[models.length - 1];
}

Cypress.Commands.add("waitForPython", () => {
  cy.contains("Python ready", { timeout: 120000 }).should("be.visible");
});

Cypress.Commands.add("setCode", (code: string) => {
  cy.window({ timeout: 30000 }).should((win) => {
    expect(liveModel(win as MonacoWin), "monaco model").not.to.equal(undefined);
  });
  cy.window().then((win) => liveModel(win as MonacoWin)!.setValue(code));
});

Cypress.Commands.add("getCode", () => {
  return cy.window().then((win) => liveModel(win as MonacoWin)?.getValue() ?? "");
});

Cypress.Commands.add("clickRun", () => {
  cy.contains("button", /^Run$/).should("be.enabled").click();
});

Cypress.Commands.add("clickSubmit", (label = "Submit") => {
  cy.contains("button", new RegExp(`^${label}$`)).should("be.enabled").click();
});

Cypress.Commands.add("verdict", (text: string | RegExp) => {
  cy.contains(text, { timeout: 30000 }).should("be.visible");
});

// Wait for React to hydrate after every visit so clicks/typing hit live handlers.
type AnyOverwrite = (name: string, fn: (originalFn: (...a: unknown[]) => Cypress.Chainable, ...args: unknown[]) => unknown) => void;
(Cypress.Commands.overwrite as unknown as AnyOverwrite)("visit", (originalFn, ...args) =>
  originalFn(...args).then(() => cy.get("html[data-hydrated]", { timeout: 30000 })),
);

Cypress.Commands.add("fillTextarea", { prevSubject: "element" }, (subject: JQuery<HTMLElement>, value: string) => {
  const el = subject[0] as HTMLTextAreaElement;
  const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value")!.set!;
  setter.call(el, value);
  el.dispatchEvent(new Event("input", { bubbles: true }));
});

export {};
