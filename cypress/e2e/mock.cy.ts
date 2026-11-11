import data from "../../data/problems.json";

/** Replace getUserMedia with a synthetic camera (animated canvas) + mic (oscillator), so tests need no hardware. */
function fakeMedia(win: Window & typeof globalThis, opts: { micFails?: boolean } = {}) {
  cy.stub(win.navigator.mediaDevices, "getUserMedia")
    .as("getUserMedia")
    .callsFake(async (c: MediaStreamConstraints) => {
      if (c.audio && opts.micFails) throw new DOMException("Requested device not found", "NotFoundError");
      const canvas = win.document.createElement("canvas");
      canvas.width = 160;
      canvas.height = 120;
      const ctx = canvas.getContext("2d")!;
      let hue = 0;
      const draw = () => {
        ctx.fillStyle = `hsl(${(hue += 7) % 360} 80% 50%)`;
        ctx.fillRect(0, 0, 160, 120);
        win.requestAnimationFrame(draw);
      };
      draw();
      const stream = canvas.captureStream(15);
      if (c.audio) {
        const ac = new win.AudioContext();
        const osc = ac.createOscillator();
        const dst = ac.createMediaStreamDestination();
        osc.connect(dst);
        osc.start();
        stream.addTrack(dst.stream.getAudioTracks()[0]);
      }
      return stream;
    });
}

function configure({ problems, minutes, explain }: { problems?: number; minutes?: number; explain?: number }) {
  const field = (label: string) => cy.contains("label", label).find("input");
  if (problems) field("Problems").clear().type(String(problems));
  if (minutes) field("Time limit").clear().type(String(minutes));
  if (explain) field("Explanation max").clear().type(String(explain));
}

describe("Mock assessment", () => {
  it("runs a full session: code, submit, record, results, history", () => {
    cy.visit("/mock", { onBeforeLoad: (win) => fakeMedia(win) });
    configure({ problems: 2 });
    cy.contains("Difficulty order: Easy → Medium");
    cy.contains("button", /^Start/).click();

    // Problem 1: timer is running and hints/solutions are hidden.
    cy.contains("Problem 1 of 2 · coding");
    cy.get(".tabular-nums").invoke("text").then((t1) => {
      cy.get(".tabular-nums", { timeout: 4000 }).should((el) => expect(el.text()).not.to.eq(t1));
    });
    cy.contains("button", /^Hints/).should("not.exist");
    cy.waitForPython();

    // Solve it with the reference solution.
    cy.get("h1")
      .invoke("text")
      .then((title) => {
        const p = data.problems.find((x) => x.title === title)!;
        expect(p.difficulty).to.eq("Easy");
        cy.setCode(p.solution);
      });
    cy.clickSubmit("Submit & explain");

    // Explanation phase: code locked, record with the fake camera.
    cy.contains("Problem 1 of 2 · explanation");
    cy.contains(/(\d+)\/\1 tests passed/);
    cy.contains("button", "Turn on camera").click();
    cy.contains("button", "Start recording").click();
    cy.contains("REC");
    cy.wait(2200);
    cy.contains("button", "Stop").click();
    cy.contains("button", "Re-record");
    cy.get("video[controls]").should("have.length", 1);
    cy.contains("button", "Next problem").click();

    // Problem 2: submit the starter without recording.
    cy.contains("Problem 2 of 2 · coding");
    cy.waitForPython();
    cy.clickSubmit("Submit & explain");
    cy.contains("You can continue without recording.");
    cy.contains("button", "Finish & see results").click();

    // Summary.
    cy.contains("h1", "Results");
    cy.contains(/explanation 0:0[2-3]/);
    cy.get("video[controls]").should("have.length", 1);
    cy.contains(/^0\/\d+ tests$/);

    // History persists.
    cy.contains("button", "New mock assessment").click();
    cy.contains("Past sessions");
    cy.contains("1/2 fully passed");
  });

  it("auto-submits and ends the session when time runs out", () => {
    // Fake only Date + setInterval so the countdown can be fast-forwarded while workers/editor use real timers.
    cy.clock(Date.now(), ["Date", "setInterval", "clearInterval"]);
    cy.visit("/mock");
    configure({ problems: 2, minutes: 1 });
    cy.contains("button", /^Start/).click();
    cy.contains("Problem 1 of 2 · coding");
    cy.waitForPython();
    cy.tick(61_000);
    cy.contains("h1", "Results", { timeout: 30000 });
    cy.contains("Time ran out.");
    cy.contains(/^0\/\d+ tests$/); // problem 1 auto-submitted with the starter code
    cy.contains("Not submitted"); // problem 2 never reached
  });

  it("falls back to video-only when the microphone is unavailable", () => {
    cy.visit("/mock", { onBeforeLoad: (win) => fakeMedia(win, { micFails: true }) });
    configure({ problems: 1 });
    cy.contains("button", /^Start/).click();
    cy.waitForPython();
    cy.clickSubmit("Submit & explain");
    cy.contains("button", "Turn on camera").click();
    cy.contains("Microphone unavailable");
    cy.contains("button", "Start recording");
  });

  it("can be ended early", () => {
    cy.visit("/mock");
    cy.contains("button", /^Start/).click();
    cy.contains("Problem 1 of 3");
    cy.contains("button", /^End$/).click();
    cy.contains("h1", "Results");
    cy.get("span:contains('Not submitted')").should("have.length", 3);
  });
});
