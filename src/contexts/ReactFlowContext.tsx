import { useRef, createContext, useContext } from 'react'
import { useStore } from 'zustand'
import { RFProps, RFState, RFStore, createRFStore } from '../stores/RFStore'

const ReactFlowContext = createContext<RFStore | null>(null)


type RFProviderProps = React.PropsWithChildren<RFProps>

export function RFProvider({ children, ...props }: RFProviderProps) {
  const storeRef = useRef<RFStore>()
  if (!storeRef.current) {
    storeRef.current = createRFStore(props)
  }
  return (
    <ReactFlowContext.Provider value={storeRef.current}>
      {children}
    </ReactFlowContext.Provider>
  )
}

export function useRFContext<T>(selector: (state: RFState) => T): T {
  const store = useContext(ReactFlowContext)
  if (!store) throw new Error('Missing BearContext.Provider in the tree')
  return useStore(store, selector)
}