import pathlib
import subprocess
from collections import defaultdict
import logging
from tempfile import NamedTemporaryFile

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
            groups[group_name].add(file)
        return groups

    def process(self):
        groups = self._get_file_groups(self.in_path)
        logger.info(f'found {len(groups)} group(s) -- {list(groups.keys())}')

        for group_name, group in groups.items():
            output = pathlib.Path(self.out_path).joinpath(f'{group_name}_joined.mp4')
            self._join(group_name, group, output)

    @staticmethod
    def _join(name: str, inputs: [pathlib.Path], output: pathlib.Path):
        logger.info(f'joining group {name} -- {len(inputs)} parts found.')
        if output.exists():
            output.unlink()

        with NamedTemporaryFile(mode='w+') as manifest:
            lines = [f"file '{file.absolute()}'" for file in inputs]
            lines.sort()
            lines = '\n'.join(lines)
            manifest.write(lines)
            manifest.flush()
            subprocess.run(f'ffmpeg -safe 0 -f concat -i {manifest.name} -c copy {output}', shell=True)
