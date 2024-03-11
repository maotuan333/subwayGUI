import { EllipsisVertical, Trash2, TrashIcon } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "../../@shadcn/ui/dropdown-menu"
import { useRFContext } from "../../../contexts/ReactFlowContext";

function MoreActionsButton({ nodeId }) {
  const { removeNode } = useRFContext((s) => s)

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <EllipsisVertical size={18} />
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuLabel>Node Actions</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem onClick={() => removeNode(nodeId)}>
            <Trash2 className="text-red-400 mr-2 h-4 w-4" />
            <span>Delete Node</span>
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default MoreActionsButton;