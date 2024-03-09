/// <reference types="vite-plugin-svgr/client" />
import { Handle, NodeProps, Position } from 'reactflow';
import FunctionIcon from "../../../assets/svg/function.svg?react";
import { FunctionNodeData } from '~/types/RFNodes';

function FunctionNode(props: NodeProps<FunctionNodeData>) {
  return (
    <div>

      <div className={`function-node rounded-full bg-[#8A3FFC] p-4 flex justify-center ${props.selected ? 'rf-node-selected' : ''}`}>
        <Handle type="target" position={Position.Left} isConnectable={props.isConnectable} />
        <FunctionIcon width={32} height={32} />
        <div className='absolute top-[110%] w-[10rem]'>
          <h1 className="text-xs font-inter font-semibold">Run Script</h1>
        </div>
        <Handle type="source" position={Position.Right} isConnectable={props.isConnectable} />
      </div>
    </div>
  );
}

export default FunctionNode;
