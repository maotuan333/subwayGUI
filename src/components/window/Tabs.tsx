/// <reference types="vite-plugin-svgr/client" />
import styles from "./Tabs.module.css";
import PlusIcon from '../../assets/svg/plus.svg?react'
import CloseTabIcon from '../../assets/svg/close.svg?react'
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TabToIcon, useTabStore } from "../../stores/tabs";

function Tabs() {

    const navigate = useNavigate();

    const { addTab, removeTab, setActive, getActive, tabs } = useTabStore();
    useEffect(() => {
        console.log(tabs)
        const activeTab = getActive();
        if (activeTab) {
            navigate(activeTab.route);
        }
    }, [tabs, navigate, getActive]);

    // 2D2D2D
    // 1E1E1E
    return (
        <div className={`${styles.TabTrack} h-10 flex items-center overflow-x-auto overflow-y-hidden`}>
            {
                tabs.map(tab => {
                    return (
                        <div key={tab.id} className={`group flex h-full items-center border-r-[1px] border-[#1E1E1E] gap-2 px-2 pr-3 
                                font-sans ${tab?.active ? 'bg-[#1E1E1E] ' : 'bg-[#2D2D2D]'} hover:cursor-pointer min-w-[8rem] overflow justify-between`}
                            onClick={() => {
                                !tab?.active ? setActive(tab.id) : null;
                            }}
                        >
                            <div className="flex items-center gap-1.5">
                                {TabToIcon[tab.route]}
                                <h6 className="text-[12px] font-semibold truncate">{tab.label}</h6>
                            </div>
                            <button className={`p-1 hover:bg-[#464646] rounded-md ${!tab?.active ? 'invisible group-hover:visible' : ''}`}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    removeTab(tab.id);
                                }}
                            >
                                <CloseTabIcon />
                            </button>
                        </div>
                    )
                })
            }
            {
                getActive()?.route !== '/' ?
                    <button className="p-3 h-full hover:bg-[#2D2D2D]" onClick={() => {
                        addTab("/");
                    }}>

                        <PlusIcon />
                    </button>
                    : ''
            }
        </div>
    );
}

export default Tabs;
