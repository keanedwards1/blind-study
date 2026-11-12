"use client";

import Editor, { type OnMount } from "@monaco-editor/react";
import { useEffect, useRef } from "react";
import { useTheme } from "./ThemeToggle";

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
  const runRef = useRef(onRun);
  const submitRef = useRef(onSubmit);
  useEffect(() => {
    runRef.current = onRun;
    submitRef.current = onSubmit;
  }, [onRun, onSubmit]);

  const onMount: OnMount = (editor, monaco) => {
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => runRef.current?.());
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => submitRef.current?.());
    if (!readOnly) editor.focus();
  };

  return (
    <Editor
      height="100%"
      language="python"
      theme={theme === "dark" ? "vs-dark" : "light"}
      value={value}
      onChange={(v) => onChange?.(v ?? "")}
      onMount={onMount}
      loading={<div className="p-4 text-sm text-subtle">Loading editor…</div>}
      options={{
        readOnly,
        fontSize: 14,
        tabSize: 4,
        insertSpaces: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        automaticLayout: true,
        padding: { top: 12 },
        renderLineHighlight: readOnly ? "none" : "line",
        fixedOverflowWidgets: true,
        // Let the wheel scroll the page once the editor has nothing left to scroll (or fits entirely).
        scrollbar: { alwaysConsumeMouseWheel: false },
      }}
    />
  );
}
