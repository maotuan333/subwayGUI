import React, { useState } from 'react';
import './MenuBar.css'; // Make sure to create and style your MenuBar.css
import { useTabStore } from "../../stores/tabs"; 
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const MenuBar = () => {
    const [showFileDropdown, setShowFileDropdown] = useState(false);
    const [showSettingsDropdown, setShowSettingsDropdown] = useState(false);
    const navigate = useNavigate();

    const toggleFileDropdown = () => setShowFileDropdown(prev => !prev);
    const toggleSettingsDropdown = () => setShowSettingsDropdown(prev => !prev);
    // Handler for clicking New Schema button
    // const handleNewSchema = (e) => {
    //     e.stopPropagation(); // Prevent event bubbling to parent elements
    
    //     addTab();
        
    //     // Navigate to the route of the new schema page
    //     // This assumes that you have imported the `useNavigate` hook from 'react-router-dom' 
    //     // and have initialized `navigate` in your component
    //     navigate("/schema/create/new");
    // };
    const { addTab, removeTab, setActive, getActive, tabs } = useTabStore();
    useEffect(() => {
        const activeTab = getActive();
        if (activeTab) {
        navigate(activeTab.route);
            }
    }, [tabs, navigate, getActive]);

    return (
        <nav className="menu-bar">
            <ul className="menu-list">
                <li className="menu-item" onClick={toggleFileDropdown}>
                    File
                    {showFileDropdown && (
                        <div className="dropdown">
                            <button onClick={() => {addTab("/");}}>New Schema</button>
                            <button>Open Schema</button>
                            <button>Save Schema</button>
                            {/* ... other options ... */}
                        </div>
                    )}
                </li>
                <li className="menu-item" onClick={toggleSettingsDropdown}>
                    Setting
                    {showSettingsDropdown && (
                        <div className="dropdown">
                            {/* Settings options here */}
                        </div>
                    )}
                </li>
            </ul>
        </nav>
    );
};

export default MenuBar;
