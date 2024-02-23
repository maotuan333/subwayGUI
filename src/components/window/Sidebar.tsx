/// <reference types="vite-plugin-svgr/client" />
import { appWindow } from "@tauri-apps/api/window";
import styles from "./Titlebar.module.css";
import WindowMinimize from "../icons/WindowMinimize";
import WindowRestore from "../icons/WindowRestore";
import WindowClose from "../icons/WindowClose";
import { useCallback, useEffect, useState } from "react";
import Logo from "../../assets/svg/subway.svg?react";
import Tabs from "./Tabs";
import FolderTree from "../../components/folder-tree/FolderTree";
import SettingsGear from "../../assets/svg/setting-gear.svg?react";

function Sidebar() {
  return (
    <div className="w-fit flex flex-col h-full bg-primary-gray border-r-[1px] border-seperator py-3">
      <FolderTree />
      <SettingsGear width={32} height={32} />
    </div>
  );
}

export default Sidebar;
