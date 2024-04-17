/// <reference types="vite-plugin-svgr/client" />
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import { Editor, useMonaco } from "@monaco-editor/react";
import { useEffect, useRef, useState } from "react";
import DnDFlow from "../components/canvas/ReactFlowDnd";
import BlocksIcon from "../assets/svg/blocks.svg?react";
import ValidationIcon from "../assets/svg/validation.svg?react";
import ObjectIcon from "../assets/svg/object.svg?react";
import FunctionIcon from "../assets/svg/function.svg?react";
import styles from "./RunSchema.module.css";
import ReactFlow, { Background, BackgroundVariant, Controls, ReactFlowProvider } from "reactflow";
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
import { ChevronDown, Code, Code2 } from "lucide-react";
import { ReactFlowContext } from "../contexts/ReactFlowContext";
import { createRFStore } from "../stores/RFStore";
import { invoke } from '@tauri-apps/api/tauri';
import path from 'path';
import { open } from "@tauri-apps/api/dialog";
import { readTextFile } from "@tauri-apps/api/fs";
import { Button } from "../components/@shadcn/ui/button";
import Sidebar from "../components/canvas/Sidebar";
import TextUpdaterNode from "../components/canvas/Nodes/TextUpdaterNode";
import SchemaNode from "../components/canvas/Nodes/SchemaNode";
import FunctionNode from "../components/canvas/Nodes/FunctionNode";
import RunSchemaNode from "../components/canvas/Nodes/RunSchemaNode";

// import { fileURLToPath } from 'url';
// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);


function RunSchema() {

  const [schemaPath, setSchemaPath] = useState("");
  const [schemaContent, setSchemaContent] = useState("");
  const [directoryPath, setDirectoryPath] = useState("");
  const [editorActive, setEditorActive] = useState(false);
  const [nodesGlobal, setNodesGlobal] = useState([]);

  function formatJSON(val = {}) {
    try {
      const res = JSON.parse(val);
      return JSON.stringify(res, null, 2)
    } catch {
      const errorJson = {
        "error": `非法返回${val}`
      }
      return JSON.stringify(errorJson, null, 2)
    }
  }

  const loadDirectory = async () => {
    try {
      const selectedPath = await open({
        multiple: false,
        title: "Open directory",
        directory: true
      });
      if (!selectedPath) return
      setDirectoryPath(selectedPath as string);
      console.log({ target_path: selectedPath, schema_path: schemaPath })
      const res: any = await invoke("find_matches", { targetPath: selectedPath, schemaPath: schemaPath })
      const matchData = res;
      const nodeData = JSON.parse(schemaContent)["nodes"];
      const nodes = []
      for (let i = 0; i < nodeData.length; i++) {
        console.log(nodeData[i])
        console.log(matchData[i])
        if (matchData[i] || !matchData[i]) {
          const newNode: any = {
            id: `${i}`,
            type: "runSchemaNode",
            position: {
              x: i * 300,
              y: 50,
            },
            data: {
              label: `File Pattern`,
              match: matchData[i]
            },
          };
          nodes.push(newNode)
        }
      }
      console.log(nodes)
      setNodesGlobal(nodes);
    } catch (err) {
      console.error(err);
    }

  }

  const runSubway = async () => {
    console.log({ target_path: directoryPath, schema_path: schemaPath })
    console.log(directoryPath)
    const res = await invoke("find_matches", { targetPath: directoryPath, schemaPath: schemaPath })
  }

  const nodeTypes = {
    textUpdater: TextUpdaterNode,
    runSchemaNode: RunSchemaNode,
    functionNode: FunctionNode,
  };

  const TestElement = () => {
    return (
      <ReactFlowProvider>
        <ReactFlow
          maxZoom={1.25}
          nodes={nodesGlobal}
          edges={[]}
          fitView
          nodeTypes={nodeTypes}

        >
          <Background
            color="#323234"
            gap={25}
            size={3}
            variant={BackgroundVariant.Dots}
          />
          <Controls color="white" className="bg-white" />
        </ReactFlow>
      </ReactFlowProvider>
    )
  }

  const loadSchema = async () => {
    try {
      const selectedPath = await open({
        multiple: false,
        title: "Open file",
        filters: [
          {
            name: 'Schema',
            extensions: ['json']
          }
        ]
      });
      if (!selectedPath) return
      setSchemaPath(selectedPath as string);
      const fileContent = await readTextFile(selectedPath as string);
      setSchemaContent(fileContent);
      setEditorActive(true);
    } catch (err) {
      console.error(err);
    }
  }

  function setEditorTheme(monaco: any) {
    monaco.editor.defineTheme('onedark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        {
          token: 'comment',
          foreground: '#5d7988',
          fontStyle: 'italic'
        },
        { token: 'constant', foreground: '#e06c75' }
      ],
      colors: {
        'editor.background': '#21252b'
      }
    });
  }

  return (
    <>
      <div
        id="schema-navbar"
        className=" justify-center items-center bg-primary-gray w-full py-2 min-h-12 border-b-[1px] border-seperator flex px-4"
      >
        <h6 className="text-md font-base">New Run <span className="text-xs">{schemaPath ? `(using ${schemaPath})` : ''}</span></h6>
        <div className="ml-auto flex items-center gap-3">
          <button
            onClick={() => setEditorActive(!editorActive)}
            className={`p-2 rounded-md hover:cursor-pointer ${editorActive ? 'bg-white/[0.4]' : 'hover:bg-white/[0.4]'}`}
          >
            <Code size={14} />
          </button>
          <button onClick={loadSchema} className="px-2 py-1 rounded-md hover:cursor-pointer text-sm bg-blue-500 hover:bg-blue-400">
            Load Schema
          </button>
          <button onClick={runSubway} className="px-2 py-1 rounded-md hover:cursor-pointer text-sm bg-blue-500 hover:bg-blue-400">
            Run Schema
          </button>
        </div>
      </div>
      {/* <div className="flex"> */}
      <PanelGroup direction="horizontal" className="flex">
        <Panel className="w-full" defaultSize={70}>
          <div className="w-full h-full">
            {!directoryPath
              ? <div className="h-full flex items-center justify-center"><Button onClick={loadDirectory} className="px-10 h-14 !text-xl !text-white !bg-blue-500 hover:!bg-blue-500/[0.8]">Open Directory</Button></div>
              : <TestElement />
            }
          </div>
        </Panel>
        <PanelResizeHandle />
        {
          editorActive ?
            <Panel defaultSize={30}>
              <div>
                <Editor
                  theme="vs-dark"
                  height="90vh"
                  defaultLanguage="json"
                  value={formatJSON(schemaContent)}
                />
              </div>
            </Panel>
            : ''
        }
      </PanelGroup>
      {/* </div> */}
    </>
  );
}

export default RunSchema;
