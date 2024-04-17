/// <reference types="vite-plugin-svgr/client" />
import { Handle, NodeProps, Position } from 'reactflow';
import FunctionIcon from "../../../assets/svg/function.svg?react";
import { FunctionNodeData } from '~/types/RFNodes';

function RunSchemaNode(props: NodeProps<FunctionNodeData>) {
  console.log(props)
  return (
    <div>

      <div className={`function-node rounded-full bg-[#8A3FFC] p-4 flex justify-center ${props.selected ? 'rf-node-selected' : ''}`}>
        {props.data?.match ? 'Match Found' : 'Match not found'}
      </div>
    </div>
  );
}

export default RunSchemaNode;
