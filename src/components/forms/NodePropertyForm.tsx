import React, { useState } from 'react';
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '../@shadcn/ui/form';
import { Input } from '../@shadcn/ui/input';
import { useForm } from 'react-hook-form';
import { useRFContext } from '../../contexts/ReactFlowContext';
import { Node } from 'reactflow';
import { NodeData } from '../../stores/RFStore';

// Define form structures for each object type
const formStructureMapping = {
  functionNode: {
    fields: [
      { name: 'filepath', label: 'Script Path', type: 'text' },
      // { name: 'field2', label: 'Field 2', type: 'number' },
      // Add more fields as needed
    ]
  },
  schemaNode: {
    fields: [
      { name: 'filepath', label: 'File Path', type: 'text' },
      { name: 'pattern', label: 'Regex Pattern', type: 'text' },
      // Add more fields as needed
    ]
  },
  // Add more mappings for other object types
};

const NodePropertyForm = ({ id, type, data }) => {
  const form = useForm();
  const formStructure = formStructureMapping[type];
  const { setNodes } = useRFContext((s) => s)
  console.log(data)
  const updateField = (value: string, field: string) => {
    console.log(value)
    console.log(field)
    setNodes((nds) =>
      nds.map((node: Node<NodeData>) => {
        if (node.id === id) {
          // it's important that you create a new object here
          // in order to notify react flow about the change
          node.data[field] = value;
        }
        return node;
      })
    );
  }


  if (!formStructure) {
    return <div>No properties exist for the node type.</div>;
  }

  return (
    <Form {...form}>

      <FormField
        control={form.control}
        name="username"
        render={({ field }) => (
          formStructure.fields.map((field) => (
            <div key={field.name}>
              {/* Render different types of input fields based on field.type */}
              {field.type === 'text' && (
                <FormItem className='mb-4'>
                  <FormLabel>{field.label}</FormLabel>
                  <FormControl>
                    <Input autoComplete='off' onChange={(e) => updateField(e.target?.value, field.name)} value={data[field.name]} placeholder={`${field.name}...`} {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
              {field.type === 'number' && (
                <FormItem>
                  <FormLabel>{field.name}</FormLabel>
                  <FormControl>
                    <Input type='number' autoComplete='off' placeholder={`${field.name}...`} {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
              {/* Add more conditional rendering for other field types as needed */}
            </div>
          ))
        )
        }
      />
    </Form>
    // <form onSubmit={handleSubmit}>
    // {formStructure.fields.map((field) => (
    //   <div key={field.name}>
    //     <label htmlFor={field.name}>{field.label}</label>
    //     {/* Render different types of input fields based on field.type */}
    //     {field.type === 'text' && (
    //       <input
    //         type="text"
    //         id={field.name}
    //         value={formValues[field.name] || ''}
    //         onChange={(e) => handleInputChange(field.name, e.target.value)}
    //       />
    //     )}
    //     {field.type === 'number' && (
    //       <input
    //         type="number"
    //         id={field.name}
    //         value={formValues[field.name] || ''}
    //         onChange={(e) => handleInputChange(field.name, e.target.value)}
    //       />
    //     )}
    //     {/* Add more conditional rendering for other field types as needed */}
    //   </div>
    // ))}
    //   <button type="submit">Submit</button>
    // </form>
  );
};

export default NodePropertyForm;