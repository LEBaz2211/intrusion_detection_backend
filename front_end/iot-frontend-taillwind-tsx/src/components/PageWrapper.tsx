
import { SensorList } from "~/components/sensorList";
import { DeviceModal } from "~/components/DeviceModal";
import { JSX } from "solid-js/jsx-runtime";
import { showModal, setShowModal, toastMessage, setToastMessage, devicesStore } from "~/store";
import { ComponentProps, createEffect } from "solid-js";
import toast from "solid-toast";


interface PageProps extends ComponentProps<any> {
    children: JSX.Element[] | JSX.Element
}

export default function PageWrapper(props: PageProps) {
  createEffect(() => {
    if (toastMessage().length > 0) toast(toastMessage());
    setToastMessage("");
  });
  return (
    <div class = "flex flex-grow w-full h-full ">
    <div>
        <DeviceModal
          show={showModal()}
          onModalHide={(id: string | null) => {
            setShowModal(!showModal());
          }}
        />
      </div>
    <main class="grid grid-cols-[400px_minmax(900px,_1fr)] gap-10 text-gray-200 m-10 w-full">
      
      <aside class = "w-100 h-[85vh]">
        <SensorList
          devices={devicesStore}
        />
      </aside>
      <section class = " overflow-y-auto h-[85vh]">
        {props.children}
      </section>
    </main>
    </div>
  );
}
