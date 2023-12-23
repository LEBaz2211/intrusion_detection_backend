import Wrapper from "~/components/PageWrapper";
import { setDevicesStore, devicesStore, setApiPutDeviceArgs, apiPutDeviceArgs, device} from "~/store";
import { IDevice } from "~/interfaces/sensors.interfaces";
import UpdateDeviceForm from "~/components/DeviceDetail";
import { Component } from "solid-js";
import Logs from "~/components/Logs";




export const Detail :Component<{device: IDevice}> = (props)=> {
  return (
      <div class = "grid grid-cols-[400px,auto] grid-rows-2 h-full gap-10 text-sky-600 overflow-y-scroll background-photo">
        <div class = " rounded-lg bg-gray-100 p-4 row-span-2">
          <h2>Detail</h2>
          <UpdateDeviceForm
            device={props.device}
            onUpdate={(device: IDevice) => {
              const devices = devicesStore.filter((item) => item.device_id !== device.device_id);
              setDevicesStore([
                ...(devices || []),
                { ...device, },
              ]);
              setApiPutDeviceArgs(device);
              console.log(apiPutDeviceArgs());
            }}
          />
        </div>
        <div class = " rounded-lg bg-gray-100 p-4 overflow-y-scroll h-full row-span-2">
          <h2>Logs</h2>
          <Logs device_id = {props.device.device_id}/>
        </div>

      </div>
  );
}

export default Detail;