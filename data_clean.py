import re,os

for dirname, _, filenames in os.walk("./assets/Converted"):
    for filename in filenames:
        filepath = os.path.join(dirname,filename)
        print(filepath)
        with open(filepath, 'r', encoding='utf-8') as file:
            original_text = file.read()

        cleaned_text = re.sub(r'\n\d+\n', '\n', original_text)

        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        cleaned_text = re.sub(r'\.\s+', '.  ', cleaned_text)

        cleaned_text = re.sub(r'[\[\]\{\}]', '', cleaned_text)

        output_file_path = "./assets/Cleaned/"+filename[:-4]+"_cleaned.txt"
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        print(output_file_path)