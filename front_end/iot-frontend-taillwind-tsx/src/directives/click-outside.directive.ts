import { Accessor, onCleanup } from "solid-js";

export default function clickOutside(el: Element, accessor: Accessor<() => void>) {
    const onClick = (e: Event) => {
        if (!el.contains(e.target as Node)) {
            accessor()?.();
        }
    };
    // Listen for events in the capture phase
    document.addEventListener("click", onClick, true);

    onCleanup(() => document.removeEventListener("click", onClick, true));
}
