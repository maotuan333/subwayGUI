import "./App.css";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import Editor from '@monaco-editor/react';
import { useRef } from "react";
import DnDFlow from "./components/canvas/ReactFlowDnd";

function App() {
  const editorRef = useRef(null);

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor;
  }

  return (
    <div style={{ display: 'flex' }}>
      <PanelGroup direction="horizontal">
        <Panel defaultSize={50} minSize={30}>
          <Editor
            height="90vh"
            defaultLanguage="json"
            defaultValue="// some comment"
            onMount={handleEditorDidMount}
          />
        </Panel>
        <PanelResizeHandle style={{
          flex: '0 0 0.25rem',
          // display: 'flex',
          // justifyContent: 'stretch',
          alignItems: 'stretch',
          outline: 'none',
          transition: 'background-color 0.2s linear',
          backgroundColor: 'green'

        }} />
        <PanelResizeHandle />
        <Panel defaultSize={50} minSize={20}>
          <DnDFlow />
        </Panel>
      </PanelGroup>
    </div>
  );
}

export default App;
