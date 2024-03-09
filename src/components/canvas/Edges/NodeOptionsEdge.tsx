import { BaseEdge, Connection, Edge, EdgeLabelRenderer, Node, getStraightPath } from 'reactflow';
import { useRFContext } from '../../../contexts/ReactFlowContext';
import { BadgeCheck, FileCheck, PlusCircleIcon, SigmaSquare } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "../../@shadcn/ui/dropdown-menu"
import { CustomNodeData } from '~/types/RFNodes';

export default function NodeOptionsEdge({ id, source, sourceX, sourceY, target, targetX, targetY }) {
  const { getId, nodes, setEdges, onConnect, setNodes } = useRFContext((s) => s)

  const [edgePath, labelX, labelY] = getStraightPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
  });

  const addNodeBetween = (type: string) => {
    const newNode: Node<CustomNodeData> = {
      id: getId(),
      type,
      position: {
        x: labelX - 35,
        y: labelY - 30,
      },
      data: {
        label: `${type} node`
      },
    };

    setNodes((nds) =>
      nds.map((node: Node<CustomNodeData>) => {
        if (node.id === source) {
          // it's important that you create a new object here
          // in order to notify react flow about the change
          node.position = {
            x: node.position.x - 100,
            y: node.position.y,
          };
        }
        else if (node.id === target) {
          // it's important that you create a new object here
          // in order to notify react flow about the change
          node.position = {
            x: node.position.x + 100,
            y: node.position.y,
          };
        }

        return node;
      }).concat(newNode)
    );
    setEdges((es) => es.filter((e) => e.id !== id));
    const sourceConnection = {
      source: source,
      target: newNode.id,
      sourceHandle: null,
      targetHandle: null,
      type: 'addNodeOptions'
    } as Connection
    const targetConnection = {
      source: newNode.id,
      target: target,
      sourceHandle: null,
      targetHandle: null,
      type: 'addNodeOptions'
    } as Connection
    onConnect(sourceConnection);
    onConnect(targetConnection);


  }

  return (
    <>
      <BaseEdge id={id} path={edgePath} />
      <EdgeLabelRenderer>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button
              style={{
                position: 'absolute',
                transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
                pointerEvents: 'all',
              }}
              className="nodrag nopan bg-[white] p-1 rounded-md"

            >
              <PlusCircleIcon size={18} color='#8A3FFC' />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56">
            <DropdownMenuLabel>Add Node</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <DropdownMenuItem onClick={() => addNodeBetween('schemaNode')}>
                <FileCheck className="mr-2 h-4 w-4" />
                <span>File Pattern</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => addNodeBetween('functionNode')}>
                <SigmaSquare className="mr-2 h-4 w-4" />
                <span>Function</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => addNodeBetween('validationNode')}>
                <BadgeCheck className="mr-2 h-4 w-4" />
                <span>Validation</span>
              </DropdownMenuItem>
            </DropdownMenuGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </EdgeLabelRenderer>
    </>
  );
}
