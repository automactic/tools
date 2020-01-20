import pathlib
import subprocess
from tempfile import NamedTemporaryFile

if __name__ == '__main__':
    dir = '/Volumes/movie/Plum/'
    output_path = '/Users/chrisli/Movies/PlumIsland.mp4'

    output = pathlib.Path(output_path)
    if output.exists():
        output.unlink()

    with NamedTemporaryFile(mode='w+') as manifest:
        files = [file for file in pathlib.Path(dir).glob('**/*') if file.is_file()]
        lines = [f"file '{file.absolute()}'" for file in files]
        lines.sort()
        print(lines)
        lines = '\n'.join(lines)
        manifest.write(lines)
        manifest.flush()

        subprocess.run(f'ffmpeg -safe 0 -f concat -i {manifest.name} -c copy {output_path}', shell=True)
