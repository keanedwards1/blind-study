import learn from "../../data/learn.json";
import data from "../../data/problems.json";

const twoSum = data.problems.find((p) => p.slug === "two-sum")!;

/** Click the correct option of the quiz card at `index` (options are shuffled on screen). */
function answerCorrectly(card: Cypress.Chainable<JQuery<HTMLElement>>, q: { options: string[]; answer: number }) {
  card.within(() => cy.contains("button", q.options[q.answer]).click());
}

describe("Theme", () => {
  it("defaults to light and remembers dark mode", () => {
    cy.visit("/");
    cy.get("html").should("not.have.attr", "data-theme");
    cy.get("body").should("have.css", "background-color", "rgb(250, 250, 249)");
    cy.get('button[aria-label="Switch to dark mode"]').click();
    cy.get("html").should("have.attr", "data-theme", "dark");
    cy.reload();
    cy.get("html").should("have.attr", "data-theme", "dark");
    cy.get("body").should("have.css", "background-color", "rgb(9, 9, 11)");
    cy.get('button[aria-label="Switch to light mode"]').click();
    cy.get("html").should("have.attr", "data-theme", "light");
  });
});

describe("Problem Learn tab", () => {
  beforeEach(() => cy.visit("/problems/two-sum"));

  it("hides building blocks until asked, then shows pattern, concepts and quiz", () => {
    cy.contains("button", /^Learn$/).click();
    cy.contains("Pattern: Arrays & Hashing").should("not.exist");
    cy.contains("button", "Show building blocks").click();
    cy.contains("Pattern: Arrays & Hashing");
    twoSum.concepts.forEach((id) => {
      const c = learn.concepts.find((x) => x.id === id)!;
      cy.contains("button", c.title.split(" (")[0]);
    });
    cy.contains("button", /^dict$/).click();
    cy.get('[data-testid="concept-detail"]').should("contain", "dict (hash map)");
    cy.get('[data-testid="quiz-card"]').should("have.length", twoSum.quiz.length);
  });

  it("grades quiz answers and records them for the quiz drill", () => {
    cy.contains("button", /^Learn$/).click();
    cy.contains("button", "Show building blocks").click();
    const [first, second] = twoSum.quiz;
    answerCorrectly(cy.get('[data-testid="quiz-card"]').eq(0), first);
    cy.get('[data-testid="quiz-card"]').eq(0).should("contain", "Correct");
    const wrong = second.options.find((_, i) => i !== second.answer)!;
    cy.get('[data-testid="quiz-card"]').eq(1).within(() => cy.contains("button", wrong).click());
    cy.get('[data-testid="quiz-card"]').eq(1).should("contain", "Not quite");
    cy.contains("1 / 2 correct");

    cy.visit("/quiz");
    cy.contains("Answered").prev().should("contain", "2 /");
    cy.contains("To review").prev().should("have.text", "1");
  });

  it("tags each solution line with the Python concepts it uses", () => {
    cy.contains("button", "Solution").click();
    cy.contains("button", "Reveal solution").click();
    cy.get('[data-testid="solution-breakdown"]').within(() => {
      cy.contains("index_of = {}");
      cy.contains("button", "enumerate & zip").click();
    });
    cy.get('[data-testid="concept-detail"]').should("contain", "enumerate & zip");
  });
});

describe("Learn page", () => {
  beforeEach(() => cy.visit("/learn"));

  it("has a guide for every pattern and a card for every Python concept", () => {
    learn.patterns.forEach((p) => cy.get(`#pattern-${p.id}`).should("contain", p.category));
    learn.concepts.forEach((c) => cy.get(`#py-${c.id}`).should("contain", c.title));
  });

  it("shows build-time output, then runs edited code in the browser", () => {
    const heap = learn.concepts.find((c) => c.id === "heapq")!;
    cy.get("#py-heapq").within(() => {
      cy.get('[data-testid="playground-output"]').should("have.text", heap.output);
      cy.get("textarea").fillTextarea("import heapq\nh = [3, 1, 2]\nheapq.heapify(h)\nprint('top', h[0])");
      cy.contains("button", "Run").click();
      cy.get('[data-testid="playground-output"]', { timeout: 120000 }).should("have.text", "top 1");
      cy.contains("button", "Reset").click();
      cy.get("textarea").should("have.value", heap.snippet);
    });
  });

  it("shows errors from playground code", () => {
    cy.get("#py-dict").within(() => {
      cy.get("textarea").fillTextarea("d = {}\nprint(d['missing'])");
      cy.contains("button", "Run").click();
      cy.get('[data-testid="playground-output"]', { timeout: 120000 }).should("contain", "KeyError").and("contain", "Line 2");
    });
  });

  it("grades a concept quiz", () => {
    const q = learn.concepts.find((c) => c.id === "set")!.quiz[0];
    answerCorrectly(cy.get("#py-set").find('[data-testid="quiz-card"]').first(), q);
    cy.get("#py-set").find('[data-testid="quiz-card"]').first().should("contain", "Correct");
  });
});

describe("Quiz drill", () => {
  const all = [
    ...data.problems.flatMap((p) => p.quiz),
    ...learn.patterns.flatMap((p) => p.quiz),
    ...learn.concepts.flatMap((c) => c.quiz),
  ];

  it("runs a round, scores it, and offers missed questions for review", () => {
    cy.visit("/quiz");
    cy.contains(`drawn from all ${all.length} questions`);
    cy.contains("label", "Round size").find("select").select("5");
    cy.contains("button", /^Start/).click();
    for (let i = 0; i < 5; i++) {
      // Always pick the first option shown; some will be wrong, which feeds the review pile.
      cy.get('[data-testid="quiz-card"] button').first().click();
      if (i < 4) cy.contains("button", "Next question").click();
    }
    cy.contains(/^\d \/ 5$/);
    cy.contains("button", "Change settings").click();
    cy.contains("Answered").prev().should("contain", "5 /");
    cy.get("body").then(($b) => {
      const missed = Number($b.find(":contains('To review')").last().prev().text());
      if (missed > 0) {
        cy.contains("label", "Only review missed").find("input").check();
        cy.contains(`${missed} match these filters`);
      }
    });
  });

  it("shows each question with the context it's about", () => {
    cy.visit("/quiz");
    cy.contains("label", "Questions about").find("select").select("Problems");
    cy.contains("label", "Category").find("select").select("Stack"); // only Valid Parentheses
    cy.contains("button", /^Start/).click();
    cy.get('[data-testid="quiz-context"]').within(() => {
      cy.contains("Problem");
      cy.contains("h2", "Valid Parentheses");
      cy.contains("balanced");
      cy.contains("Input: s = \"()\"");
      cy.contains("def is_valid").should("not.exist");
      cy.contains("button", "Show the reference solution").click();
      cy.contains("def is_valid");
    });

    cy.visit("/quiz");
    cy.contains("label", "Questions about").find("select").select("Python");
    cy.contains("button", /^Start/).click();
    cy.get('[data-testid="quiz-context"]').should("contain", "Python concept").find("button").click();
    cy.get('[data-testid="quiz-context"] pre').should("contain", "print");
  });

  it("filters by source and category", () => {
    cy.visit("/quiz");
    cy.contains("label", "Questions about").find("select").select("Python");
    cy.contains(`${learn.concepts.flatMap((c) => c.quiz).length} match these filters`);
    cy.contains("label", "Questions about").find("select").select("Problems");
    cy.contains("label", "Category").find("select").select("Stack");
    cy.contains(`${data.problems.filter((p) => p.category === "Stack").flatMap((p) => p.quiz).length} match these filters`);
  });
});
