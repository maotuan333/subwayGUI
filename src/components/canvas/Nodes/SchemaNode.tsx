import { useState, useRef, useEffect, memo, useContext } from "react";
import { Handle, Position, NodeToolbar, NodeProps } from "reactflow";
import { useRFContext } from "../../../contexts/ReactFlowContext";
import { SchemaNodeData } from "~/types/RFNodes";
import { Blocks, EllipsisVertical, FileBox, TrashIcon, TriangleAlert } from "lucide-react";

import { Separator } from "../../../components/@shadcn/ui/separator";
import MoreActionsButton from "./MoreActions";
// function EditableLabel({
//   label,
//   handleChange,
//   handleBlur,
//   handleClick,
//   isEditing,
// }) {
//   const inputRef = useRef(null);

//   useEffect(() => {
//     if (isEditing && inputRef.current) {
//       inputRef.current.focus();
//     }
//   }, [isEditing]);

//   return (
//     <input
//       type="text"
//       value={label}
//       onBlur={handleBlur}
//       onClick={handleClick}
//       onChange={handleChange}
//       readOnly={!isEditing}
//       ref={inputRef}
//       style={{
//         border: "none",
//         outline: "none",
//         textAlign: "center",
//       }}
//     />
//   );
// }

function SchemaNode({ id, data, selected }: NodeProps<SchemaNodeData>) {

  const [isEditing, setIsEditing] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);
  const fileInputRef = useRef(null);
  const { updateNodeData } = useRFContext((s) => s)

  const handleClick = (e) => {
    setIsEditing(true);
    setShowTooltip(true);
    e.stopPropagation();
  };

  const handleBlur = () => {
    setIsEditing(false);
  };

  const handleFileSelectClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.value;
    updateNodeData(id, "filepath", selectedFile);
    setShowTooltip(false);
  };

  return (
    <>
      <div className={`items-center justify-between px-2 py-2 bg-[#414141] min-w-[15rem] rounded-md schema-node ${selected ? 'rf-node-selected' : ''}`}>
        <div className="flex flex-col gap-1.5 grow">
          <div className="flex items-center justify-between">
            <div className="flex gap-2.5 items-center">
              <div className="node-icon p-2 bg-[#4B8BF3] rounded-md">
                <FileBox size={20} color="white" />
              </div>
              <div className="node-text flex flex-col items-start">
                <h1 className="text-sm text-white">{data.label}</h1>
                <h1 className="text-xs text-[#bababa]">File Pattern</h1>
              </div>
            </div>
            <MoreActionsButton />
          </div>

        </div>


        <Handle type="target" position={Position.Left} isConnectable={true} />
        <Handle type="source" position={Position.Right} isConnectable={true} />
      </div >
      <div>

      </div>
      {
        !data.extension ?
          <div className="w-full mt-1 absolute ml-auto">
            <div className="flex flex-row-reverse items-center gap-2">
              <h1 className="text-[12px] text-[#bababa]">Missing required properties</h1>
              <TriangleAlert size={16} className="text-red-400" />
            </div>
          </div>
          : ''
      }
      {
        data.extension ?
          <div className="w-full mt-1 absolute ml-auto break-all">
            <div className="flex flex-row-reverse items-center gap-1">
              <h1 className="text-[12px]">Matches {data.extension} files {data.prefix ? `starting with ${data.prefix}` : ''}</h1>
              {/* <Blocks size={18} /> */}
            </div>
          </div>
          : ''
      }
    </>
  );
}

export default memo(SchemaNode);
