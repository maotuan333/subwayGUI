import React, { ReactElement, ReactNode, useEffect, useState } from "react";
import { Link, NavLink, matchPath, useLocation, useNavigate, useResolvedPath } from "react-router-dom";

interface SidebarItemProps {
  title: string;
  route: string;
  icon: ReactElement;
}

const SidebarItem = ({ route, icon }: SidebarItemProps) => {
  const location = useLocation();
  const [isActive, setActive] = useState(false);

  useEffect(() => {
    console.log(location.pathname)
    console.log(matchPath(route, location.pathname))
    if (matchPath(route, location.pathname)) {
      setActive(true);
    }
    else {
      setActive(false);
    }
  }, [location])

  const navigate = useNavigate();
  return (
    <button onClick={() => navigate(isActive ? '/' : route)} className={`flex h-12  items-center justify-center w-full ${isActive ? 'border-l-2 border-white' : ''}`}>
      {React.cloneElement(icon, { fill: isActive ? 'white' : '#a9a9a9' })}
    </button>
  );
};
export default SidebarItem;
