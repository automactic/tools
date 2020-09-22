import logging
import pathlib
import subprocess
from collections import defaultdict
from tempfile import NamedTemporaryFile
from typing import Set

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GoProFileJoiner:
    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path

    @staticmethod
    def _get_file_groups(dir: str) -> [set]:
        groups = defaultdict(set)
        files = [file for file in pathlib.Path(dir).glob('**/*') if file.is_file()]
        for file in files:
            group_name = file.name.split('.')[0][-3:]
            if not group_name:
                continue
            if file.suffix.lower() != '.mp4':
                continue
            groups[group_name].add(file)
        return groups

    def process(self):
        groups = self._get_file_groups(self.in_path)
        group_names = sorted(groups.keys())
        logger.info(f'found {len(group_names)} group(s) -- {group_names}')

        for group_name in group_names:
            group = groups[group_name]
            output = pathlib.Path(self.out_path).joinpath(f'{group_name}_joined.mp4')
            self._join(group_name, group, output)

    @staticmethod
    def _join(name: str, inputs: Set[pathlib.Path], output: pathlib.Path):
        if inputs:
            logger.info(f'joining group {name} -- {len(inputs)} parts found.')
        else:
            logger.info(f'skipping group {name} -- {len(inputs)} parts found.')
            return

        if output.exists():
            output.unlink()

        inputs = sorted([file.absolute() for file in inputs])
        with NamedTemporaryFile(mode='w+') as manifest:
            lines = [f"file '{file}'" for file in inputs]
            manifest.write('\n'.join(lines))
            manifest.flush()
            subprocess.run([
                '/usr/local/bin/ffmpeg',
                '-safe', '0',
                '-f', 'concat',
                '-i', manifest.name,
                '-c', 'copy',
                output
            ])
            subprocess.run([
                'touch',
                '-r',
                inputs[0],
                output,
            ])
