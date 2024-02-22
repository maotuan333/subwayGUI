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
  return (
    <div className="dndnode input border-seperator border-[1px] hover:cursor-pointer active:cursor-grab active:border-dotted active:border-blue-200 overflow-hidden" onDragStart={(event) => onDragStart(event, nodeType)} draggable>
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