/// <reference types="vite-plugin-svgr/client" />
import { PanelGroup } from "react-resizable-panels";
import { useMonaco } from "@monaco-editor/react";
import { useEffect, useRef } from "react";
import DnDFlow from "../components/canvas/ReactFlowDnd";
import BlocksIcon from "../assets/svg/blocks.svg?react";
import ValidationIcon from "../assets/svg/validation.svg?react";
import ObjectIcon from "../assets/svg/object.svg?react";
import FunctionIcon from "../assets/svg/function.svg?react";
import styles from "./SchemaBuilder.module.css";
import { ReactFlowProvider } from "reactflow";
import DraggableNode from "../components/canvas/DraggableItem";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "../components/@shadcn/ui/collapsible";
import { ChevronDown } from "lucide-react"
import { ReactFlowContext } from "../contexts/ReactFlowContext";
import { createRFStore } from "../stores/RFStore";

function SchemaBuilder() {
  const editorRef = useRef(null);
  const monaco = useMonaco();
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
  const store = useRef(createRFStore()).current;


  return (
    <>
      <div
        id="schema-navbar"
        className=" justify-center items-center bg-primary-gray w-full py-2 min-h-12 border-b-[1px] border-seperator flex px-4"
      >
        <h6 className="text-md font-base">New Schema Builder</h6>
      </div>

      <ReactFlowProvider >
        <PanelGroup direction="horizontal">
          <div className="min-w-[15rem] lg:min-w-[15rem] xl:min-w-[20rem] border-r-[1px] border-seperator bg-primary-gray">
            <Collapsible defaultOpen={true}>
              <div className={`${styles['dnd-item-collapsible']} border-seperator`}>
                <CollapsibleTrigger asChild>
                  <div className={`${styles['dnd-item-collapsible-header']} p-4 justify-between`}>
                    <div className="flex items-center gap-2">
                      <BlocksIcon height={20} width={20} />
                      <h5 className="text-[15px] font-medium">Objects</h5>
                    </div>
                    <ChevronDown className="h-4 w-4 group-data-[state=open]:animate-spin" />
                  </div>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <div className={`${styles['dnd-item-collapisble-content']} grid gap-x-2 gap-y-2 px-4 pb-4`}>
                    <DraggableNode background="#4B8BF3" nodeType='schemaNode' label={'Input'} Icon={<ObjectIcon height={24} width={24} />} />
                    <DraggableNode background="#12B368" nodeType='input' label={'Validation'} Icon={<ValidationIcon height={24} width={24} />} />
                    <DraggableNode background="#8A3FFC" nodeType='functionNode' label={'Function'} Icon={<FunctionIcon height={24} width={24} />} />
                  </div>
                </CollapsibleContent>
              </div>
            </Collapsible>
          </div>
          <ReactFlowContext.Provider value={store}>
            <DnDFlow />
          </ReactFlowContext.Provider>
        </PanelGroup >
      </ReactFlowProvider >
    </>
  );
}

export default SchemaBuilder;
