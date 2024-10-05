"""
use obspy to convert mseed to wav, then ffmpeg to conver wav to flac
"""

import os
import obspy
import glob

def mseed2flac(filenames):
    # resolve wildcard characters
    print(filenames)
    if type(filenames)==str:
        if '*' in filenames:
            filenames = glob.glob(filenames, recursive=True)
    else:
        if len(filenames)==1:
            if '*' in filenames[0]:
                filenames = glob.glob(filenames[0], recursive=True)

    print(filenames)
    print('here')
    for filename in filenames:
        print(filename)
        if not(filename.endswith('mseed')):continue
        print(filename)
        try:
            st = obspy.read(filename)
            st.write(filename.replace('mseed','wav'), format='WAV')
            # by default say no to overwrite
            os.system('ffmpeg -n -i '+filename.replace(' ', '\ ').replace('mseed','wav')+' -c:a flac '+filename.replace(' ', '\ ').replace('mseed','flac'))
            os.system('rm '+filename.replace(' ', '\ ').replace('mseed','wav'))
            os.system('rm '+filename.replace(' ', '\ ')) # also remove mseed file

        except:
            print('Failed to convert '+filename)
            continue

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filenames", nargs='+', type=str,
        help="Directory where mseed files are stored",
    )

    args = parser.parse_args()

    mseed2flac(args.filenames)