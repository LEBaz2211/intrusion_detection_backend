import { Component, createEffect, createSignal } from 'solid-js';
import { IDevice } from '~/interfaces/sensors.interfaces';

const FormItem: Component<{ key: string,label: string, type: string, value: string|number, onChange: (e: Event) => void }> = (props) => {
  return (
    <div class = "flex flex-col gap-4">
      <label>
        {props.label}
      </label>
      {props.type === 'display' ? 
      <label class=" pl-3 text-lg text-sky-800 rounded-lg">{props.value}</label> 
      : <input
          name={props.key}
          class={`w-full p-3 text-sm  rounded-lg`}
          type={props.type}
          value={props.value}
          onChange={props.onChange}
        />}
    </div>
  );
}



const UpdateDeviceForm: Component<{ device: IDevice, onUpdate: (device: IDevice) => void }> = (props) => {
  const [device, setDevice] = createSignal(props.device);
  const handleSubmit = (e: Event) => {
    e.preventDefault();
    props.onUpdate(device());
  };

  const handleChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    setDevice(prev => ({ ...prev, [target.name]: target.value }));
  };


  return (
    <form onSubmit={handleSubmit} class=" flex flex-col gap-6">
      <FormItem
        key = "device_id"
        label="Device ID"
        type="display"
        value={device().device_id}
        onChange={handleChange}
      />
      <FormItem
        key = "name"
        label="Device Name"
        type="text"
        value={device().name}
        onChange={handleChange}
      />
      <button 
      onClick={(e)=>{ handleChange(e); props.onUpdate(device()); }}
      name='status'
      value='ACTIVE'
      class=" pl-3 text-lg text-sky-800 rounded-lg">
        Reset Status
      </button>
      <div class="grid gap-4 grid-cols-2">
        <FormItem
          key = "x1"
          label="Device x"
          type="number"
          value={device().x1}
          onChange={handleChange}
        />
        <FormItem
          key = "y1"
          label="Device y"
          type="number"
          value={device().y1}
          onChange={handleChange}
        />
      </div>
      <div class="grid gap-4 grid-cols-2">
        <FormItem
          key = "x2"
          label="Reflector x"
          type="number"
          value={device().x2}
          onChange={handleChange}
        />  
        <FormItem
          key = "y2"
          label="Reflector y"
          type="number"
          value={device().y2}
          onChange={handleChange}
        />
      </div>
      

      
      <button type="submit">Update Device</button>
    </form>
  );
};

export default UpdateDeviceForm;
