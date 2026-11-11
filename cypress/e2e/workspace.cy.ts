import data from "../../data/problems.json";

const twoSum = data.problems.find((p) => p.slug === "two-sum")!;
const mod = Cypress.platform === "darwin" ? "{meta}" : "{ctrl}";

describe("Problem workspace", () => {
  beforeEach(() => {
    cy.visit("/problems/two-sum");
    cy.waitForPython();
  });

  it("shows the statement and examples", () => {
    cy.contains("h1", "Two Sum");
    cy.contains("Example 1");
    cy.contains("nums = [2, 7, 11, 15], target = 9");
    cy.getCode().should("include", "def two_sum(nums: List[int], target: int) -> List[int]:");
  });

  it("reports a wrong answer on the starter code", () => {
    cy.clickRun();
    cy.verdict("Wrong Answer");
    cy.contains("Your output").next().should("have.text", "None");
  });

  it("accepts a correct solution, marks it solved and shows stdout", () => {
    cy.setCode(twoSum.solution.replace("for i, n in enumerate(nums):", "print('debug-line')\n    for i, n in enumerate(nums):"));
    cy.clickRun();
    cy.verdict("All examples passed");
    cy.clickSubmit();
    cy.verdict("Accepted");
    cy.contains(`${twoSum.tests.length} / ${twoSum.tests.length} passed`);
    cy.contains("debug-line");
    cy.contains("span", /^Solved$/);

    cy.visit("/");
    cy.get('a[href="/problems/two-sum"]').should("contain", "✓");
    cy.contains(`1 / ${data.problems.length} solved`);
  });

  it("shows a runtime error with the user's line", () => {
    cy.setCode("def two_sum(nums, target):\n    return nums[999]\n");
    cy.clickRun();
    cy.verdict("Runtime Error");
    cy.contains("Line 2, in two_sum");
    cy.contains("IndexError: list index out of range");
  });

  it("shows a syntax error", () => {
    cy.setCode("def two_sum(nums, target)\n    pass\n");
    cy.clickRun();
    cy.verdict("Compile / Load Error");
    cy.contains("SyntaxError");
  });

  it("times out an infinite loop and recovers", () => {
    cy.setCode("def two_sum(nums, target):\n    while True:\n        pass\n");
    cy.clickRun();
    cy.verdict("Time Limit Exceeded");
    cy.waitForPython();
    cy.setCode(twoSum.solution);
    cy.clickRun();
    cy.verdict("All examples passed");
  });

  it("runs with the keyboard shortcut", () => {
    cy.setCode(twoSum.solution);
    // Monaco listens for keydown on its hidden textarea; dispatch the chord directly.
    cy.get(".monaco-editor .view-lines").first().click();
    cy.focused().trigger("keydown", {
      key: "Enter", code: "Enter", keyCode: 13, which: 13, metaKey: mod === "{meta}", ctrlKey: mod === "{ctrl}", bubbles: true, force: true,
    });
    cy.verdict("All examples passed");
  });

  it("keeps code across reloads and can reset it", () => {
    cy.setCode("# my work in progress\n" + twoSum.starter);
    cy.wait(600); // debounced save
    cy.reload();
    cy.waitForPython();
    cy.getCode().should("include", "# my work in progress");
    cy.contains("button", "Reset").click(); // window.confirm is auto-accepted
    cy.getCode().should("not.include", "# my work in progress");
  });

  it("reveals hints one at a time and the solution on demand", () => {
    cy.contains("button", /^Hints/).click();
    cy.contains("Hint 1").should("not.exist");
    cy.contains("button", "Show hint 1").click();
    cy.contains("Hint 1");
    cy.contains("button", "Show hint 2").click();
    cy.contains("That's all the hints.");

    cy.contains("button", "Solution").click();
    cy.contains("index_of").should("not.exist");
    cy.contains("button", "Reveal solution").click();
    cy.contains("Time:");
    cy.contains("button", "Load solution into editor").click();
    cy.getCode().should("include", "index_of");
  });

  it("navigates to the next problem", () => {
    cy.contains("a", "Next ›").click();
    cy.location("pathname").should("eq", `/problems/${data.problems[data.problems.indexOf(twoSum) + 1].slug}`);
    cy.contains("h1", data.problems[data.problems.indexOf(twoSum) + 1].title);
  });
});

describe("Special problem types through the UI", () => {
  // One of each harness feature: linked list, tree, in-place mutation, class ops, custom driver, custom checker.
  ["merge-two-sorted-lists", "invert-binary-tree", "rotate-image", "implement-trie-prefix-tree", "linked-list-cycle", "clone-graph", "alien-dictionary"].forEach(
    (slug) => {
      it(`accepts the reference solution for ${slug}`, () => {
        const p = data.problems.find((x) => x.slug === slug)!;
        cy.visit(`/problems/${slug}`);
        cy.waitForPython();
        cy.clickSubmit();
        cy.verdict(/Wrong Answer|Runtime Error/); // starter fails…
        cy.setCode(p.solution);
        cy.clickSubmit();
        cy.verdict("Accepted"); // …reference passes
      });
    },
  );
});
