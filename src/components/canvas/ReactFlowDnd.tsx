import { useCallback, useContext, useEffect, useRef, useState } from "react";
import ReactFlow, {
  addEdge,
  Background,
  BackgroundVariant,
  Controls,
  useOnSelectionChange,
  Node,
  useStoreApi
} from "reactflow";
import "reactflow/dist/style.css";


import "./index.css";
import SchemaNode from "./Nodes/SchemaNode";
import TextUpdaterNode from "./Nodes/TextUpdaterNode";
import FunctionNode from "./Nodes/FunctionNode";
import { ReactFlowContext } from "../../contexts/ReactFlowContext";
import { useStore } from "zustand";
import { NodeData } from "~/stores/RFStore";


const initialNodes = [
  {
    id: "0",
    type: "schemaNode", //'input' for old version
    data: { label: "schema" },
    position: { x: 0, y: 100 },
  },
];

const nodeTypes = { textUpdater: TextUpdaterNode, schemaNode: SchemaNode, functionNode: FunctionNode };


let id = 1;
const getId = () => `${id++}`;

const AddNodeOnEdgeDrop = () => {
  const store = useContext(ReactFlowContext)
  const rfApiStore = useStoreApi();
  const { resetSelectedElements, addSelectedNodes } = rfApiStore.getState();
  if (!store) throw new Error('Missing ReactFlowContext.Provider in the tree');
  const { nodes, setNodes, onNodesChange, edges, setEdges, onEdgesChange } = useStore(store, (s) => s)
  // const edges = useStore(store, (s) => s.edges);
  const reactFlowWrapper = useRef(null);
  // const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  // const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [selectedEdges, setSelectedEdges] = useState([]);

  useOnSelectionChange({
    onChange: ({ nodes, edges }) => {
      console.log("changed")
      setSelectedNodes(nodes.map((node) => node.id));
      setSelectedEdges(edges.map((edge) => edge.id));
    },
  });

  useEffect(() => {
    console.log(selectedNodes[0])
    const selectedNode = nodes.find((node) => node.id == selectedNodes[0]);
    console.log(selectedNode)
  }, [selectedNodes])

  const onConnect = useCallback(
    (params) => { params['label'] = 'inputfile.txt'; console.log(params); setEdges((eds) => addEdge(params, eds)) },
    [],
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');

      // check if the dropped element is valid
      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      const newNode: Node<NodeData> = {
        id: getId(),
        type,
        position,
        data: {
          label: `${type} node`
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
      <div className="wrapper w-[80%] h-full bg-[#1A1A1C]" ref={reactFlowWrapper}>
        <ReactFlow
          maxZoom={1.25}
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
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
      {
        selectedNodes.length > 0 ?
          <div className="bg-red-200 h-full w-[25%]">
            <div>
              <p>{nodes.find((node) => node.id == selectedNodes[0]).data?.label}</p>
              <p>Selected edges: {selectedEdges.join(', ')}</p>
            </div>
          </div>
          : ''
      }
    </>
  );
};

export default () => (
  <AddNodeOnEdgeDrop />
);
