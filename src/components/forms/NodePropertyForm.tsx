"use client"
import { Input } from '../@shadcn/ui/input';
import { useForm } from 'react-hook-form';
import { useRFContext } from '../../contexts/ReactFlowContext';
import { Node, useStore } from 'reactflow';
import { CustomNodeData } from '~/types/RFNodes';

import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '../@shadcn/ui/form';

import React, { useMemo } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../@shadcn/ui/select';

const formStructureMapping = {
  functionNode: {
    fields: [
      { name: 'filepath', label: 'Script Path', type: 'text', required: true },
    ]
  },
  schemaNode: {
    fields: [
      { name: 'label', label: 'Label', type: 'text', options: [], required: false },
      { name: 'extension', label: 'File Extension', type: 'text', options: [], required: true },
      { name: 'prefix', label: 'Prefix', type: 'text' },
    ]
  },
};

const NodePropertyForm = () => {
  const selectedNode = useStore(s => s.getNodes().filter(node => node.selected))[0];
  const form = useForm();
  const formStructure = formStructureMapping[selectedNode?.type];
  const setNodes = useRFContext((s) => s.setNodes);
  const updateField = (value: string, field: string) => {
    setNodes((nds) =>
      nds.map((node: Node<CustomNodeData>) => {
        if (node.id === selectedNode?.id) {
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
    <div className=''>
      <Form {...form}>

        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            formStructure.fields.map((field) => {
              return (
                <div key={field.name}>
                  {
                    field.type === "select" ?
                      <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Email</FormLabel>
                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                              <FormControl>
                                <SelectTrigger>
                                  <SelectValue placeholder="Select a verified email to display" />
                                </SelectTrigger>
                              </FormControl>
                              <SelectContent>
                                <SelectItem value="m@example.com">m@example.com</SelectItem>
                                <SelectItem value="m@google.com">m@google.com</SelectItem>
                                <SelectItem value="m@support.com">m@support.com</SelectItem>
                              </SelectContent>
                            </Select>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      :
                      <FormItem className='mb-4'>
                        <FormLabel className='flex gap-1'>{field.label} {field.required ? <h1 className='text-red-400'>*</h1> : ''}</FormLabel>
                        <FormControl>
                          <Input value={selectedNode?.data[field.name]} autoComplete='off' onChange={(e) => updateField(e.target?.value, field.name)} placeholder={`${field.name}...`} {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                  }
                </div>
              )
            })
          )
          }
        />
      </Form>
    </div>
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