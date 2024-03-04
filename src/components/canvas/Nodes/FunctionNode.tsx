/// <reference types="vite-plugin-svgr/client" />
import { useCallback } from 'react';
import { Handle, Position } from 'reactflow';
import FunctionIcon from "../../../assets/svg/function.svg?react";

const handleStyle = { left: 10 };

function FunctionNode({ data, isConnectable }) {
  const onChange = useCallback((evt) => {
    console.log(evt.target.value);
  }, []);

  return (
    <div>

      <div className="text-updater-node rounded-full bg-[#4B8BF3] p-4 flex justify-center">
        <Handle type="target" position={Position.Left} isConnectable={isConnectable} />
        <Handle type="target" position={Position.Right} isConnectable={isConnectable} />
        <FunctionIcon width={24} height={24} />
        <div className='absolute top-[110%] w-[10rem]'>
          <h1 className="text-xs font-inter font-semibold">Run Script</h1>
        </div>
      </div>
    </div>
  );
}

export default FunctionNode;
