/// <reference types="vite-plugin-svgr/client" />
import { PanelGroup } from "react-resizable-panels";
import { useMonaco } from "@monaco-editor/react";
import { useEffect, useRef } from "react";
import DnDFlow from "../components/canvas/ReactFlowDnd";
import BlocksIcon from "../assets/svg/blocks.svg?react";
import EditPropertiesIcon from "../assets/svg/wrench.svg?react";
import ValidationIcon from "../assets/svg/validation.svg?react";
import ObjectIcon from "../assets/svg/object.svg?react";
import FunctionIcon from "../assets/svg/function.svg?react";
import styles from "./SchemaBuilder.module.css";
import { ReactFlowProvider } from "reactflow";
import DraggableNode from "../components/canvas/DraggableItem";

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

  return (
    <>
      <div
        id="schema-navbar"
        className="bg-primary-gray w-full py-2 min-h-12 border-b-[1px] border-seperator flex items-center px-4 justify-between"
      >
        <h6 className="text-lg font-medium py-2">Schema Builder</h6>
      </div>

      <ReactFlowProvider >
        <PanelGroup direction="horizontal">
          <div className="w-[30%] border-r-[1px] border-seperator">
            <div className={`${styles['dnd-item-collapsible']} border-seperator p-4`}>
              <div className={`${styles['dnd-item-collapsible-header']} gap-2`}>
                <BlocksIcon height={20} width={20} />
                <h5 className="text-[15px] font-medium">Objects</h5>
              </div>
              <div className="dnd-item-collapsible-content mt-4 grid grid-cols-2 gap-2">
                <DraggableNode background="#8A3FFC" nodeType='textUpdater' label={'Input'} Icon={<ObjectIcon height={24} width={24} />} />
                <DraggableNode background="#12B368" nodeType='input' label={'Validation'} Icon={<ValidationIcon height={24} width={24} />} />
                <DraggableNode background="#4B8BF3" nodeType='input' label={'Function'} Icon={<FunctionIcon height={24} width={24} />} />
              </div>
            </div>
            <div className={`${styles['dnd-item-collapsible']} border-seperator p-4`}>
              <div className={`${styles['dnd-item-collapsible-header']} gap-1`}>
                <EditPropertiesIcon height={24} width={24} />
                <h5 className="text-[15px] font-medium">Object Properties</h5>
              </div>
            </div>
          </div>
          <div className="w-full">
            <DnDFlow />
          </div>
        </PanelGroup >
      </ReactFlowProvider >
    </>
  );
}

export default SchemaBuilder;
