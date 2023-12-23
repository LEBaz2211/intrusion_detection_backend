import { Component, For } from "solid-js"
import { IEventLog } from "~/interfaces/sensors.interfaces"
import { logsStore, setLogsStore, FetchEventLogsParams } from "~/store"
import { get_logs_from_db } from "~/apiClient/device"
interface LogsProps { device_id: string }

const x_more_logs = (query: FetchEventLogsParams,number: number) => {
    const newQuery = query
    newQuery.startId = logsStore[logsStore.length - 1].event_id
    newQuery.number = number
    get_logs_from_db(newQuery).then((res) => {

        setLogsStore([...logsStore,...res.slice(1,)])
    })
}
const headerClass = "text-lg text-sky-600 rounded-lg pb-4 border-gray-400 "
const itemClass = " pl-3 pr-3 mb-1 text-lg bg-gray-300 text-sky-800 border border-gray-400 "
const buttonClass = "bg-sky-600 hover:bg-sky-700 text-white font-bold py-2 px-4 rounded"
const Logs: Component<LogsProps> = (props) => {
    const query: FetchEventLogsParams = {
        deviceId: props.device_id,
        number: 10,
        startId: null
    }
    setLogsStore([])
    get_logs_from_db(query).then((res) => {
        setLogsStore(res)
    });
    return (
        <div class = "relative">
            <div class="position sticky top-0 bg-gray-100">
                <div class = {"p-4 flex justify-end gap-4"}>
                    <button class = {buttonClass} onClick={()=>x_more_logs(query,10)}> load 10</button>
                    <button class = {buttonClass} onClick={()=>x_more_logs(query,100)}> load 100</button>
                </div>
                <div class = "grid grid-cols-4  w-full">
                    <label class = {headerClass}> Event Type </label>
                    <label class = {headerClass}> Event Id </label>
                    
                    <label class = {headerClass}> Event Description </label>
                    <label class = {headerClass}> Time </label>
                </div>
            </div>
            <div class = "grid grid-cols-[auto,auto,auto,auto] overflow-y-scroll "
            
            >
            <For each = {logsStore}>
                {(item: IEventLog) => (
                    <>
                        <label class={itemClass}
                        classList={{ 
                            "bg-red-600 text-gray-100": item.event_type === "INTRUDER_DETECTED",
                            "bg-lime-600 text-gray-100": item.event_type === "DEVICE_OPERATIONAL",
                            "bg-orange-400 text-gray-100": item.event_type === "DEVICE_TIMEOUT",
                            "bg-gray-400 text-gray-100": item.event_type === "DEVICE_INACTIVE",
                            "bg-sky-600 text-gray-100": item.event_type === "ACTIVE",
                        }}> 
                        {item.event_type} </label>
                        <label class={itemClass}>{item.event_id}</label>
                        <label class={itemClass}>{item.event_description}</label>
                        <label class={itemClass}>{item.timestamp}</label>
                    </>
                )}
            </For>
            </div >
        </div>
    )
};

export default Logs;