type DefaultNodeData = {
  label: string;
};

export interface FunctionNodeData extends DefaultNodeData {
  extension?: string;
  prefix?: string;
}

export interface SchemaNodeData extends DefaultNodeData {
  filepath?: string;
  extension?: string;
  prefix?: string;
}

export type CustomNodeData = SchemaNodeData | FunctionNodeData;
