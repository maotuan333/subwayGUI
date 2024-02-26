const onDragStart = (event, nodeType) => {
  event.dataTransfer.setData('application/reactflow', nodeType);
  event.dataTransfer.effectAllowed = 'move';
};

type DraggableItemProps = {
  nodeType: string
  label: string,
  background: string,
  Icon: React.ReactNode
}
//@ts-ignore
function DraggableItem({ nodeType, label, background, Icon }: DraggableItemProps) {
  // @ts-ignore
  const colors = "bg-[#4B8BF3] bg-[#F34E1E] bg-[#FB43B9] bg-[#8A3FFC] bg-[#aA32A1] bg-[#12B368]";
  // @ts-ignore
  const bordercolors = "active:border-[#4B8BF3] active:border-[#F34E1E] active:border-[#FB43B9] active:border-[#8A3FFC] active:border-[#aA32A1] active:border-[#12B368]"
  return (
    <div className={`dndnode input rounded-sm overflow-hidden border-seperator border-[1px] hover:cursor-pointer active:cursor-grab active:border-dashed active:border-[${background}]`} onDragStart={(event) => onDragStart(event, nodeType)} draggable>
      <div className="flex items-center gap-2">
        <div className={`bg-[${background}] p-2`}>
          {Icon}
        </div>
        <h6 className="text-sm">{label}</h6>
      </div>
    </div>
  )
}

export default DraggableItem;