import { Component, ComponentProps } from "solid-js";
import { A, useLocation } from "solid-start";
import { IDevice } from "~/interfaces/sensors.interfaces";
import { IconButton } from "./IconButton";
import { Trash } from "~/icons/trash";
import { devicesStore, setDevicesStore, setApiDeleteDeviceArgs, setDevice, device } from "~/store";
import toast from "solid-toast";

interface SensorListItemProps extends ComponentProps<any> {
    item:IDevice;
}

const deleteDevice = (device: IDevice) => {
    
    const newDevices = devicesStore.filter(
        (item) => item.device_id !== device.device_id
    );
    setDevicesStore(newDevices);
    setDevice(undefined);
}

export const SensorListItem: Component<SensorListItemProps> = ({
    item,
    }) => {
    console.log(item);

    return (
        <>
            <div 
            class = "w-full"
            onClick = {()=>{
                setDevice(undefined);
                setDevice(item);
            }}
            >
            
                <div
                    class=" button-hover-parent-hide  p-2 flex flex-row justify-between text-gray-700 hover:bg-sky-600 hover:text-gray-200 cursor-pointer  rounded-lg mb-2 border border-solid border-2"
                    classList={{
                    "list__item --active bg-sky-600 text-gray-100": Boolean(
                        device()?.device_id === item.device_id
                    ),
                    "border-red-600": item.status === "INTRUDER_DETECTED",
                    "border-green-600": item.status === "ACTIVE",
                    "border-gray-300": item.status === "INACTIVE",
                    "border-purple-300": item.status === "DEVICE_TIMEOUT"
                    }}
                    >
                        
                    <div>
                        <div>{item.name}</div>
                        <div class="text-xs break-all"> {item.status} </div>
                    </div>
                    <div class ="button-hover-child-hide">
                        <IconButton 
                        color = "red"
                        onClick = {(e)=>{
                            e.preventDefault();
                            e.stopPropagation();
                            deleteDevice(item);
                            setApiDeleteDeviceArgs(item.device_id);
                        }}
                        label = "Delete"
                        icon = {Trash}
                        type = "button"
                        />
                    </div>
                </div>
                
            </div>
        </>
    );
}