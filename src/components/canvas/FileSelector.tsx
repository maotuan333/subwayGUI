import { useRef } from "react";

function FileSelector({ setInput }) {
  const fileInputRef = useRef(null);

  const handleChange = (event) => {
    const value = event.target.value;
    setInput(value);
  };
  const handleClick = () => {
    fileInputRef.current.click();
  };

  // todo: tool tip when right clicking dummy element

  return (
    <div>
      <form>
        <input type="file" name="input" onChange={handleChange} hidden />
        <button onClick={handleClick}>Choose file</button>
      </form>
    </div>
  );
}

export default FileSelector;
