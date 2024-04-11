import {
  forwardRef,
  useCallback,
  useContext,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from "react";
import ReactFlow, {
  addEdge,
  Background,
  BackgroundVariant,
  Controls,
  useOnSelectionChange,
  Node,
  Edge,
  useStoreApi,
  getIncomers,
  getOutgoers,
  getConnectedEdges,
  isNode,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";

import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../../components/@shadcn/ui/tabs";
import YAML from "yaml";

import "./index.css";
import SchemaNode from "./Nodes/SchemaNode";
import TextUpdaterNode from "./Nodes/TextUpdaterNode";
import FunctionNode from "./Nodes/FunctionNode";
import { useRFContext } from "../../contexts/ReactFlowContext";
import NodeOptionsEdge from "./Edges/NodeOptionsEdge";
import { ChevronLeft, Code, Trash2, TrashIcon, X } from "lucide-react";
import NodePropertyForm from "../forms/NodePropertyForm";
import { CustomNodeData } from "../../types/RFNodes"; //okay ~ didn't work?
import { BaseDirectory, writeTextFile, readTextFile } from "@tauri-apps/api/fs";
import dagre from "dagre";
import React from "react";
const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const getLayoutedElements = (elements) => {
  dagreGraph.setGraph({ rankdir: "LR" });
  dagreGraph.graph.rankdir = "LR";

  console.log("set dagre graph");

  elements.forEach((el) => {
    if (isNode(el)) {
      dagreGraph.setNode(el.id, { label: el.label, pattern: el.pattern });
      console.log(`Added node: ${el.id}`);
    } else {
      dagreGraph.setEdge(el.source, el.target);
      console.log(`Added edge: ${el.source} -> ${el.target}`);
    }
  });

  dagre.layout(dagreGraph);
  console.log("layout dagre graph");
  console.log(dagreGraph);

  return elements.map((el) => {
    if (isNode(el)) {
      const nodeWithPosition = dagreGraph.node(el.id);
      console.log(el.id);
      console.log(nodeWithPosition);
      if (nodeWithPosition) {
        el.targetPosition = "left";
        el.sourcePosition = "right";
        el.position = {
          x: nodeWithPosition.x + Math.random() / 1000,
          y: nodeWithPosition.y,
        };
        console.log(el.position);
      } else {
        console.log(`Node with id ${el.id} not found in dagre graph.`);
      }
    }
    return el;
  });
};

const nodeTypes = {
  textUpdater: TextUpdaterNode,
  schemaNode: SchemaNode,
  functionNode: FunctionNode,
};
const edgeTypes = { addNodeOptions: NodeOptionsEdge };

const AddNodeOnEdgeDrop = forwardRef((props, ref) => {
  const rfApiStore = useStoreApi();
  const { addSelectedNodes } = rfApiStore.getState();
  const {
    getId,
    nodes,
    setNodes,
    onNodesChange,
    removeNode,
    edges,
    setEdges,
    onEdgesChange,
  } = useRFContext((s) => s);
  // @ts-ignore
  useImperativeHandle(ref, () => ({
    async saveSchema(filename) {
      const schemaData = YAML.stringify({
        nodes: nodes.map((node) => ({
          id: node.id,
          label: node.data.label,
          pattern: node.data?.extension || "",
          prefix: node.data?.prefix,
        })),
        edges: edges.map((edge) => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
        })),
      });
      console.log(schemaData);
      console.log(`subwayGUI-data/${filename}`);
      await writeTextFile(`subwayGUI-data/${filename}`, schemaData, {
        dir: BaseDirectory.Download,
      });
      console.log("saved");
    },
    async loadSchema(filename) {
      console.log("called");
      const schemaYAML = await readTextFile(`subwayGUI-data/${filename}`, {
        dir: BaseDirectory.Download,
      });
      console.log("read");
      const schemaData = YAML.parse(schemaYAML);
      console.log(schemaData);
      const parsedNodes: Node<CustomNodeData>[] = schemaData.nodes.map(
        (node) => ({
          id: node.id,
          type: node.label,
          data: {
            label: node.label,
            pattern: node.pattern, //suffix
            prefix: node.prefix, // prefix
          },
          position: { x: 0, y: 0 }, // do we need this
          sourcePosition: "right",
          targetPosition: "left",
        }),
      );
      console.log(parsedNodes);
      const parsedEdges: Edge[] = schemaData.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        animated: true,
        markerEnd: {
          type: MarkerType.ArrowClosed,
        },
      }));
      console.log(parsedEdges);
      const layoutedNodes = getLayoutedElements(parsedNodes);
      console.log(layoutedNodes);
      setNodes([...layoutedNodes]);
      setEdges([...parsedEdges]);
      reactFlowInstance.fitView();
      console.log(`read in subwaygui-data\\${filename}`);
    },
  }));

  // const edges = useStore(store, (s) => s.edges);
  const reactFlowWrapper = useRef(null);
  // const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  // const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [selectedEdges, setSelectedEdges] = useState([]);
  const onNodesDelete = useCallback(
    (deleted) => {
      setEdges(
        deleted.reduce((acc, node) => {
          const incomers = getIncomers(node, nodes, edges);
          const outgoers = getOutgoers(node, nodes, edges);
          const connectedEdges = getConnectedEdges([node], edges);

          const remainingEdges = acc.filter(
            (edge) => !connectedEdges.includes(edge),
          );

          const createdEdges = incomers.flatMap(({ id: source }) =>
            outgoers.map(({ id: target }) => ({
              id: `${source}->${target}`,
              source,
              target,
            })),
          );

          return [...remainingEdges, ...createdEdges];
        }, edges),
      );
    },
    [nodes, edges],
  );
  useOnSelectionChange({
    onChange: ({ nodes, edges }) => {
      setSelectedNodes(nodes.map((node) => node.id));
      setSelectedEdges(edges.map((edge) => edge.id));
      // setTimeout(reactFlowInstance.fitView, 200)
    },
  });

  const onConnect = useCallback(
    (connection) => {
      console.log(connection);
      const edge = { ...connection, type: "addNodeOptions" };
      setEdges((eds) => addEdge(edge, eds));
    },
    [setEdges],
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const type = event.dataTransfer.getData("application/reactflow");
      // check if the dropped element is valid
      if (typeof type === "undefined" || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      const newNode: Node<CustomNodeData> = {
        id: getId(),
        type,
        position,
        data: {
          label: `${type}`,
        },
      };
      setNodes((nodes) => nodes.concat(newNode));
      setTimeout(() => {
        addSelectedNodes([newNode.id]);
      }, 1);
    },
    [reactFlowInstance],
  );

  return (
    <>
      <div
        className="wrapper w-full h-full bg-[#1A1A1C]"
        ref={reactFlowWrapper}
      >
        <ReactFlow
          maxZoom={1.25}
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          edgeTypes={edgeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodesDelete={onNodesDelete}
          onConnect={onConnect}
          onInit={setReactFlowInstance}
          proOptions={{ hideAttribution: true }}
          onDrop={onDrop}
          onDragOver={onDragOver}
          fitView
        >
          <Background
            color="#323234"
            gap={25}
            size={3}
            variant={BackgroundVariant.Dots}
          />
          <Controls color="white" className="bg-white" />
        </ReactFlow>
      </div>
      {selectedNodes.length > 0 ? (
        <div className="bg-primary-gray h-full w-[40rem]">
          {/* <div>
              <p>{nodes.find((node) => node.id == selectedNodes[0])?.data?.label}</p>
              <p>Selected edges: {selectedEdges.join(', ')}</p>
            </div> */}
          <div className="px-4 flex h-14 items-center justify-between border-seperator border-b-[1px]">
            <div className="flex items-center gap-3">
              <div
                className="border-[0.5px] rounded-md p-1 hover:bg-white/[0.6]"
                onClick={() => {
                  addSelectedNodes([]);
                }}
              >
                <ChevronLeft className="hover:cursor-pointer" size={18} />
              </div>
              <h1 className="font-medium">Node Properties</h1>
            </div>
            <div className="flex items-center gap-2">
              {/* <div className=" p-2 rounded-md hover:cursor-pointer hover:bg-white/[0.4]">
                  <Code size={14} className="hover:cursor-pointer" />
                </div> */}
              <div
                className="p-2 rounded-md hover:cursor-pointer hover:bg-red-300/[0.4]"
                onClick={() =>
                  removeNode(
                    nodes.find((node) => node.id == selectedNodes[0])?.id,
                  )
                }
              >
                <Trash2 size={14} className="text-red-300" />
              </div>
            </div>
          </div>
          <div className="p-4">
            <NodePropertyForm />
          </div>
        </div>
      ) : (
        ""
      )}
    </>
  );
});

export default AddNodeOnEdgeDrop;

// // Running the pipeline when user clicks on a node
// // input to Run Subway
// "node_id_clicked": 5,
// "schema":
// [{
//   id: 1,
//   data: {
//     label: "SchemaNode",
//     pattern: "_data.npy",
//     prefix: "experimentx_",
//     parents: null,
//     children: 2
//   },
// },
// {
//   id: 2,
//   data: {
//     label: "FunctionNode",
//     pattern: "/fullpath/scriptToGenerateData.py",
//     prefix: null,
//     parents: 1,
//     children: 3
//   }, // backend runs in cli: python /fullpath/scriptToGenerateData.py experimentx_{sth}_data.npy {sth2}_output.npy
// },
// {
//   id: 3,
//   data: {
//     label: "SchemaNode",
//     pattern: "output.npy",
//     prefix: null,
//     parent: 2,
//     children: null
//   },
// }
// ]
