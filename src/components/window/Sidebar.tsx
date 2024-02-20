/// <reference types="vite-plugin-svgr/client" />
import { appWindow } from "@tauri-apps/api/window";
import styles from "./Titlebar.module.css";
import WindowMinimize from "../icons/WindowMinimize";
import WindowRestore from "../icons/WindowRestore";
import WindowClose from "../icons/WindowClose";
import { useCallback, useEffect, useState } from "react";
import Logo from "../../assets/svg/subway.svg?react";
import Tabs from "./Tabs";
import SettingsGear from "../../assets/svg/setting-gear.svg?react";

function Sidebar() {
  return (
    <div className="w-12 flex justify-center items-end h-full bg-primary-gray border-r-[1px] border-seperator py-3">
      <SettingsGear width={32} height={32} />
    </div>
  );
}

export default Sidebar;
