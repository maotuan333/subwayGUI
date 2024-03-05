import { createContext } from 'react'
import { RFStore } from '~/stores/RFStore'

export const ReactFlowContext = createContext<RFStore | null>(null)