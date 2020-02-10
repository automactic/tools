from gopro import GoProFileJoiner

if __name__ == '__main__':
    joiner = GoProFileJoiner('/Volumes/256GB_SD/DCIM/100GOPRO/mp4', '/Users/chrisli/Movies')
    joiner.process()
    # joiner.join(input_dir='/Users/chrisli/Movies/365', output_path='/Users/chrisli/Movies/365_joined.mp4')
