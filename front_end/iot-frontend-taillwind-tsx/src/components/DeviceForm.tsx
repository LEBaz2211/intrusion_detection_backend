import { createFormGroup, createFormControl, withControl } from "solid-forms";
import { IDevice } from "~/interfaces/sensors.interfaces";
import { TextField } from "~/components/TextField";

const controlFactory = () => {
  return createFormGroup({
    name: createFormControl<string>("Device", {
      required: true,
      validators: (val: string) => {
        return !val.length ? {isMissing: true} : null;
      }
    }),

    device_id: createFormControl<string>(""),
    status: createFormControl<string>("INACTIVE"),
    x1: createFormControl<number>(0),
    y1: createFormControl<number>(0),
    x2: createFormControl<number>(0),
    y2: createFormControl<number>(0),

  });
};

export const DeviceForm = withControl<
  {
    device?: Partial<IDevice>;
    formSubmit: Function;
    formUpdate?: Function;
    actionBtnText: string;
  },
  typeof controlFactory
>({
  controlFactory,
  component: (props) => {
    const controlGroup = () => props.control.controls;
    const device = () => props.device;

    return (
      <form
        action=""
        class="space-y-4"
        classList={{
          "is-valid": props.control.isValid,
          "is-invalid": !props.control.isValid,
          "is-touched": props.control.isTouched,
          "is-untouched": !props.control.isTouched,
          "is-dirty": props.control.isDirty,
          "is-clean": !props.control.isDirty,
        }}
        onSubmit={(e) => {
          e.preventDefault();
          console.log(props.control.value);

          const params = {
            ...props.control.value
          };
        
          props.formSubmit(params);
        }}
      >
        <div class="grid grid-cols-1 gap-4">
          <div>
            <label for="name" class="mb-4 block">
              Device Name
            </label>
            <TextField
              placeholder="name"
              id="name"
              label="Name"
              control={controlGroup().name}
            />
          </div>
          <div>
            <label for="device_id" class="mb-4 block">
              Device ID
            </label>
            <TextField
              placeholder="device Id"
              id="device_id"
              label="device_id"
              control={controlGroup().device_id}
            />
          </div>
          <div>
            <label for="status" class="mb-4 block">
              Status
            </label>
            <TextField
              placeholder="status"
              id="status"
              label="status"
              control={controlGroup().status}
            />
          </div>
          <div>
            <label for="x1" class="mb-4 block">
              Device x coordinate

            </label>
            <TextField
              type="number"
              id="x1"
              label="x1"
              control={controlGroup().x1}
            />
          </div>
          <div>
            <label for="y1" class="mb-4 block">
              Device y coordinate
            </label>
            <TextField
              type="number"
              id="y1"
              label="y1"
              control={controlGroup().y1}
            />
          </div>
          <div>
            <label for="x2" class="mb-4 block">
              Reflector x coordinate
            </label>
            <TextField
              type="number"
              id="x2"
              label="x2"
              control={controlGroup().x2}
            />
          </div>
          <div>
            <label for="y2" class="mb-4 block">
            Reflector y coordinate
            </label>
            <TextField
              type="number"
              id="y2"
              label="y2"
              control={controlGroup().y2}
            />
          </div>
          
        </div>


        <div class="mt-4">
          <button
            disabled={!props.control.isValid}
            type="submit"
            class="inline-flex items-center disabled:bg-gray-500 justify-center w-full px-5 py-3 text-white bg-sky-600 hover:bg-sky-700 rounded-lg sm:w-auto"
          >
            <span class="font-medium"> {props.actionBtnText} </span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5 ml-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14 5l7 7m0 0l-7 7m7-7H3"
              />
            </svg>
          </button>
        </div>
      </form>
    );
  },
});