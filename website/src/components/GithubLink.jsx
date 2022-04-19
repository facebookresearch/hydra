/**
 * Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
 */

import React from "react";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

import {useActiveVersion} from "@theme/hooks/useDocs";

function createGitHubUrl(to) {
    const activeVersion = useActiveVersion();
    const versionToBaseUrl = useDocusaurusContext().siteConfig.customFields.githubLinkVersionToBaseUrl

    const version = activeVersion?.name ?? "current";
    const baseUrl = versionToBaseUrl[version];
    return baseUrl + to;
}

export default function GithubLink(props) {
    return (
        <Link
            {...props}
            to={createGitHubUrl(
                props.to,
            )}
            target="_blank"
        />
    );
}

export function ExampleGithubLink(props) {
    const text = props.text ?? "Example (Click Here)" 
    return (
        <GithubLink {...props}>
            <span>&nbsp;</span><img
                src={"https://img.shields.io/badge/-" + text + "-informational"}
                alt="Example (Click Here)"
            />
        </GithubLink>
    );
}
