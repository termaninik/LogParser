from collections import defaultdict
from pprint import pprint
from typing import Generator
from pathlib import Path

import json
import re
import ast


class IterLogFile:
    def __init__(self, file_path: str):
        self.__path = Path(file_path)

    def __iter__(self) -> Generator[str, None, None]:
        with self.__path.open(mode='r', encoding='utf-8', errors='replace') as f:
            for row in f:
                yield row.strip()


class ParseLogFile:
    def __init__(self, path: str):
        self.__path = path

    @staticmethod
    def __parse_a_string(row: str) -> tuple[str, str]:
        row = re.sub(r"ZoneCoordinates\(([^)]*)\)", r'"ZoneCoordinates(\1)"', row)

        device_id = row.split('|')[5].split(':')[0].strip()
        data = row.split('Analysis result: ')[1].strip()
        data = ast.literal_eval(data)

        return device_id, data

    def parse(self, pattern: str) -> None:
        _data = defaultdict(dict)
        _pattern = pattern

        with open('log.json', 'w') as file:
            for row in IterLogFile(self.__path):
                if _pattern in row:
                    device_id, data = self.__parse_a_string(row)

                    next_idx = len(_data[device_id]) + 1
                    _data[device_id][next_idx] = data

            file.write(json.dumps(_data, indent=2))

    def get_device_id(self, device_id: str):
        with open('log.json', 'r') as f:
            data = json.loads(f.read())

        return self.to_json(data[device_id])

    @staticmethod
    def to_json(obj: dict):
        return json.dumps(obj, indent=2)

    @staticmethod
    def to_python(obj: dict):
        pass


if __name__ == '__main__':
    t = ParseLogFile('AidisLog.log')
    t.parse(pattern='Analysis result:')
    print(t.get_device_id('30ce2a66'))
    print(t.get_device_id('30ce2a66'))
