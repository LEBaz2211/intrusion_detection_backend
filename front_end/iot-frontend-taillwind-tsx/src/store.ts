import { IDevice, IEventLog } from "./interfaces/sensors.interfaces";
import { createEffect, createSignal } from "solid-js";
import { createStore, SetStoreFunction, Store } from "solid-js/store";
import toast from "solid-toast";

export function createLocalStore<T extends object>(
  name: string,
  init: T
): [Store<T>, SetStoreFunction<T>] {
  const localState = localStorage.getItem(name);
  const [state, setState] = createStore<T>(
    localState ? JSON.parse(localState) : init
  );
  createEffect(() => localStorage.setItem(name, JSON.stringify(state)));
  return [state, setState];
}

export function removeIndex<T>(array: readonly T[], index: number): T[] {
  return [...array.slice(0, index), ...array.slice(index + 1)];
}

const logs:IEventLog[] = [
  {
    event_id : 1,
    device_id : "ecam-intrusion-monitoring-2023",
    timestamp : "2021-10-01 12:00:00",
    event_type : "Intrusion",
    event_description : "Intrusion detected in the area",
  },
  {
    event_id : 2,
    device_id : "ecam-intrusion-monitoring-2023",
    timestamp : "2021-10-01 13:00:00",
    event_type : "Intrusion",
    event_description : "Intrusion detected in the area",
  },
];

export interface FetchEventLogsParams {
  deviceId: string;
  number?: number;
  startId?: number | null;
};


export const [device, setDevice] = createSignal<IDevice|undefined>(undefined);
export const [devicesStore, setDevicesStore] = createLocalStore<IDevice[]>("devices",[]);
export const [logsStore, setLogsStore] = createLocalStore<IEventLog[]>("logs",logs);

export const [showModal, setShowModal] = createSignal(false);
export const [deviceSignial, setDeviceSignial] = createSignal<IDevice|null>(null);

export const [apiGetDeviceArgs, setApiGetDeviceArgs] = createSignal("");
export const [apiGetAllDevicesArgs, setApiGetAllDevicesArgs] = createSignal(false);
export const [apiPostDeviceArgs, setApiPostDeviceArgs] = createSignal<IDevice|null>(null);
export const [apiPutDeviceArgs, setApiPutDeviceArgs] = createSignal<IDevice|null>(null);
export const [apiDeleteDeviceArgs, setApiDeleteDeviceArgs] = createSignal("");

export const [apiGetLogArgs, setApiGetLogArgs] = createSignal<FetchEventLogsParams|null>({ deviceId: "", number: 10, startId: null});


export const [liveData, setLiveData] = createSignal(false);
export const [toastMessage, setToastMessage] = createSignal("");