/// <reference types="vite-plugin-svgr/client" />
import { appWindow } from "@tauri-apps/api/window";
import styles from "./Titlebar.module.css";
import WindowMinimize from "../icons/WindowMinimize";
import WindowRestore from "../icons/WindowRestore";
import WindowClose from "../icons/WindowClose";
import { useCallback, useEffect, useState } from "react";
import Logo from '../../assets/svg/subway.svg?react'

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
            })
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
    }

    return (
            <div data-tauri-drag-region className={`w-full flex justify-between items-center ${isFocused ? 'bg-[#3C3C3C]' : 'bg-[#323233]'}`}>
                <div data-tauri-drag-region className="ml-0.5">
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
    );
}

export default Titlebar;
