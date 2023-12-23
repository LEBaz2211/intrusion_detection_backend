import Wrapper from "~/components/PageWrapper";
import { device } from "~/store";
import { Detail } from "~/components/DevicePage";
import { IDevice } from "~/interfaces/sensors.interfaces";
import { Show } from "solid-js";
import Fa from 'solid-fa'
import { faArrowAltCircleLeft } from '@fortawesome/free-solid-svg-icons'




export default function Home() {
 return (
    <Wrapper>
      <Show when={device()} >
        <Detail device={device() as IDevice} />
      </Show>
      <Show when={!device()} >
        <div class = "relative h-full w-full flex">
        <img src="/bg.png"/>
          <code class=" m-auto text-gray-400 m-auto text-6xl"> 
          <div class = "flex justify-between">
            <Fa pulse icon={faArrowAltCircleLeft} /> 
          </div> 
          No device selected</code>
        </div>
      </Show>
    </Wrapper>
  );
}