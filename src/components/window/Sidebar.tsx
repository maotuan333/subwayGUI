/// <reference types="vite-plugin-svgr/client" />
// import SettingsGear from "../../assets/svg/setting-gear.svg?react";
import SettingsFolder from "../../assets/svg/sidebar-folder.svg?react";
import { Link, MemoryRouter, NavLink, Outlet, Route, Routes, UNSAFE_LocationContext } from "react-router-dom";
import SidebarItem from "./SidebarItems";
import FolderTree from "../folder-tree/FolderTree";
import { Panel, PanelResizeHandle } from "react-resizable-panels";
import { MoonStar } from "lucide-react";

function Sidebar() {

  const Layout = () => {
    return (

      <div className="flex h-full">
        <div className="w-12 flex justify-between flex-col items-center h-full border-seperator">
          <div id="top-sidebar-icons" className="w-full h-12">
            <SidebarItem title="File View" route="folder" icon={<SettingsFolder width={30} height={30} />} />
          </div>
          <div id="bottom-sidebar-icons" className="w-full h-12">
            <div className="h-12 flex items-center justify-center">
              <MoonStar color="#a9a9a9" />
            </div>
          </div>
        </div>
        <div className="bg-[#252526] border-r-[1px] border-seperator">
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
