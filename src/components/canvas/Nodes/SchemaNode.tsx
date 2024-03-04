import { useState, useRef, useEffect, memo } from "react";
import { Handle, Position, NodeToolbar } from "reactflow";
import FileSelector from "../FileSelector";

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

function SchemaNode({ data }) {
  const [isEditing, setIsEditing] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);
  const [label, setLabel] = useState(data.label); //TODO raise this state to ReactFlowDnd
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
    setLabel(selectedFile);
    data.label = selectedFile
    setShowTooltip(false);
  };

  return (
    <div className="schema-node">
      <div>
        <EditableLabel
          label={label}
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
