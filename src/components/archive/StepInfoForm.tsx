import React, { useState } from "react";

function StepInfoForm() {
  const [inputs, setInputs] = useState({
    name:"",
    input:"",
    func:"",
    output:""
  });

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(inputs);
  }

  // todo: tool tip when right clicking dummy element

  return (
    <div>
    <form onSubmit={handleSubmit} >
        <label>Name:
        <input 
          type="text" 
          name="name" 
          placeholder="Name of the step"
          value={inputs.name || ""} 
          onChange={handleChange}
        />
        </label><br/>
      <label>Input:
      <input 
        type="file" 
        name="input" 
        placeholder="Unique extension or suffix"
        value={inputs.input || ""} 
        onChange={handleChange}
        required
      />
      </label><br/>
      <label>Script:
        <input 
          type="file" 
          accept=".py,.m"
          name="func" 
          placeholder="Select script for the step"
          value={inputs.func || ""} 
          onChange={handleChange}
        />
        </label><br/>
      <label>Output:
        <input 
          type="file" 
          name="output" 
          placeholder="Unique extension or suffix"
          value={inputs.output || ""} 
          onChange={handleChange}
          required
        />
        </label>
        <input type="submit" />
    </form>
    </div>
  )
}

export default StepInfoForm;
