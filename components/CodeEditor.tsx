"use client";

import { loader, type Monaco, type OnMount } from "@monaco-editor/react";
import { useEffect, useRef, useState } from "react";
import { useTheme } from "./ThemeToggle";

type Editor = Parameters<OnMount>[0];
export type Keymap = "default" | "vim" | "emacs";

/**
 * Vim and Emacs keybindings: the monaco-vim / monaco-emacs browser bundles, loaded from jsDelivr the first time they're
 * picked. Loaded as plain scripts they use the global `monaco` (the CDN editor's), so no second copy of Monaco is bundled.
 * Monaco's AMD loader defines a global `define`; it's hidden while an add-on loads so the bundle takes its browser path.
 */
const ADDONS = {
  vim: { url: "https://cdn.jsdelivr.net/npm/monaco-vim@0.4.4/dist/monaco-vim.umd.js", global: "MonacoVim" },
  emacs: { url: "https://cdn.jsdelivr.net/npm/monaco-emacs@0.3.0/dist/monaco-emacs.js", global: "MonacoEmacs" },
} as const;
type VimLib = { initVimMode(editor: Editor, status: HTMLElement | null): { dispose(): void } };
type EmacsLib = { EmacsExtension: new (editor: Editor) => { start(): void; dispose(): void } };
const addonLoads = new Map<string, Promise<unknown>>();
function loadAddon(kind: "vim" | "emacs"): Promise<unknown> {
  const { url, global } = ADDONS[kind];
  const w = window as unknown as Record<string, unknown>;
  if (w[global]) return Promise.resolve(w[global]);
  let p = addonLoads.get(kind);
  if (!p) {
    p = new Promise((resolve, reject) => {
      const saved = w.define;
      w.define = undefined;
      const s = document.createElement("script");
      s.src = url;
      s.crossOrigin = "anonymous";
      s.onload = () => {
        w.define = saved;
        resolve(w[global]);
      };
      s.onerror = () => {
        w.define = saved;
        addonLoads.delete(kind);
        reject(new Error(`Couldn't load ${kind} keybindings`));
      };
      document.head.appendChild(s);
    });
    addonLoads.set(kind, p);
  }
  return p;
}

/**
 * Disposing an editor (e.g. leaving a page quickly) makes Monaco cancel its background work, which surfaces as an
 * unhandled promise rejection named "Canceled". It's expected and harmless, so swallow exactly that one.
 */
let cancelGuard = false;
function ignoreMonacoCancellations() {
  if (cancelGuard || typeof window === "undefined") return;
  cancelGuard = true;
  window.addEventListener("unhandledrejection", (e) => {
    const reason = e.reason as { name?: string; message?: string } | undefined;
    if (reason?.name === "Canceled" && reason?.message === "Canceled") e.preventDefault();
  });
}

const OPTIONS = {
  language: "python",
  fontSize: 14,
  tabSize: 4,
  insertSpaces: true,
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  automaticLayout: true,
  padding: { top: 12 },
  fixedOverflowWidgets: true,
  // Let the wheel scroll the page once the editor has nothing left to scroll (or fits entirely).
  scrollbar: { alwaysConsumeMouseWheel: false },
} as const;

/**
 * Monaco, created and disposed by this component's own effect.
 *
 * With Cache Components, Next keeps pages you navigate away from alive but hidden (React <Activity>): their effects are
 * cleaned up when the page hides and run again when you come back. @monaco-editor/react's <Editor> doesn't survive that
 * (it reuses an editor it already disposed, which throws and takes the page down), so this creates a fresh editor each time
 * the effect runs. The code itself lives in the parent's state, so nothing is lost.
 */
