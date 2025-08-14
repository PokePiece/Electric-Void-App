import React from 'react';
import MetaChat from './MetaChat';

export default function MetaVoid() {


    return (
        <div>
            <h1 className='p-3 text-lg'>MetaVoid</h1>
            <MetaChat bodyPlaceholder='Display here...' inputPlaceholder='Enter here...' title='MetaChat' />
        </div>
    )
}