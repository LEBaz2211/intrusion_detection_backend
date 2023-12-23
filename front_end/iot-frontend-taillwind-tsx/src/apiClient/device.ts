
import { IDevice, IEventLog } from "~/interfaces/sensors.interfaces";

import { onCleanup } from "solid-js";
import { statusToastHandler } from "./toast";
import { apiGetAllDevicesArgs, devicesStore, setApiGetAllDevicesArgs, setApiPostDeviceArgs, setDevice, FetchEventLogsParams, liveData } from "~/store";



async function get_device_from_db(query: string) {
    if (query.trim() === "") return null;
    const response = await fetch(
        `http://127.0.0.1:5000/device/${query}`,
        {
            method: "GET",
        });
    statusToastHandler(response.status, null );
    const results = await response.json();
    const device = results.device as IDevice;
    return device;
}

async function get_devices_from_db() {
    const response = await fetch(
        `http://127.0.0.1:5000/devices`,
        {
            method: "GET",
        });
    statusToastHandler(response.status, null );
    console.log(response.status);
    const results = await response.json();
    const devices = results.devices as IDevice[];
    return devices;
}

async function post_device_to_db(device: IDevice) {
    const response = await fetch(
        `http://127.0.0.1:5000/device`,
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(device),
        });
    statusToastHandler(response.status, "Device created successfully" );
    
    const results = await response.json();
}
async function update_device_in_db(device: IDevice) {
    const response = await fetch(
        `http://127.0.0.1:5000/device/${device.device_id}`,
        {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(device),
        });
    
    statusToastHandler(response.status, "Device updated successfully" );
    const results = await response.json();
    console.log(results);
}

export async function delete_device_in_db(device_id: string) {
    const response = await fetch(
        `http://127.0.0.1:5000/device/${device_id}`,
        {
            method: "DELETE",
        });
    statusToastHandler(response.status, "Device deleted successfully" );
    const results = await response.json();
    console.log(results);
}

export async function get_logs_from_db({ deviceId, number, startId = null }: FetchEventLogsParams) {
    const baseUrl = 'http://127.0.0.1:5000/event_logs'; 
    const queryParams = new URLSearchParams();
  
    // Add query parameters if they are provided
    if (number !== undefined) queryParams.append('number', number.toString());
    if (startId !== null) queryParams.append('start_id', startId.toString());
  
    const url = `${baseUrl}/${encodeURIComponent(deviceId)}?${queryParams}`;
    const response = await fetch(url, { method: 'GET' });
    statusToastHandler(response.status, "logs Refreshed" );
    const results = await response.json();
    const logs = results.event_logs as IEventLog[];
    return logs;
}
  





import { createEffect } from "solid-js";
import { 
    apiDeleteDeviceArgs, 
    apiGetDeviceArgs,
    setApiGetDeviceArgs,
    apiPostDeviceArgs, 
    apiPutDeviceArgs, 
    setApiPutDeviceArgs,
    setApiDeleteDeviceArgs, 
    setDevicesStore } from "~/store";

let intervalIds: NodeJS.Timeout[] = []; 
createEffect(()=> {
    if (liveData()) { intervalIds.push(setInterval(()=>setApiGetAllDevicesArgs(true), 1000)) }
    else {
        intervalIds.forEach((intervalId) => clearInterval(intervalId));
        intervalIds = [];
    }
}
);

onCleanup(() => {
    intervalIds.forEach((intervalId) => clearInterval(intervalId));
  });

createEffect(()=> { 
    if (apiGetAllDevicesArgs()) {
        get_devices_from_db().then((db_devices) => {
            if (db_devices) setDevicesStore(db_devices);
        });
    }
    setApiGetAllDevicesArgs(false);
});
createEffect(()=> {
    const device = apiPostDeviceArgs();
    setApiPostDeviceArgs(null);
    if (device !== null) { 
        post_device_to_db(device);
        setApiGetAllDevicesArgs(true);
    }
});

createEffect(()=> {
    const device = apiPutDeviceArgs();
    setApiPutDeviceArgs(null);
    if (device !== null) {
        update_device_in_db(device);
        get_devices_from_db().then((db_devices) => {
            if (db_devices) setDevicesStore(db_devices); 
        });}
});

createEffect(()=> {
    if (apiDeleteDeviceArgs())
    {
        delete_device_in_db(apiDeleteDeviceArgs());
        setDevicesStore(devicesStore.filter((device) => device.device_id !== apiDeleteDeviceArgs()));
        setApiDeleteDeviceArgs("");
        setDevice(undefined);
    }
});

createEffect(()=> {
    const device_id = apiGetDeviceArgs();
    setApiGetDeviceArgs("");
    if (device_id !== "") {
        get_device_from_db(device_id).then((db_devices) => {
            const devices = devicesStore.filter((device) => device.device_id !== device_id);
            if (db_devices) setDevicesStore([...devices, db_devices]);
        });
    }
});



