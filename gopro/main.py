from gopro import GoProFileJoiner

if __name__ == '__main__':
    joiner = GoProFileJoiner('/Volumes/256GB_SD/DCIM/100GOPRO/', '/Users/chrisli/Movies')
    joiner.process()
