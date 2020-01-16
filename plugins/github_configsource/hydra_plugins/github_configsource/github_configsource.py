# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import base64
import json
import urllib.request
from typing import Any, List, Optional
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse

from omegaconf import OmegaConf

from hydra.core.object_type import ObjectType
from hydra.plugins.config_source import ConfigLoadError, ConfigResult, ConfigSource


class GitHubConfigSource(ConfigSource):
    github_api: str = "https://api.github.com"

    def __init__(self, provider: str, path: str) -> None:
        super().__init__(provider=provider, path=path)
        res = urlparse(path)
        netloc = res.netloc.split(".")
        if len(netloc) != 2:
            raise ValueError(f"Invalid owner.repo segment : {res.netloc}")
        query = parse_qs(res.query)
        self.owner = netloc[0]
        self.repo = netloc[1]
        self.url_path = res.path
        if "ref" in query:
            refs = query.get("ref")
            assert refs is not None
            if len(refs) != 1:
                raise ValueError(f"Invalid too many ref query parameters : {query}")
            self.ref = refs[0]
        else:
            self.ref = "master"

    @staticmethod
    def scheme() -> str:
        return "github"

    def _get_url(self, config_path: str) -> str:
        return f"{self.github_api}/repos/{self.owner}/{self.repo}/contents{self.url_path}/{config_path}?ref={self.ref}"

    @staticmethod
    def _get_json_response(url: str) -> Any:
        request = urllib.request.Request(url=url)
        with urllib.request.urlopen(request) as response:
            if response.code != 200:
                raise URLError(f"Invalid response code : {response.code}")
            return json.loads(response.read())

    def load_config(self, config_path: str) -> ConfigResult:
        try:
            url = self._get_url(config_path)
            json_res = self._get_json_response(url)
            if json_res["type"] != "file":
                raise URLError(f"Unexpected object type : {json_res['type']}")
            cfg_str = bytes.decode(base64.decodebytes(str.encode(json_res["content"])))
            cfg = OmegaConf.create(cfg_str)
            return ConfigResult(
                config=cfg, path=self.get_source_path(), provider=self.provider,
            )
        except URLError as e:
            raise ConfigLoadError(
                f"GitHubConfigSource: Error loading config from url: {url} : {e}"
            )

    def exists(self, config_path: str) -> bool:
        return self.get_type(config_path) is not ObjectType.NOT_FOUND

    def get_type(self, config_path: str) -> ObjectType:
        try:
            url = self._get_url(config_path)
            return self._get_type(self._get_json_response(url))
        except URLError:
            return ObjectType.NOT_FOUND

    @staticmethod
    def _get_type(json_res: Any) -> ObjectType:
        if isinstance(json_res, list):
            return ObjectType.GROUP
        elif json_res["type"] == "file":
            return ObjectType.CONFIG
        else:
            raise ValueError(f"Unexpected object type : {json_res['type']}")

    def list(self, config_path: str, results_filter: Optional[ObjectType]) -> List[str]:
        try:
            ret: List[str] = []
            url = self._get_url(config_path)
            json_res = self._get_json_response(url)
            if self._get_type(json_res) == ObjectType.CONFIG:
                raise IOError(f"URL points to a file : {url}")
            elif self._get_type(json_res) == ObjectType.GROUP:
                for item in json_res:
                    file = item["name"]

                    if config_path != "":
                        file_path = f"{config_path}/{file}"
                    else:
                        file_path = file

                    self._list_add_result(
                        files=ret,
                        file_path=file_path,
                        file_name=file,
                        results_filter=results_filter,
                    )
            return sorted(ret)

        except URLError:
            return []
