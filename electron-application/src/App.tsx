import React from 'react';
import Math from './Math.tsx'
import Chat from './Chat.tsx'
import Auto from './Auto.tsx'
import MetaVoid from './MetaVoid.tsx';

export default function App() {


  return (
      <div className=''>
      <div className="text-center flex flex-row justify-center gap-20 py-10 bg-gray-900">
       
        <a href='/' ><p className='text-blue-200 text-2xl'>Human</p></a>
       
      </div>
      <h1 className='p-3 text-lg'>InterVoid</h1>
      <div className='pt-3'>
        <Chat
          title=""
          bodyPlaceholder="Response will appear here..."
          inputPlaceholder="Type a message..."
        
          /> 
      </div>
      <div>
        <Auto />
      </div>
      <MetaVoid />
      <Math />
    </div>
  )
}