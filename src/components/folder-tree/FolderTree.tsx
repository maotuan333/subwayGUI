import React, {useState, useEffect} from 'react';
import { open } from '@tauri-apps/api/dialog';
import { readDir, BaseDirectory } from '@tauri-apps/api/fs';
import { desktopDir } from '@tauri-apps/api/path';
import { Tree } from 'react-arborist';
// Reads the `$APPDATA/users` directory recursively


export default () => {
  // const [appDataDirPath, setAppDataDirPath] = useState("");
  const [data, setData] = useState([]);
  const [root, setRoot] = useState<string|string[]|null>("");

  const openFileFinder = async () => {
    const selected = await open({
      directory:true,
      recursive: true
    });
    setRoot(selected);
  };


  useEffect(() => {
    var i = 0; // Create globally scoped variable to create id for files/folder
    function loopThroughJSON(obj) {
      if (typeof obj === 'object'){
        obj.id = `${i}`;
        i++;
      } 
      for (let key in obj) {
        if (typeof obj[key] === 'object') {
          if (Array.isArray(obj[key])) {
            // loop through array
           
            for (let i = 0; i < obj[key].length; i++) {
              loopThroughJSON(obj[key][i]);
            }
          } else {
            // call function recursively for object
            loopThroughJSON(obj[key]);
          }
        }
      }
    }
    
    const getAppDataDir = async () => {
      console.log(root);
      if(!root) return;
      console.log("getting entries")
      const entries = await readDir(root, { recursive: true });
      loopThroughJSON(entries);
      setData(entries);
    }
    getAppDataDir();
  },[root])


  return (
    <>
    <button onClick={openFileFinder}>Open File</button>
    <Tree
      data={data}
      idAccessor="path"
    >
      {Node}
    </Tree>
    </>
  );
};

// Custom node rendering for each folder/file in the tree
function Node({ node, style, dragHandle }) {
  /* This node instance can do many things. See the API reference. */
  return (
    <div style={style} ref={dragHandle}>
      <span onClick={()=>{node.isOpen ? node.close() : node.open()}}>
      {node.isLeaf ? "🖹" : "🗀"}
      </span>
      {node.data.name}
    </div>
  );
}