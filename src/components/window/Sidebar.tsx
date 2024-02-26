/// <reference types="vite-plugin-svgr/client" />
import SettingsGear from "../../assets/svg/setting-gear.svg?react";
import SettingsFolder from "../../assets/svg/sidebar-folder.svg?react";
import { Link, MemoryRouter, NavLink, Outlet, Route, Routes, UNSAFE_LocationContext } from "react-router-dom";
import SidebarItem from "./SidebarItems";
import FolderTree from "../folder-tree/FolderTree";

function Sidebar() {

  const Layout = () => {
    return (
      <div className="flex h-full">
        <div className="w-12 flex justify-between flex-col items-center h-full border-r-[1px] border-seperator">
          <div id="top-sidebar-icons" className="w-full h-12">
            <SidebarItem title="File View" route="folder" icon={<SettingsFolder width={30} height={30} />} />
          </div>
          <div id="bottom-sidebar-icons" className="w-full h-12">
            <SidebarItem title="Settings" route="settings" icon={<SettingsGear width={30} height={30} />} />
          </div>
        </div>
        <div className="bg-[#252526]">
          <Outlet />
        </div>
      </div>
    )
  }

  return (
    <UNSAFE_LocationContext.Provider value={null}>
      <MemoryRouter >
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="folder" element={<FolderTree />} />
            <Route path="settings" element={<div >asdasdhkajskdhjasdjhsaj</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    </UNSAFE_LocationContext.Provider >
  );
}

export default Sidebar;
