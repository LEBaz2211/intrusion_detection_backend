import { Component, createSignal, onCleanup, onMount } from 'solid-js';
import { liveData, setLiveData } from '~/store';
import { Socket } from 'socket.io-client';


const SocketComponent : Component = () => {

  const [getSocket, setSocket] = createSignal<Socket | null>(null);

  

  return (
    <>
      {liveData() && 
      <div class = " text-lime-500" >Live Data on: 
      <button onClick={() => setLiveData(!liveData())} class = "hover:bg-red-700 text-white font-bold py-2 px-4 rounded"> 
        Disconnect 
      </button>
    </div>}
      {!liveData() && 
      <div class = " text-red-500" >Live Data off: 
        <button onClick={() => setLiveData(!liveData())} class = "hover:bg-lime-700 text-white font-bold py-2 px-4 rounded"> 
          Reconnect 
        </button>
      </div>}
    </>
  );
};

export default SocketComponent;
