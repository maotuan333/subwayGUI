import React, { useState, useEffect } from 'react';
import { open } from '@tauri-apps/api/dialog';
import { readDir, BaseDirectory } from '@tauri-apps/api/fs';
import { desktopDir } from '@tauri-apps/api/path';
import { Tree } from 'react-arborist';
import { Button } from '../@shadcn/ui/button';
import { ChevronDown, ChevronRight, FileIcon } from 'lucide-react';
// Reads the `$APPDATA/users` directory recursively


export default () => {
  // const [appDataDirPath, setAppDataDirPath] = useState("");
  const [data, setData] = useState([]);
  const [root, setRoot] = useState<string | string[] | null>("");

  const openFileFinder = async () => {
    const selected = await open({
      directory: true,
      recursive: true
    });
    setRoot(selected);
  };


  useEffect(() => {
    var i = 0; // Create globally scoped variable to create id for files/folder
    function loopThroughJSON(obj) {
      if (typeof obj === 'object') {
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
      if (!root) return;
      console.log("getting entries")
      const entries = await readDir(root, { recursive: true });
      loopThroughJSON(entries);
      setData(entries);
    }
    getAppDataDir();
  }, [root])


  return (
    <div className='h-full'>
      <Button className='w-[80%] mt-8 ml-6 rounded-sm !bg-blue-500 hover:!bg-blue-500/[0.8] !text-white' onClick={openFileFinder}>Open Folder</Button>
      <Tree
        data={data}
        openByDefault={false}
        width={"15rem"}
        style={{ height: '100%' }}
        indent={24}
        height={1000}
        paddingBottom={10}
        padding={25 /* sets both */}
      >
        {Node}
      </Tree>
    </div>
  );
};

// Custom node rendering for each folder/file in the tree
function Node({ node, style, dragHandle }) {
  /* This node instance can do many things. See the API reference. */
  return (
    <div className='hover:bg-seperator'>
      <div style={style} className='ml-6 flex font-inter text-[13px] items-center gap-2 ' ref={dragHandle}>
        <span onClick={() => { node.isOpen ? node.close() : node.open() }}>
          {node.isLeaf ? <FileIcon size={14} /> : node.isOpen ? <ChevronDown size={17} /> : <ChevronRight size={17} />}
        </span>
        {node.data.name}
      </div>
    </div>
  );
}