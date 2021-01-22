/**
 * Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
 */

import React, {useEffect, useRef} from 'react';

export default function Script(props) {
    const instance = useRef(null);
    const script = useRef(
        typeof document !== 'undefined' ? document.createElement('script') : null,
    );

    useEffect(() => {
        instance.current.appendChild(script.current);
    }, []);

    useEffect(() => {
        for (const key in props) {
            if (props.hasOwnProperty(key)) {
                script.current[key] = props[key];
            }
        }
    });

    return <div ref={instance}/>;
}