/// <reference types="vite-plugin-svgr/client" />
import { appWindow } from "@tauri-apps/api/window";
import styles from "./Titlebar.module.css";
import WindowMinimize from "../icons/WindowMinimize";
import WindowRestore from "../icons/WindowRestore";
import WindowClose from "../icons/WindowClose";
import { useCallback, useEffect, useState } from "react";
import Logo from '../../assets/svg/subway.svg?react'

function Titlebar() {

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
    const toggleMaximized = () => {
        const fetchMaximizedStatus = async () => {
            const isMax = await appWindow.isMaximized();
            setIsMaximized(!isMax);
            isMax ? appWindow.unmaximize() : appWindow.maximize();
        };
        fetchMaximizedStatus();
    }

    return (
        <div className={`h-full bg-[#1E1E1E] ${isMaximized ? 'rounded-none' : 'rounded-xl border-[1px] border-[#444444]'}`}>
            <div data-tauri-drag-region className={`w-full bg-[#1E1E1E] flex justify-between items-center 
            ${isMaximized ? 'rounded-none' : 'rounded-t-xl'}`}>
                <div data-tauri-drag-region className="">
                    <Logo data-tauri-drag-region width={32} height={32} />
                </div>
                <div className={`${styles.WindowButtonGroup} flex`}>
                    <button className={styles.WindowButton} onClick={() => appWindow.minimize()}>
                        <WindowMinimize width="1.25rem" height="0.65rem" fill="#BCBCBC" />
                    </button>
                    <button className={styles.WindowButton} onClick={async () => toggleMaximized()}>
                        <WindowRestore width="1.25rem" height="1rem" fill="#BCBCBC" />
                    </button>
                    <button className={`${styles.WindowButton} hover:!bg-red-600`} onClick={() => appWindow.close()}>
                        <WindowClose width="1.25rem" height="1.25rem" fill="#BCBCBC" />
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Titlebar;
