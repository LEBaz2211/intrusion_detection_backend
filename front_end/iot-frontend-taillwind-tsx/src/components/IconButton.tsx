

import { Component, ComponentProps } from "solid-js";

interface IconButtonProps extends ComponentProps<any> {
    onClick: (event: MouseEvent) => void;
    label: string;
    icon: Component;
    color?: string;
    type?: "reset" | "submit" | "button";
}

export const IconButton:Component<IconButtonProps> = ({
    onClick,
    label,
    icon,
    type,
    color,
    }) => {
    return (
    <button
        onclick={onClick}
        role="button"
        type={type || "button"}
        title={label}
        class={`w-10 h-10 flex transition-all ease-in-out duration-100 hover:scale-125 items-center justify-center text-white bg-${color?color:"sky"}-600 border border-${color?color:"sky"}-600 rounded-full hover:bg-${color?color:"sky"}-700 active:text-white focus:outline-none focus:ring`}
        >
            <span class="sr-only">{label}</span>
            {icon({})}
    </button>
    );
};