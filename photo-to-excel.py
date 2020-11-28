import pandas as pd
import numpy as np
from PIL import Image
from openpyxl import load_workbook
import os

# Max size of the image
MAX_SIZE = 500*500

def rgb2hex(r, g, b):
    '''
    Converts rgb values to hex
    r (int) - red value of the pixel
    g (int) - green value of the pixel
    b (int) - blue value of the pixel
    return (str) - the hex value of the rgb color
    '''
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def image_to_df(filename):
    '''
    Converts image to a df of hex values of the pixels
    filename (str) - the name of the image file to be converted to excel
    return (pandas.DataFrame) - a DataFrame where each cell is the hex value of the color of that pixel
    '''
    img = Image.open(filename)
    pixels = np.array(img.convert('RGBA').getdata())

    as_hex = np.zeros(pixels.shape[0]).astype(str)
    for i in range(pixels.shape[0]):
        as_hex[i] = rgb2hex(pixels[i][0], pixels[i][1], pixels[i][2])
    
    reshaped = as_hex.reshape(img.size[1], img.size[0])

    # Shrink the image if it is too large
    factor = int(reshaped.size / MAX_SIZE)
    if factor > 0:
        scaled = reshaped[::factor, ::factor]
    else:
        scaled = reshaped

    as_df = pd.DataFrame(scaled)
    return as_df

def color_column(series):
    '''
    Gets styles for a Series based on the hex value in the cell
    Styles the DataFrame when used in the apply function
    series (pandas.Series) - a pandas.Series of hex values
    return (list) - a list of styles for each cell in the pandas.Series
    '''
    return ['background-color: ' + item for item in series]

def color_df(hex_df):
    '''
    Applies the color_column function to the DataFrame to color the cells
    hex_df (pandas.DataFrame) - a pandas.DataFrame filled with hex values
    return (pandas.Styler) - a stylized pandas.DataFrame where each cell is colored
    '''
    hex_df = hex_df.style.apply(color_column)
    return hex_df

def image_to_excel(img_filename):
    '''
    Converts an image to an excel file
    img_filename (str) - filename of an image
    return - None
    '''
    df = image_to_df(img_filename)
    colored = color_df(df)
    new_filename = filename + '.xlsx'
    colored.to_excel(new_filename, header=False, index=False)

    # Clear the text entries in the cells
    wb = load_workbook(new_filename)
    ws = wb['Sheet1']
    for row in ws:
        for cell in row:
            cell.value = None
    wb.save(new_filename)

if __name__ == '__main__':
    for filename in os.listdir():
        try:
            image_to_excel(filename)
        except:
            pass