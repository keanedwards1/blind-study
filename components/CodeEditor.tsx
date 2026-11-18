"use client";

import { loader, type Monaco, type OnMount } from "@monaco-editor/react";
import { useEffect, useRef, useState } from "react";
import { useTheme } from "./ThemeToggle";

type Editor = Parameters<OnMount>[0];

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
}: {
  value: string;
  onChange?: (v: string) => void;
  readOnly?: boolean;
  onRun?: () => void;
  onSubmit?: () => void;
}) {
  const theme = useTheme();
  const host = useRef<HTMLDivElement>(null);
  const editorRef = useRef<Editor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const [ready, setReady] = useState(false);
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
        setReady(true);
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

  return (
    <div className="relative h-full w-full">
      <div ref={host} className="h-full w-full" />
      {!ready && <div className="absolute inset-0 p-4 text-sm text-subtle">Loading editor…</div>}
    </div>
  );
}
