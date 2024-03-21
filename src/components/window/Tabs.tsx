/// <reference types="vite-plugin-svgr/client" />
import styles from "./Tabs.module.css";
import PlusIcon from "../../assets/svg/plus.svg?react";
import CloseTabIcon from "../../assets/svg/close.svg?react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TabToIcon, useTabStore } from "../../stores/tabs";

function Tabs() {
  const navigate = useNavigate();

  const { addTab, removeTab, setActive, getActive, tabs } = useTabStore();
  useEffect(() => {
    const activeTab = getActive();
    if (activeTab) {
      navigate(activeTab.route);
    }
  }, [tabs, navigate, getActive]);

  // 2D2D2D
  // 1E1E1E
  return (
    <div className={`h-12 custom-scrollbar`}>
      <div className="flex">

        <div
          className={`${styles.TabTrack} min-h-12 flex items-center custom-scrollbar`}
        >
          {tabs.map((tab) => {
            return (
              <div
                key={tab.id}
                className={`group flex min-w-[170px] flex h-12 z-[50] items-center border-r-[1px] border-primary-gray gap-2 px-2 pr-3 
                                z-50 font-system ${tab?.active ? "bg-primary-gray " : ""} hover:cursor-pointer min-h-full overflow justify-between`}
                onClick={() => {
                  !tab?.active ? setActive(tab.id) : null;
                }}
              >
                <div className="flex items-center gap-1.5">
                  {TabToIcon(tab.route)}
                  <h6 className="text-[12px] font-semibold truncate max-w-[6rem] ">
                    {tab.label}
                  </h6>
                </div>
                <button
                  className={`p-1 hover:bg-[#464646] rounded-md ${!tab?.active ? "group-hover:visible" : ""}`}
                  onClick={(e) => {
                    e.stopPropagation();
                    removeTab(tab.id);
                  }}
                >
                  <CloseTabIcon />
                </button>
              </div>
            );
          })}
        </div>
        {getActive()?.route !== "/" ? (
          <button
            className="px-3 h-12 bg-transparent hover:bg-primary-gray/[0.4]"
            onClick={() => {
              addTab("/");
            }}
          >
            <PlusIcon />
          </button>
        ) : (
          ""
        )}

      </div>
    </div>
  );
}

export default Tabs;
