import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import { Editor, useMonaco } from "@monaco-editor/react";
import { useEffect, useRef } from "react";
import DnDFlow from "../components/canvas/ReactFlowDnd";
import { useReactFlow } from "reactflow";

function SchemaBuilder() {
  const editorRef = useRef(null);

  const monaco = useMonaco();
  // const { screenToFlowPosition, setViewport, setCenter } = useReactFlow();

  useEffect(() => {
    if (monaco) {
      monaco.editor.defineTheme("my-theme", {
        base: "vs",
        inherit: true,
        rules: [],
        colors: {
          "editor.background": "#000000",
        },
      });
    }
  }, [monaco]);

  function handleEditorDidMount(editor, _) {
    editorRef.current = editor;
  }

  return (
    <>
      <div
        id="schema-navbar"
        className="bg-primary-gray w-full py-2 min-h-12 border-b-[1px] border-seperator flex items-center px-4 justify-between"
      >
        <h6 className="text-lg font-medium">Schema Builder</h6>
      </div>

      <PanelGroup direction="horizontal">
        <div className="w-[25%] border-r-[1px] border-seperator"></div>
        <div className="w-full">
          <DnDFlow />
        </div>
      </PanelGroup>
    </>
  );
}

export default SchemaBuilder;
