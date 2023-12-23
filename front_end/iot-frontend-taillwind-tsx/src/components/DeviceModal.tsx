import { Component, ComponentProps, Show } from "solid-js";
import { IDevice } from "~/interfaces/sensors.interfaces";
import { apiPostDeviceArgs, devicesStore, setDevicesStore } from "~/store";
import { DeviceForm } from "~/components/DeviceForm";
import { setApiPostDeviceArgs } from "~/store";
import  clickOutsideDirective  from "~/directives/click-outside.directive";

interface DeviceModalProps extends ComponentProps<any> {
    show: boolean;
    onModalHide: (id: string | null) => void;
    device?: IDevice;
}

const clickOutside = clickOutsideDirective;

export const DeviceModal: Component<DeviceModalProps> = (
    props: DeviceModalProps
) => {
    return (
        <Show when={props.show}>
            <div class="fixed z-50 top-0 left-0 right-0 bottom-0 bg-[rgba(0,0,0,0.75)]">
                <div class="relative max-h-[85%] overflow-y-auto top-20 bg-gray-200 max-w-md m-auto h- block p-8 pb-8 border-t-4 border-sky-600 rounded-lg shadow-xl"
                    use:clickOutside={() => {
                        props.onModalHide(null);
                    }} >
                    <h5 class="text-4xl font-bold mb-4">
                        {(props.device ? "Edit" : "Create") + " Device"}
                    </h5>

                    <DeviceForm
                        formSubmit={(device: IDevice) => {
                            setDevicesStore([
                                ...(devicesStore || []),
                                {
                                    ...device,
                                },
                            ]);
                            setApiPostDeviceArgs(device);
                            props.onModalHide(null);
                        }}
                        actionBtnText={"Save"}
                    />
                    <span class="absolute bottom-9 right-8">
                        <button onClick={() => props.onModalHide(null)}>
                            <svg
                                class="w-6 h-6 text-gray-500 hover:text-gray-900"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    stroke="currentColor"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M6 18L18 6M6 6l12 12"
                                ></path>
                            </svg>
                        </button>
                    </span>
                </div>
            </div>
        </Show>
    );
};
