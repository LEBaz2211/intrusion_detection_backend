// @refresh reload
import { Suspense } from "solid-js";
import { Router } from "solid-app-router";
import { NavBar } from "./components/NavBar";
import {
  
  Body,
  ErrorBoundary,
  FileRoutes,
  Head,
  Html,
  Meta,
  Routes,
  Scripts,
  Title,
} from "solid-start";
import "./root.css";

import { Toaster } from "solid-toast";

export default function Root() {

  return (
    <Html lang="en">
      <Head>
        <Title>lazzzzer !!!</Title>
        <Meta charset="utf-8" />
        <Meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <Body class = "flex flex-col">
        <Toaster 
        position="top-right"
        // Spacing between each toast in pixels
        gutter={8}
        toastOptions={{
          className: '',
          duration: 5000,
          position: 'top-center',
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
        />

      <Router>
        <Suspense>
          <ErrorBoundary>
            <NavBar />
              <Routes>
                <FileRoutes />
              </Routes>
          </ErrorBoundary>
        </Suspense>
        </Router>
        <Scripts />
      </Body>
    </Html>
  );
}
