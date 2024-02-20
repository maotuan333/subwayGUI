/// <reference types="vite-plugin-svgr/client" />
import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";
import { persist } from "zustand/middleware";
import NewTabIcon from "../assets/svg/new-tab-icon.svg?react";
import SchemaBuilderIcon from "../assets/svg/schema-builder-icon.svg?react";

type Tab = {
  id: string;
  label: string;
  route: string;
  active: boolean;
};

interface TabState {
  tabs: Tab[];
  addTab: (route: string) => void;
  removeTab: (id: string) => void;
  setActive: (id: string) => void;
  getActive: () => Tab;
}

const RouteToTabMap = {
  "/": () => ({
    id: uuidv4(),
    label: "New page",
    route: "/",
    active: true,
  }),
  "/schema/create": () => ({
    id: uuidv4(),
    label: "Schema Builder",
    route: "/schema/create",
    active: true,
  }),
};

export const TabToIcon = {
  "/": <NewTabIcon className="min-w-[16px]" />,
  "/schema/create": <SchemaBuilderIcon className="min-w-[16px]" />,
};

export const useTabStore = create<TabState>()(
  persist(
    (set, get) => ({
      // initial state
      tabs: [RouteToTabMap["/"]()],
      addTab: (route: string) => {
        set((state) => {
          console.log();
          return {
            tabs: [
              ...state.tabs
                .filter((tab) => tab.route !== "/")
                .map((tab) => ({ ...tab, active: false })),
              RouteToTabMap[route](),
            ],
          };
        });
      },
      removeTab: (id) => {
        set((state) => {
          const openTabs = state.tabs.filter((tab) => tab.id !== id);
          if (openTabs.length == 0) {
            openTabs.push(RouteToTabMap["/"]());
          }
          if (openTabs.filter((tab) => tab.active == true).length == 0) {
            openTabs[0].active = true;
          }
          return {
            tabs: openTabs,
          };
        });
      },
      setActive: (id) => {
        set((state) => ({
          tabs: state.tabs.map((tab) =>
            tab.id === id
              ? { ...tab, active: true }
              : { ...tab, active: false },
          ),
        }));
      },
      getActive: () => {
        const tabs = get().tabs;
        return tabs.find((obj) => obj.active === true);
      },
    }),
    {
      name: "tab-storage",
    },
  ),
);
