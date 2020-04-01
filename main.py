
import sys

def get_args():

    import sys
    args = {
        '-u': None,
        '-s':None,
        '-e':None,
        '-c':None,
        '-l':None

    }
    try:
        for i in range(1,len(sys.argv),2 ):
            args[sys.argv[i]] = sys.argv[i+1]
    except IndexError:
        print("invalid arguments")
        sys.exit(0)


    if args['-u'] is None:
        print("no url found, exiting")
        sys.exit(0)

    final_args = {'url': args['-u'], 'chapter':args['-c'], 'start':args['-s'], 'end':args['-e'], 'location':args['-l']}

    return final_args

if __name__=='__main__':
    import scrapper
    args = get_args()
    scrapper.download_manga(**args)

