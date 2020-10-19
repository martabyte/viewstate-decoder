#!/usr/bin/python3

from viewstate import ViewState
import argparse
import urllib.parse

#Handling of command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-vs', dest='encoded_vs', help='Input Base64 ViewState')
parser.add_argument('-f', dest='vs_filename', help='Input File with Base64 ViewState')
parser.add_argument('-o', dest='output_filename', default='output_viewstate.txt', help='Name of the Output File with the Resulting ViewState')
args = parser.parse_args()

encoded_vs = ''

if(not args.encoded_vs and not args.vs_filename):
    print('ERROR: Input needed - Usage: viewstate-decoder.py [-h] [-vs ENCODED_VS] [-f VS_FILENAME] [-o OUTPUT_FILENAME]')
else:
    # Check if the input is given in the command line
    if (args.encoded_vs):
        encoded_vs = args.encoded_vs()
    else: # If not, we have the input inside a file with name: args.vs_filename
        input_file = open(args.vs_filename, 'r')
        encoded_vs = input_file.read()
        input_file.close()

        # Convert the URL encoded input into Base64 only (URL decode)
        encoded_vs = urllib.parse.unquote(encoded_vs) 
        
    #Create ViewState object
    vs = ViewState(encoded_vs)
    decoded_vs = vs.decode()
    hmac = vs.mac
    sign = vs.signature

    #Write to output file
    output_file = open(args.output_filename, 'w')
    output_file.write('Decoded Viewstate: 'str(decoded_vs)) # We must set it as 'string' to write it because it's a tuple, not a string
    output_file.write('\n ViewState HMAC Signature Type: ' + hmac)
    output_file.write('\n ViewState HMAC Signature: ' + str(sign))
    output_file.close()

    print('Output file saved to: '+ args.output_filename)
