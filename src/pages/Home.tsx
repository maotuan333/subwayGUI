/// <reference types="vite-plugin-svgr/client" />
import styles from "./Home.module.css";
import PlusIcon from '../assets/svg/plus.svg?react'
import { useNavigate } from "react-router-dom";

function Home() {

    const navigate = useNavigate();

    return (
        <div className={`${styles.Container} h-full gap-6`}>
            <button className={`${styles.ActionButton} bg-[#0C8CE9]`} onClick={() => navigate('/schema/create')}>
                <div className="p-2 bg-[#0A6DC2] rounded-3xl">
                    <PlusIcon width={20} height={20} />
                </div>
                <h1 className="font-sans font-semibold">Schema Builder</h1>
            </button>
            <button className={`${styles.ActionButton} bg-[#9747FF]`}>
                <div className="p-2 bg-[#8638E5] rounded-3xl">
                    <PlusIcon width={20} height={20} />
                </div>
                <h1 className="font-sans font-semibold">Run a Subway</h1>
            </button>
        </div>
    );
}

export default Home;
