import styles from "./Home.module.css";

function Home() {
    return (
        <div className={styles.Container}>
            <button className={`${styles.ActionButton} bg-red-200`}>
            test
            </button>
        </div>
    );
}

export default Home;
