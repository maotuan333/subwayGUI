/// <reference types="vite-plugin-svgr/client" />
import styles from "./Tabs.module.css";
import PlusIcon from '../../assets/svg/plus.svg?react'
import { useTabStore } from "../../stores/tabs";
import NewTabIcon from '../../assets/svg/new-tab-icon.svg?react'
import CloseTabIcon from '../../assets/svg/close.svg?react'

function Tabs() {

    const { addTab, removeTab, setActive, tabs } = useTabStore();

    // 2D2D2D
    // 1E1E1E
    return (
        <div className={`${styles.TabTrack} h-10 flex items-center overflow-x-auto overflow-y-hidden`}>
            {
                tabs.map(tab => {
                    console.log(tab)
                    return (
                        <div key={tab.id} className={`group flex h-full items-center border-r-[1px] border-[#1E1E1E] gap-2 px-2 pr-3 
                                font-sans ${tab.active ? 'bg-[#1E1E1E] ' : 'bg-[#2D2D2D]'} hover:cursor-pointer min-w-[8rem]  overflow`}
                            onClick={() => !tab.active ? setActive(tab.id) : null}
                        >
                            <NewTabIcon className="min-w-[16px]" />
                            <h6 className="text-[12px] font-semibold truncate">{tab.label} ({tab.id})</h6>
                            <button className={`p-1 hover:bg-[#464646] rounded-md ${!tab.active ? 'invisible group-hover:visible' : ''}`}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    removeTab(tab.id)
                                }}
                            >
                                <CloseTabIcon />
                            </button>
                        </div>
                    )
                })
            }
            <button className="p-3 h-full hover:bg-[#2D2D2D]" onClick={() => addTab("/new", "New page")}>
                <PlusIcon />
            </button>
        </div>
    );
}

export default Tabs;
