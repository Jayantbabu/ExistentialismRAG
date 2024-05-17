from bs4 import BeautifulSoup
import zipfile
import os
import tempfile

tmpdirname = tempfile.mkdtemp()

def extract_text_from_epub(epub_path, output_txt_path):
    with zipfile.ZipFile(epub_path, 'r') as zf:
        zf.extractall(tmpdirname)
    
    text_content = []
    
    for dirname, _, filenames in os.walk(tmpdirname):
        for filename in filenames:
            if filename.endswith('.html') or filename.endswith('.xhtml'):
                filepath = os.path.join(dirname, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    text = soup.get_text(separator=' ', strip=True)
                    text_content.append(text)

    with open(output_txt_path, 'w', encoding='utf-8') as text_file:
        text_file.write('\n\n'.join(text_content))

# epub_path = './assets/Jean-Paul Sartre - Being and Nothingness (2021, Simon and Schuster) - libgen.li.epub'
# output_txt_path = './assets/Being_and_Nothingness_Extracted.txt'

# extract_text_from_epub(epub_path, output_txt_path)

for dirname, _, filenames in os.walk("./assets/Books"):
    for filename in filenames:
        if filename.endswith(".epub"):
            filepath = os.path.join(dirname,filename)
            output_txt_path = "./assets/Converted/"+filename[:-17]+".txt"
            extract_text_from_epub(filepath, output_txt_path)
            print("Done: "+ filename)