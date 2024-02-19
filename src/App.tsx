import { Routes, Route, Outlet } from "react-router-dom";
import SchemaBuilder from "./pages/SchemaBuilder";
import Missing from "./components/router/Missing";
import Home from "./pages/Home";
import Titlebar from "./components/window/Titlebar";
import { useCallback, useEffect, useState } from "react";
import { appWindow } from "@tauri-apps/api/window";
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
      <>
        <Titlebar />
        <Tabs />
        <div className="flex flex-col min-w-0 w-[100%] h-full">
          <Outlet />
        </div>
      </>
    );
  };

  return (
    <div
      className={`h-full bg-[#1E1E1E] overflow-hidden ${isMaximized ? "rounded-none" : "rounded-xl border-[1px] border-[#444444]"}`}
    >
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
