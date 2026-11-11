import data from "../../data/problems.json";

describe("Problem list", () => {
  beforeEach(() => cy.visit("/"));

  it("lists every problem under its category", () => {
    cy.get('a[href^="/problems/"]').should("have.length", data.problems.length);
    data.categories.forEach((cat) => cy.contains("h2", cat, { matchCase: false }));
    cy.contains(`0 / ${data.problems.length} solved`);
  });

  it("filters by search text, difficulty and status", () => {
    cy.get('input[placeholder="Search problems"]').type("palindrom");
    cy.get('a[href^="/problems/"]').should("have.length", 3);

    cy.get('input[placeholder="Search problems"]').clear();
    cy.get("select").first().select("Hard");
    const hard = data.problems.filter((p) => p.difficulty === "Hard").length;
    cy.get('a[href^="/problems/"]').should("have.length", hard);

    cy.get("select").eq(1).select("Solved");
    cy.contains("No problems match.");
  });

  it("opens a random unsolved problem", () => {
    cy.contains("button", "Random unsolved").click();
    cy.location("pathname").should("match", /^\/problems\/[a-z0-9-]+$/);
    cy.contains("Example 1");
  });

  it("exports progress as a JSON download", () => {
    cy.window().then((win) => cy.stub(win.URL, "createObjectURL").as("blob").returns("blob:x"));
    cy.contains("button", "Export").click();
    cy.get("@blob").should("have.been.calledOnce");
  });
});

describe("Problem routes", () => {
  it("serves a page for every problem", () => {
    data.problems.forEach((p) => {
      cy.request(`/problems/${p.slug}`).then((res) => {
        expect(res.status, p.slug).to.eq(200);
        expect(res.body, p.slug).to.include(p.title.replace(/&/g, "&amp;").replace(/'/g, "&#x27;"));
      });
    });
  });

  it("shows the not-found page for an unknown problem", () => {
    // The page reads `params` inside <Suspense> (required by Cache Components), so streaming has
    // already started when notFound() runs: Next keeps HTTP 200 and adds a noindex tag (documented behaviour).
    cy.request({ url: "/problems/not-a-real-problem", failOnStatusCode: false }).then((res) => {
      expect(res.body).to.include("This page could not be found");
      expect(res.body).to.include("noindex");
    });
    cy.visit("/problems/not-a-real-problem", { failOnStatusCode: false });
    cy.contains("This page could not be found");
  });
});