export default function CodeEditor({
  value,
  onChange,
  readOnly,
  onRun,
  onSubmit,
  keymap = "default",
}: {
  value: string;
  onChange?: (v: string) => void;
  readOnly?: boolean;
  onRun?: () => void;
  onSubmit?: () => void;
  /** Editing mode: normal, Vim or Emacs keybindings. */
  keymap?: Keymap;
}) {
  const theme = useTheme();
  const host = useRef<HTMLDivElement>(null);
  const editorRef = useRef<Editor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const statusRef = useRef<HTMLDivElement>(null);
  // Bumped each time a fresh editor is created (first load, or coming back to a page Next kept alive), so add-ons re-attach.
  const [editorVersion, setEditorVersion] = useState(0);
  const ready = editorVersion > 0;
  // The latest props, for callbacks registered once when the editor is created.
  const latest = useRef({ value, onChange, readOnly, onRun, onSubmit, theme });
  useEffect(() => {
    latest.current = { value, onChange, readOnly, onRun, onSubmit, theme };
  });

  useEffect(() => {
    ignoreMonacoCancellations();
    let cancelled = false;
    let editor: Editor | null = null;
    loader
      .init()
      .then((monaco) => {
        if (cancelled || !host.current) return;
        const l = latest.current;
        monacoRef.current = monaco;
        // This Monaco build doesn't set a global; Vim/Emacs keybinding add-ons (and the Cypress helpers) look for one.
        (window as unknown as { monaco?: Monaco }).monaco ??= monaco;
        const ed = monaco.editor.create(host.current, {
          ...OPTIONS,
          value: l.value,
          theme: l.theme === "dark" ? "vs-dark" : "light",
          readOnly: l.readOnly,
          renderLineHighlight: l.readOnly ? "none" : "line",
        });
        editor = ed;
        ed.onDidChangeModelContent(() => {
          const v = ed.getValue();
          if (v !== latest.current.value) latest.current.onChange?.(v);
        });
        ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => latest.current.onRun?.());
        ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => latest.current.onSubmit?.());
        if (!l.readOnly) ed.focus();
        editorRef.current = ed;
        setEditorVersion((v) => v + 1);
      })
      .catch((err: unknown) => {
        if ((err as { type?: string })?.type !== "cancelation") console.error("Monaco failed to load", err);
      });
    return () => {
      cancelled = true;
      editorRef.current = null;
      if (editor) {
        editor.getModel()?.dispose();
        editor.dispose();
      }
    };
  }, []);

  // Code changed from outside (Reset, Load solution, switching problems): replace the text, keeping it undoable.
  useEffect(() => {
    const ed = editorRef.current;
    const model = ed?.getModel();
    if (!ed || !model || ed.getValue() === value) return;
    ed.pushUndoStop();
    ed.executeEdits("external", [{ range: model.getFullModelRange(), text: value }]);
    ed.pushUndoStop();
  }, [value]);

  useEffect(() => {
    monacoRef.current?.editor.setTheme(theme === "dark" ? "vs-dark" : "light");
  }, [theme]);

  useEffect(() => {
    editorRef.current?.updateOptions({ readOnly, renderLineHighlight: readOnly ? "none" : "line" });
  }, [readOnly]);

  // Vim / Emacs keybindings, attached to the live editor and removed when the mode changes or the editor goes away.
  useEffect(() => {
    const ed = editorRef.current;
    if (!editorVersion || !ed || keymap === "default") return;
    let active: { dispose(): void } | null = null;
    let stopped = false;
    loadAddon(keymap)
      .then((lib) => {
        if (stopped || editorRef.current !== ed) return;
        if (keymap === "vim") active = (lib as VimLib).initVimMode(ed, statusRef.current);
        else {
          const ext = new (lib as EmacsLib).EmacsExtension(ed);
          ext.start();
          active = ext;
        }
        ed.focus();
      })
      .catch((err: unknown) => console.error(err));
    const status = statusRef.current;
    return () => {
      stopped = true;
      active?.dispose();
      if (status) status.textContent = "";
    };
  }, [editorVersion, keymap]);

  return (
    <div className="relative flex h-full w-full flex-col">
      <div ref={host} className="min-h-0 w-full flex-1" />
      {keymap === "vim" && (
        // Vim's mode line (-- NORMAL --, -- INSERT --, :commands), filled in by monaco-vim.
        <div ref={statusRef} className="h-6 shrink-0 border-t border-line px-3 font-mono text-xs leading-6 text-muted" aria-live="polite" />
      )}
      {!ready && <div className="absolute inset-0 p-4 text-sm text-subtle">Loading editor…</div>}
    </div>
  );
}
