/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
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