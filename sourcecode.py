import PyPDF2
from gtts import gTTS
import pygame
from pygame import mixer
from PIL import Image
import pytesseract
import os
import glob
import PySimpleGUI as sg
import tkinter as tk
import fitz



# In this function we get first and last page, which we want the software to read
def get_text(value):

    string = value
    string = string.strip()
    if "-" in string:
        first_page_number = int(string.split("-")[0])
        last_page_number = int(string.split("-")[1])
    else:
        first_page_number = int(string)
        last_page_number = 0

    return first_page_number,last_page_number

def main():
    global e,first_page_number,last_page_number
    ##### Create directory for Text to speech software
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory,r'Text_to_speech_software')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    print(current_directory)
    print(final_directory)

    #### GUI Part #####

    # All the stuff inside your window.
    layout = [  [sg.Text('Choose PDF File to read'),sg.Input(),sg.FileBrowse()],
                [sg.Text('Enter PDF Page number or range separated by - '), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]

    # Create the GUI Window Prompt
    window = sg.Window('Input', layout)
    valid = False
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        # Here we read the path of the pdf file
        pdf_to_read = values[0]

        if event in (None, 'Cancel'):	# if user closes window or clicks cancel
            print("Exitting")
            window.close()
            exit()

        if event == "Ok":

            if values[0] == "":
                sg.Popup("Enter value", "Enter PDF file to be transcribed ")
            if values[1] == "":
                sg.Popup("Enter value", "Enter page number(s) to be transcribed")

            if values[0]!="" and values[1]!="":
                for char in values[1]:
                    if char.isdigit()==False:
                        sg.Popup("Invalid value","Enter valid number or numbers separated by -")
                        break
                    else:
                        valid=True
                        break
        # Break while loop if valid first and last page numbers received
        if valid==True:
            print('You entered ', values[1])
            break

    window.close()
    first_page_number,last_page_number = get_text(values[1])

    # In this bunch of code, we get permission to delete the folder if it already exists, where we intend to save our PDF images and audio
    image_directory = glob.glob(final_directory)
    for file in os.listdir(final_directory):
        filepath = os.path.join(final_directory,file)
        print(filepath)
        os.chmod(filepath, 0o777)
        os.remove(filepath)

    # Here we read desired PDF pages and store them as images in a folder
    book = open('example.pdf', 'rb')
    out = open('output.txt', 'a')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    print("The number of pages in the pdf is: {}".format(pages))
    print("Your PDF is being processed...")
    for curr_page in range(0, pages):
        page = pdfReader.getPage(curr_page)
    text = page.extractText()
    out.write(text)
    out. close()

    print("Your Audibook is being created...")

    with open("output.txt") as file:
         file = file.read()

    speak = gTTS(file, lang='en')
    speak.save('audiobook.mp3')
    print("Successfully created the Audiobook")

    # Initialize the Pytesseract OCR software
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


    mytext = []

    # Here we load the image(s) created in Text_to_speech folder and read the text in image via pytesseract Optical Character Recognition (OCR) software
    # thus reading text in images and giving us a string
    for file in os.listdir(final_directory):
        data = pytesseract.image_to_string(Image.open(os.path.join(final_directory,file)),lang="eng")
        data = data.replace("|","I") # For some reason the image to text translation would put | instead of the letter I. So we replace | with I
        data = data.split('\n')
        mytext.append(data)


    # Language in which you want to convert
    language = 'en'

    print(mytext)

    # Here we make sure that the text is read correctly and we read it line by line. Because sometimes, text would end abruptly

    newtext= ""
    for text in mytext:
        for line in text:
            line = line.strip()
            # If line is small, ignore it
            if len(line.split(" ")) < 10 and len(line.split(" "))>0:
                newtext= newtext + " " + str(line) + "\n"

            elif len(line.split(" "))<2:
                pass
            else:
                if line[-1]!=".":
                    newtext = newtext + " " + str(line)
                else:
                    newtext = newtext + " " + line + "\n"

    print(newtext)



    # Here we load and play the audio file
    pygame.init()
    mixer.init()
    mixer.music.load("audiobook.mp3")
    mixer.music.play()
    pygame.event.wait()


    ########## GUI END ########

if __name__ == '__main__':
    main()
