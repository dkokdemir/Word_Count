# Word_Count
This repository contains a Word Cloud Generator web application, which allows users to upload text files and generate word clouds based on the text content. The application is built using Flask, a lightweight Python web framework, and leverages the WordCloud and NLTK libraries for text processing and visualization.

**Features**

Upload text files in various formats, including .txt, .rtf, .doc, .docx, and .pdf.
Customize word clouds by providing word mappings, omitting specific words, and choosing whether to include numbers.
Download word cloud images in .png format.
Download word frequency data as a .csv file.
A clean, minimalistic, and elegant user interface.

**Installation**

Prerequisites
Python 3.6 or newer
pip (Python package installer)

**Steps**

1. Clone this repository:
<code> git clone https://github.com/yourusername/word-cloud-generator.git
cd word-cloud-generator </code>

2. Create a virtual environment (optional, but recommended):
<code> python3 -m venv venv source venv/bin/activate  
...For Windows, use `venv\Scripts\activate`</code>

3. Install the required Python packages:
<code> pip install -r requirements.txt </code>

4. Run the application:
<code> python app.py </code>

5. Open your browser and go to http://localhost:5000 to access the Word Cloud Generator.

**Usage**
1. On the main page, click the "Choose File" button and select a text file from your computer.
2. (Optional) Enter word mappings in the "Word Mappings" field. Use the format original=replacement and separate multiple mappings with commas. Example: old=new, cat=dog.
3. (Optional) Enter words to omit in the "Omit Words" field. Separate multiple words with commas. Example: word1, word2, word3.
4. (Optional) Check the "Do you want to count numbers in the text?" box if you want to include numbers in the word cloud.
5. Click the "Submit" button to generate the word cloud.
6. The generated word cloud image will appear on the page, along with a download link for the word frequency data in CSV format.

**Contributing**

We welcome contributions to improve the Word Cloud Generator! Please feel free to submit issues for bug reports, feature requests, or general feedback. If you'd like to contribute code, please fork the repository, make your changes, and submit a pull request.

**Licence**
This project is licensed under the GNU General Public License (GPL) v3.0 License. See the LICENSE file for more information.
