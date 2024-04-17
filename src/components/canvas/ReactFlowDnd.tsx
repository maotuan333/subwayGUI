import {
  forwardRef,
  useCallback,
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
import YAML from "yaml";
import "./index.css";
import SchemaNode from "./Nodes/SchemaNode";
import TextUpdaterNode from "./Nodes/TextUpdaterNode";
import FunctionNode from "./Nodes/FunctionNode";
import { useRFContext } from "../../contexts/ReactFlowContext";
import NodeOptionsEdge from "./Edges/NodeOptionsEdge";
import { ChevronLeft, Trash2 } from "lucide-react";
import NodePropertyForm from "../forms/NodePropertyForm";
import { CustomNodeData } from "../../types/RFNodes"; //okay ~ didn't work?
import { BaseDirectory, writeTextFile, readTextFile } from "@tauri-apps/api/fs";
import dagre from "dagre";
import { open, save } from "@tauri-apps/api/dialog";
import { Button } from "../@shadcn/ui/button";
import { invoke } from "@tauri-apps/api/tauri";

const getLayoutedElements = (elements) => {

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: "LR" });

  elements.forEach((el) => {
    if (isNode(el)) {
      dagreGraph.setNode(el.id, { label: el.label, pattern: el.pattern });
    } else {
      dagreGraph.setEdge(el.source, el.target);
    }
  });

  dagre.layout(dagreGraph);

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



interface AddNodeOnEdgeDropProps {
  initialSchema?: string; // Adjust the type as needed
  // Other props...
}


const AddNodeOnEdgeDrop = forwardRef((props: AddNodeOnEdgeDropProps, ref) => {
  const rfApiStore = useStoreApi();
  const { initialSchema } = props;
  const { addSelectedNodes } = rfApiStore.getState();
  const {
    getId,
    nodes,
    getNodes,
    setNodes,
    onNodesChange,
    removeNode,
    edges,
    setEdges,
    onEdgesChange,
  } = useRFContext((s) => s);

  const readFileContents = async () => {
    try {
      const selectedPath = await open({
        multiple: false,
        title: "Open file"
      });
      if (!selectedPath) return
    } catch (err) {
      console.error(err);
    }
  }


  const loadSchema = async (filename) => {
    const schemaYAML = await readTextFile(`subwayGUI-data/${filename}`, {
      dir: BaseDirectory.Download,
    });
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
    const parsedEdges: Edge[] = schemaData.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      animated: true,
      markerEnd: {
        type: MarkerType.ArrowClosed,
      },
    }));
    const layoutedNodes = getLayoutedElements(parsedNodes);
    setNodes([...layoutedNodes]);
    setEdges([...parsedEdges]);
  };

  const saveSchema = async () => {
    const schemaData = JSON.stringify({
      nodes: getNodes().map((node) => ({
        id: node.id,
        node_type: "pattern",
        node_label: node.data.label,
        node_data: {
          extension: node.data?.extension,
          prefix: node.data?.prefix,
        }
      })),
    });
    try {
      const savePath = await save({
        filters: [{
          name: 'schema',
          extensions: ['json']
        }]
      });
      if (!savePath) return;
      await invoke("save_file", { path: savePath, contents: schemaData })
    } catch (err) {
      console.error(err);
    }
  }


  useImperativeHandle(ref, () => ({
    saveSchema,
    loadSchema
  }));

  // const edges = useStore(store, (s) => s.edges);
  const reactFlowWrapper = useRef(null);
  // const [nodes, setNodes, onNodesCange] = useNodesState(initialNodes);
  // const [edges, setEdges, onEdgesChange] = useEdgesState([]);
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
    },
  });

  const onConnect = useCallback(
    (connection) => {
      const edge = { ...connection };
      edge.animated = true
      edge.markerEnd = {
        type: MarkerType.ArrowClosed,
      }
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

      setNodes((nodes) => nodes.concat({ ...newNode, data: { label: "File Pattern" } }));
      setTimeout(() => {
        addSelectedNodes([newNode.id]);
        reactFlowInstance.fitView();
      }, 1);
    },
    [reactFlowInstance],
  );

  useEffect(() => {
    if (initialSchema) {
      // Logic to load and apply the schema
      loadSchema(initialSchema);
    }
  }, [initialSchema]);

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
