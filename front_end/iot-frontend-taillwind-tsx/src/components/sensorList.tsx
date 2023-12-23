import { Component,ComponentProps,For,Show } from "solid-js";

import { setShowModal } from "~/store";
import { Plus } from "~/icons/plus"
import { IconButton } from "./IconButton";
import { SensorListItem } from "./sensorListItem";

import { devicesStore, setApiGetAllDevicesArgs, setDevice, device } from "~/store";
import { IDevice } from "~/interfaces/sensors.interfaces";
// @refresh reload

interface SensorListProps extends ComponentProps<any> {
    devices: IDevice[];
}


export const SensorList: Component<SensorListProps> = (props) => {
    setApiGetAllDevicesArgs(true);
    return (
        <>
            <div class="w-full  flex-col bg-gray-200 text-sky-600 h-full border-gray-300 border p-4 rounded-lg overflow-y-auto">
                <Show  when = {device()}>
                    <button
                        class = "bg-sky-600 hover:bg-sky-700 text-white font-bold py-2 px-4 rounded"
                        onClick={() => {setDevice(undefined);}}>
                        Open Map
                    </button>
                </Show>

                <div class="flex  justify-between py-4">
                    <h1 class="text-xl justify-center ">Devices</h1>
                    <IconButton
                        label="Add"
                        icon={Plus}
                        onClick={() => {
                            setShowModal(true);
                            setDevice(undefined);
                        }}
                    />
                </div>
                    
                <For each={props.devices} fallback={<div>Loading...</div>}>
                    {(item ) => ( <SensorListItem item={item} />)}
                </For>
            </div>
        </>
    );
}