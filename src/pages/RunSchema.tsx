/// <reference types="vite-plugin-svgr/client" />
import { PanelGroup } from "react-resizable-panels";
import { useMonaco } from "@monaco-editor/react";
import { useEffect, useRef, useState } from "react";
import DnDFlow from "../components/canvas/ReactFlowDnd";
import BlocksIcon from "../assets/svg/blocks.svg?react";
import ValidationIcon from "../assets/svg/validation.svg?react";
import ObjectIcon from "../assets/svg/object.svg?react";
import FunctionIcon from "../assets/svg/function.svg?react";
import styles from "./RunSchema.module.css";
import { ReactFlowProvider } from "reactflow";
import DraggableNode from "../components/canvas/DraggableItem";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "../components/@shadcn/ui/collapsible";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "../components/@shadcn/ui/resizable";
import { ChevronDown, Code } from "lucide-react";
import { ReactFlowContext } from "../contexts/ReactFlowContext";
import { createRFStore } from "../stores/RFStore";
import { invoke } from '@tauri-apps/api/tauri';
import path from 'path';

import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


function RunSchema() {
  const flowRefs = useRef([]);
  const editorRef = useRef(null);
  const monaco = useMonaco();
  flowRefs.current = [];
  // TODO How are we gonna pass in backend info
  const [subways, setSubways] = useState([]);

  // const { screenToFlowPosition, setViewport, setCenter } = useReactFlow();

  useEffect(() => {
    if (monaco) {
      monaco.editor.defineTheme("my-theme", {
        base: "vs",
        inherit: true,
        rules: [],
        colors: {
          "editor.background": "#000000",
        },
      });
    }
  }, [monaco]);

  function handleEditorDidMount(editor, _) {
    editorRef.current = editor;
  }

  const handleLoadClick = () => {
    // Call the Rust function and update the state with the returned data
    invoke('filematch',{directory: path.resolve(__dirname)}).then((response) => {
      const data = JSON.parse(response); // Assuming the response is a JSON string
      console.log(data)
      setSubways(data); // Update the state with the returned data
    }).catch((error) => {
      console.error('Error calling filematch:', error);
    });
  };

  const addToRefs = (el) => {
    if (el && !flowRefs.current.includes(el)) {
      flowRefs.current.push(el);
    }
    console.log(flowRefs.current);
  };

  return (
    <>
      <div
        id="schema-navbar"
        className=" justify-center items-center bg-primary-gray w-full py-2 min-h-12 border-b-[1px] border-seperator flex px-4"
      >
        <h6 className="text-md font-base">New Run</h6>
        <div className="ml-auto flex items-center gap-3">
          {/* @ts-ignore */}
          <button
            className="p-2 rounded-md hover:cursor-pointer hover:bg-white/[0.4]"
            onClick={() =>
              {handleLoadClick()
              flowRefs.current.map((el) => el.loadSchema("example.yaml"))
              }
            }
          >
            <Code size={14} className="hover:cursor-pointer" />
          </button>
          <button className="px-2 py-1 rounded-md hover:cursor-pointer text-sm bg-blue-500 hover:bg-blue-400">
            Load Schema
          </button>
        </div>
      </div>

      <ReactFlowProvider>
        <PanelGroup direction="horizontal">
          <div className="min-w-[15rem] lg:min-w-[15rem] xl:min-w-[20rem] border-r-[1px] border-seperator bg-primary-gray">
            <Collapsible defaultOpen={true}>
              <div
                className={`${styles["dnd-item-collapsible"]} border-seperator`}
              >
                <CollapsibleTrigger asChild>
                  <div
                    className={`${styles["dnd-item-collapsible-header"]} p-4 justify-between`}
                  >
                    <div className="flex items-center gap-2">
                      <BlocksIcon height={20} width={20} />
                      <h5 className="text-[15px] font-medium">Objects</h5>
                    </div>
                    <ChevronDown className="h-4 w-4 group-data-[state=open]:animate-spin" />
                  </div>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <div
                    className={`${styles["dnd-item-collapisble-content"]} grid gap-x-2 gap-y-2 px-4 pb-4`}
                  >
                    <DraggableNode
                      background="#4B8BF3"
                      nodeType="schemaNode"
                      label={"Input"}
                      Icon={<ObjectIcon height={24} width={24} />}
                    />
                    <DraggableNode
                      background="#12B368"
                      nodeType="input"
                      label={"Validation"}
                      Icon={<ValidationIcon height={24} width={24} />}
                    />
                    <DraggableNode
                      background="#8A3FFC"
                      nodeType="functionNode"
                      label={"Function"}
                      Icon={<FunctionIcon height={24} width={24} />}
                    />
                  </div>
                </CollapsibleContent>
              </div>
            </Collapsible>
          </div>
          <ResizablePanelGroup direction="vertical" style={{ height: "100vh" }}>
            {subways.map((item, index) => {
              const store = createRFStore(`${index}`)
              return (
                <>
                  <ResizablePanel maxSize={30} minSize={15}>
                    <p>
                      {item}
                    </p>
                    <ReactFlowContext.Provider value={store} key={index}>
                      <DnDFlow ref={addToRefs} initialSchema="example.yaml"/>
                    </ReactFlowContext.Provider>
                  </ResizablePanel>
                  <ResizableHandle />
                </>
              );
            })}
            <ResizablePanel style={{ flex: "1 1 auto" }} />
          </ResizablePanelGroup>
        </PanelGroup>
      </ReactFlowProvider>
    </>
  );
}

export default RunSchema;
