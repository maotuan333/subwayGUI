import { useCallback, useEffect, useRef, useState } from "react";
import ReactFlow, {
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow,
  ReactFlowProvider,
  Background,
  BackgroundVariant,
  Controls,
  useOnSelectionChange,
} from "reactflow";
import "reactflow/dist/style.css";

import "./index.css";
import SchemaNode from "./Nodes/SchemaNode";
import TextUpdaterNode from "./Nodes/TextUpdaterNode";
import FunctionNode from "./Nodes/FunctionNode";

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
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [selectedEdges, setSelectedEdges] = useState([]);

  useOnSelectionChange({
    onChange: ({ nodes, edges }) => {
      setSelectedNodes(nodes.map((node) => node.id));
      setSelectedEdges(edges.map((edge) => edge.id));
    },
  });

  useEffect(() => {
    console.log(nodes[selectedNodes[0]])
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

      // reactFlowInstance.project was renamed to reactFlowInstance.screenToFlowPosition
      // and you don't need to subtract the reactFlowBounds.left/top anymore
      // details: https://reactflow.dev/whats-new/2023-11-10
      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX,
        y: event.clientY,
      });
      const newNode = {
        id: getId(),
        type,
        position,
        data: { label: `${type} node` },
      };

      setNodes((nds) => nds.concat(newNode));
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
              <p>Selected nodes: {selectedNodes.join(', ')}</p>
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
