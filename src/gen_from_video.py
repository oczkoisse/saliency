import cv2
import sys
import bms
import os.path
import os
import argparse

def cleanup_dir(dest):
    """
    Cleanups the destination directory by removing all files in it, but ignoring the sub-directories
    :param dest: the destination directory
    :return: None
    """
    if not os.path.exists(dest):
        return
    files = os.listdir(dest)
    for f in files:
        fullpath = os.path.join(dest, f)
        if os.path.isfile(fullpath):
            try:
                os.remove(fullpath)
            except OSError:
                print "Cannot remove {}".format(fullpath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process a video to generate Boolean map based saliency maps as images')
    parser.add_argument('src', help='path to the input video')
    parser.add_argument('dest', help='output directory to store saliency map images')
    parser.add_argument('--display', default=False, type=bool, help='display the saliency maps in a window as generated')
    args = parser.parse_args(sys.argv[1:])

    if not os.path.exists(args.dest):
        try:
            os.mkdir(args.dest)
        except OSError:
            print "Cannot create output directroy: {}".format(args.dest)

    cleanup_dir(args.dest)
    fc = 0
    cap = cv2.VideoCapture(args.src)
    b = None
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            if not b:
                b = bms.BMS(frame)
            else:
                b.refresh(frame)
        else:
            break

        sm = b.get_saliency_map()
        # Display the resulting frame
        if args.display:
            cv2.imshow('frame', sm)

        cv2.imwrite(os.path.join(args.dest, str(fc) + '.jpg'), sm)
        fc += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()