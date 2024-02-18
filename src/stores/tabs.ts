import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";

type Tab = {
  id: string;
  label: string;
  route: string;
  active: boolean;
};

interface TabState {
  tabs: Tab[];
  addTab: (route: string, label: string) => void;
  removeTab: (id: string) => void;
  setActive: (id: string) => void;
}

export const useTabStore = create<TabState>((set) => ({
  // initial state
  tabs: [],
  // methods for manipulating state
  addTab: (route: string, label: string) => {
    set((state) => ({
      tabs: [
        ...state.tabs.map((tab) => ({ ...tab, active: false })),
        {
          id: uuidv4(),
          label,
          route,
          active: true,
        } as Tab,
      ],
    }));
  },
  removeTab: (id) => {
    set((state) => {
      const openTabs = state.tabs.filter((tab) => tab.id !== id);
      if(openTabs.length != 0 && openTabs.filter((tab) => tab.active == true).length == 0) {
        openTabs[0].active = true;
      }
      return {
        tabs: openTabs
      };
    });
  },
  setActive: (id) => {
    set((state) => ({
      tabs: state.tabs.map((tab) =>
        tab.id === id ? { ...tab, active: true } : { ...tab, active: false }
      ),
    }));
  },
}));
