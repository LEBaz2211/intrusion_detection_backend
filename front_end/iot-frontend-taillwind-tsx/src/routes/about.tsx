import { A } from "solid-start";

export default function About() {
  return (
    <main class="text-center mx-auto text-gray-200 p-4">
      <h1 class="max-6-xs text-6xl text-gray-200 font-thin uppercase my-16">
        About Page
      </h1>
      <p class="my-4">
        <A href="/" class="text-gray-50 hover:underline">
          Home
        </A>
        {" - "}
        <span>About Page</span>
      </p>
    </main>
  );
}
