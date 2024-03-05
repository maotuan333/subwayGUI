import { useState, useRef, useEffect, memo, useContext } from "react";
import { Handle, Position, NodeToolbar, NodeProps } from "reactflow";
import { ReactFlowContext } from "../../../contexts/ReactFlowContext";
import { useStore } from "zustand";
import { NodeData } from "../../../stores/RFStore";

function EditableLabel({
  label,
  handleChange,
  handleBlur,
  handleClick,
  isEditing,
}) {
  const inputRef = useRef(null);

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditing]);

  return (
    <input
      type="text"
      value={label}
      onBlur={handleBlur}
      onClick={handleClick}
      onChange={handleChange}
      readOnly={!isEditing}
      ref={inputRef}
      style={{
        border: "none",
        outline: "none",
        textAlign: "center",
      }}
    />
  );
}

function SchemaNode({ id, data, selected }: NodeProps<NodeData>) {
  const [isEditing, setIsEditing] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);
  const fileInputRef = useRef(null);

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
    updateNodeLabel(id, selectedFile);
    setShowTooltip(false);
  };
  const store = useContext(ReactFlowContext)
  if (!store) throw new Error('Missing ReactFlowContext.Provider in the tree');
  const { updateNodeLabel } = useStore(store, (s) => s)

  return (
    <div className={`schema-node ${selected ? 'rf-node-selected' : ''}`}>
      <div>
        <EditableLabel
          label={data.label}
          handleChange={handleFileChange}
          handleBlur={handleBlur}
          handleClick={handleClick}
          isEditing={isEditing}
        />
        {/* TODO: Only show text cursor when hovering text */}
      </div>
      <Handle type="target" position={Position.Top} isConnectable={true} />

      {showTooltip && (
        <NodeToolbar align="end" isVisible position={Position.Bottom}>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: "none" }}
          />
          <button
            style={{ backgroundColor: "white" }}
            onClick={handleFileSelectClick}
            className="bg-white text-black"
          >
            Select File
          </button>
        </NodeToolbar>
      )}
      <Handle type="source" position={Position.Bottom} isConnectable={true} />
    </div>
  );
}

export default memo(SchemaNode);
