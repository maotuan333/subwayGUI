import "./App.css";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import Editor from '@monaco-editor/react';
import { useRef } from "react";
import DnDFlow from "./components/canvas/ReactFlowDnd";

import { Routes, Route, Outlet } from "react-router-dom";
import SchemaBuilder from "./pages/SchemaBuilder";
import Missing from "./components/router/Missing";
import Home from "./pages/Home";
import Titlebar from "./components/window/Titlebar";
import { useCallback, useEffect, useState } from "react";
import { appWindow } from "@tauri-apps/api/window";
import Sidebar from "./components/window/Sidebar";
import Tabs from "./components/window/Tabs";

function App() {
  const [isMaximized, setIsMaximized] = useState(false);

  const updateIsWindowMaximized = useCallback(async () => {
    const resolvedPromise = await appWindow.isMaximized();
    setIsMaximized(resolvedPromise);
  }, []);

  useEffect(() => {
    updateIsWindowMaximized();
    let unlisten = undefined;
    const listen = async () => {
      unlisten = await appWindow.onResized(() => {
        updateIsWindowMaximized();
      });
    };
    listen();
    return () => unlisten && unlisten();
  }, [updateIsWindowMaximized]);

  const Layout = () => {
    return (
      <div className="flex flex-col h-full">
        <Titlebar />
        <PanelGroup direction="horizontal">
          <div className="flex w-full h-full min-w-0 custom-scrollbar">
            <Sidebar />
            {/* <PanelResizeHandle /> */}
            <Panel>
              <div className="flex flex-col h-full grow min-w-0">
                {/* <Tabs /> */}
                <Outlet />
              </div>
            </Panel>
          </div>
        </PanelGroup>

      </div >
    );
  };

  return (
    <div className={`h-full bg-primary-gray ${isMaximized ? 'rounded-none' : 'rounded-xl border-[1px] border-[#444444]'}`}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/schema/create" element={<SchemaBuilder />} />
          <Route path="*" element={<Missing />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;

// <div style={{ display: 'flex' }}>
// <PanelGroup direction="horizontal">
//   <Panel defaultSize={50} minSize={30}>
//     <FolderTree />
//   </Panel>
//   <Panel defaultSize={50} minSize={30}>
//     <Editor
//       height="90vh"
//       defaultLanguage="json"
//       defaultValue="// some comment"
//       onMount={handleEditorDidMount}
//     />
//   </Panel>
//   <PanelResizeHandle style={{
//     flex: '0 0 0.25rem',
//     // display: 'flex',
//     // justifyContent: 'stretch',
//     alignItems: 'stretch',
//     outline: 'none',
//     transition: 'background-color 0.2s linear',
//     backgroundColor: 'green'

//   }} />
//   <PanelResizeHandle />
//   <Panel defaultSize={50} minSize={20}>
//     <DnDFlow />
//   </Panel>
// </PanelGroup>