/// <reference types="vite-plugin-svgr/client" />
import { appWindow } from "@tauri-apps/api/window";
import styles from "./Titlebar.module.css";
import WindowMinimize from "../icons/WindowMinimize";
import WindowRestore from "../icons/WindowRestore";
import WindowClose from "../icons/WindowClose";
import { useCallback, useEffect, useState } from "react";
import Logo from "../../assets/svg/subway.svg?react";
import Tabs from "./Tabs";

function Titlebar() {
  const [isFocused, setIsFocused] = useState(false);

  const updateIsWindowFocused = useCallback(async () => {
    const resolvedPromise = await appWindow.isFocused();
    setIsFocused(resolvedPromise);
  }, []);

  useEffect(() => {
    updateIsWindowFocused();
    let unlisten = undefined;
    const listen = async () => {
      unlisten = await appWindow.onFocusChanged(() => {
        updateIsWindowFocused();
      });
    };
    listen();
    return () => unlisten && unlisten();
  }, [updateIsWindowFocused]);

  const toggleMaximized = () => {
    const fetchMaximizedStatus = async () => {
      const isMax = await appWindow.isMaximized();
      isMax ? appWindow.unmaximize() : appWindow.maximize();
    };
    fetchMaximizedStatus();
  };

  return (
    <div
      data-tauri-drag-region
      className={`w-full h-12 overflow-x-auto flex justify-between items-center border-b-[1px] border-seperator ${isFocused ? "bg-secondary-gray" : "bg-ternary-gray"}`}
    >
      <div className="h-full flex items-center justify-center">
        <div
          data-tauri-drag-region
          className="bg-primary-gray flex items-center justify-center w-12 border-r-[1px] border-seperator h-full"
        >
          <Logo data-tauri-drag-region width={40} height={40} />
        </div>
        <div className="h-full">
          <Tabs />
        </div>
      </div>
      <div className={`${styles.WindowButtonGroup} flex items-center h-full`}>
        <button
          className={styles.WindowButton}
          onClick={() => appWindow.minimize()}
        >
          <WindowMinimize width="1.25rem" height="0.65rem" fill="#BCBCBC" />
        </button>
        <button
          className={styles.WindowButton}
          onClick={async () => toggleMaximized()}
        >
          <WindowRestore width="1.25rem" height="1rem" fill="#BCBCBC" />
        </button>
        <button
          className={`${styles.WindowButton} hover:!bg-red-600`}
          onClick={() => appWindow.close()}
        >
          <WindowClose width="1.25rem" height="1.25rem" fill="#BCBCBC" />
        </button>
      </div>
    </div>
  );
}

export default Titlebar;
