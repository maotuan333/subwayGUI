import { useCallback, useContext, useEffect, useRef, useState } from "react";
import ReactFlow, {
  addEdge,
  Background,
  BackgroundVariant,
  Controls,
  useOnSelectionChange,
  Node,
  useStoreApi,
  getIncomers,
  getOutgoers,
  getConnectedEdges
} from "reactflow";
import "reactflow/dist/style.css";

import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../../components/@shadcn/ui/tabs"


import "./index.css";
import SchemaNode from "./Nodes/SchemaNode";
import TextUpdaterNode from "./Nodes/TextUpdaterNode";
import FunctionNode from "./Nodes/FunctionNode";
import { useRFContext } from "../../contexts/ReactFlowContext";
import { NodeData } from "~/stores/RFStore";
import NodeOptionsEdge from "./Edges/NodeOptionsEdge";


const nodeTypes = { textUpdater: TextUpdaterNode, schemaNode: SchemaNode, functionNode: FunctionNode };
const edgeTypes = { addNodeOptions: NodeOptionsEdge }

const AddNodeOnEdgeDrop = () => {
  const rfApiStore = useStoreApi();
  const { addSelectedNodes } = rfApiStore.getState();
  const { getId, nodes, setNodes, onNodesChange, edges, setEdges, onEdgesChange } = useRFContext((s) => s)
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

          const remainingEdges = acc.filter((edge) => !connectedEdges.includes(edge));

          const createdEdges = incomers.flatMap(({ id: source }) =>
            outgoers.map(({ id: target }) => ({ id: `${source}->${target}`, source, target }))
          );

          return [...remainingEdges, ...createdEdges];
        }, edges)
      );
    },
    [nodes, edges]
  );
  useOnSelectionChange({
    onChange: ({ nodes, edges }) => {
      setSelectedNodes(nodes.map((node) => node.id));
      setSelectedEdges(edges.map((edge) => edge.id));
    },
  });

  const onConnect = useCallback(
    (connection) => {
      console.log(connection)
      const edge = { ...connection, type: 'addNodeOptions' };
      setEdges((eds) => addEdge(edge, eds));
    },
    [setEdges],
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
          label: `File Pattern`
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
      <div className="wrapper w-full h-full bg-[#1A1A1C]" ref={reactFlowWrapper}>
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
      {
        selectedNodes.length > 0 ?
          <div className="bg-red-200 dark:bg-primary-gray h-full w-[40rem]">
            {/* <div>
              <p>{nodes.find((node) => node.id == selectedNodes[0])?.data?.label}</p>
              <p>Selected edges: {selectedEdges.join(', ')}</p>
            </div> */}
            <h1 className="">Properties</h1>
          </div>
          : ''
      }
    </>
  );
};

export default () => (
  <AddNodeOnEdgeDrop />
);
