import { Component } from "solid-js";
import { Github } from "~/icons/github";
import  SocketComponent  from "~/apiClient/socket";
import { device } from "~/store";
import toast from "solid-toast";
import {
  A,
  useLocation,
} from "solid-start";


export const NavBar: Component = () => {

    const location = useLocation();
    if (device()?.status == "INTRUDER_DETECTED") toast("INTRUDER_DETECTED", 
    {
        duration: 5000,
        position: "top-center",
        style: { background: "red", color: "white",},
        icon: "🔥",
    });
    const active = (path: string) =>
        path == location.pathname
        ? "border-sky-600"
        : "border-transparent hover:border-sky-600";

    return (
        <nav class="bg-neutral-800 ">
            <ul class=" flex items-center p-3 text-gray-200 ">
                <li class={`border-b-2 ${active("/")} mx-1.5 sm:mx-6`}>
                    <A href="/">Home</A>
                </li>
                <li class={`border-b-2 ${active("/about")} mx-1.5 sm:mx-6`}>
                    <A href="/about">About</A>
                </li>
                <li class={`border-b-2  mx-1.5 sm:mx-6`}>
                    <A class = "flex gap-2" href="https://github.com/ChillinSoul/IOT-lazer.git"><Github/> Github</A>
                </li>
                <div class="flex-grow"></div>
                <li class={`border-b-2 mx-1.5 sm:mx-6`}>
                    <SocketComponent />
                </li>
            </ul>
        </nav>
    );
}