import { createStore } from 'zustand';
import {
  Connection,
  Edge,
  EdgeChange,
  Node,
  NodeChange,
  addEdge,
  OnNodesChange,
  OnEdgesChange,
  OnConnect,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';

// import initialNodes from './nodes';
// import initialEdges from './edges';

export type NodeData = {
  color?: string;
  label: string;
};

export interface RFProps {
  id: number,
  nodes: Node<NodeData>[];
  edges: Edge[];
}

export interface RFState extends RFProps {
  getId: () => string;
  onNodesChange: OnNodesChange;
  onEdgesChange: OnEdgesChange;
  onConnect: OnConnect;
  setNodes: (nodes) => void;
  setEdges: (edges) => void;
  updateNodeLabel: (nodeId: string, label: string) => void;
};

export type RFStore = ReturnType<typeof createRFStore>

export const createRFStore = (initProps?: Partial<RFProps>) => {
  const DEFAULT_PROPS: RFProps = {
    id: 0,
    nodes: [],
    edges: []
  }
  return createStore<RFState>((set, get) => ({
    ...DEFAULT_PROPS,
    ...initProps,
    getId: () => {
      set((state) => ({ id: state.id + 1 })); // Increment the ID using set
      return `${get().id}`;
    },
    onNodesChange: (changes: NodeChange[]) => {
      set({
        nodes: applyNodeChanges(changes, get().nodes),
      });
    },
    onEdgesChange: (changes: EdgeChange[]) => {
      set({
        edges: applyEdgeChanges(changes, get().edges),
      });
    },
    onConnect: (connection: Connection) => {
      set({
        edges: addEdge(connection, get().edges),
      });
    },
    setNodes: (nodes) => {
      set((state) => ({
        nodes: typeof nodes === 'function' ? nodes(state.nodes) : nodes,
      }));
    },
    setEdges: (edges) => {
      set((state) => ({
        edges: typeof edges === 'function' ? edges(state.edges) : edges,
      }));
    },
    updateNodeLabel: (nodeId: string, label: string) => {
      set({
        nodes: get().nodes.map((node) => {
          if (node.id === nodeId) {
            // it's important to create a new object here, to inform React Flow about the cahnges
            node.data = { ...node.data, label };
          }

          return node;
        }),
      });
    },
  }));
}