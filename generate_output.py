import os
import getopt, sys
import pandas as pd

options = "ha:o:d:"
long_options = ["help", "aggregation=", "output=", "device="]


def parse_arguments(arg):
    out_args = {
        'agg': 'mean',
        'out': 'output.csv',
        'dev': 'lenovo'
    }
    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                print("Usage: \n\tpython3 generate_output.py -a method -o output.csv\n")
                print("Method can be: \n\tmean, median, min, max, first, or last (Default: mean)")
                return out_args, True

            elif currentArgument in ("-a", "--aggregation"):
                out_args['agg'] = currentValue

            elif currentArgument in ("-o", "--output"):
                out_args['out'] = currentValue

            elif currentArgument in ("-d", "--device"):
                out_args['dev'] = currentValue

    except getopt.error as err:
        print(str(err))

    return out_args, False


def aggregate(method, data):
    if method == 'mean':
        return data.mean(), True
    elif method == 'median':
        return data.median(), True
    elif method == 'min':
        return data.min(), True
    elif method == 'max':
        return data.max(), True
    elif method == 'first':
        return data.first(), True
    elif method == 'last':
        return data.last(), True
    return data, False


def main(args):

    input_args, hlp = parse_arguments(args)

    if hlp:
        return

    # Reading the input files
    df_encode = pd.read_csv('Encoding/encoding.csv')
    df_complexity = pd.read_csv('Video complexity/complexity.csv')

    # Todo: Various Devices

    if os.path.exists('Decoding/decoding_{}.csv'.format(input_args['dev'])):
        df_decode = pd.read_csv('Decoding/decoding_{}.csv'.format(input_args['dev']))
        df_upscale = pd.read_csv('Decoding and upscaling/decoding_upscaling_{}.csv'.format(input_args['dev']))
    else:
        print("The decoding device is not available!")
        return

    # Merge data
    df_ec = pd.merge(df_encode, df_complexity, on=['video']).reset_index(drop=True)

    df_ec = df_ec.groupby(['video', 'resolution', 'codec', 'framerate', 'qp', 'preset']).first()
    df_upscale = df_upscale.groupby(['video', 'resolution', 'codec', 'framerate', 'qp', 'preset'])
    df_decode = df_decode.groupby(['video', 'resolution', 'codec', 'framerate', 'qp', 'preset'])

    # Aggregation
    df_decode, success = aggregate(input_args['agg'], df_decode)
    df_upscale, success = aggregate(input_args['agg'], df_upscale)
    if not success:
        print("The aggregation method is not supported! Try to use: mean, median, min, max, first, or last")
        return

    df_ec.columns = [c + '_encode' for c in df_ec.columns]
    df_upscale.columns = [c + '_upscale' for c in df_upscale.columns]
    df_decode.columns = [c + '_decode' for c in df_decode.columns]

    # Concat dataframes
    df_total = pd.concat([df_ec, df_decode, df_upscale], axis=1, join='inner').reset_index()

    # Write to file
    df_total.to_csv('{}'.format(input_args['out']), index=False)


if __name__ == "__main__":
    argumentList = sys.argv[1:]
    main(argumentList)
