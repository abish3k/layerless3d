from pySlice import slice_file

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Takes a 3D Model, and slices it at regular intervals')
    parser.add_argument('file',
                        metavar='FILE',
                        help='File to be sliced',
                        nargs='?',
                        default='../stl/bottle.stl',
                        type=argparse.FileType('rb'))
    parser.add_argument('-r', '--resolution', type=float,
                        default=1,
                        help='The Z-Axis resolution of the printer, in mms')

    args = parser.parse_args()
    slice_file(args.file, args.resolution)