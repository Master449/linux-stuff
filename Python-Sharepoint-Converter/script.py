from bs4 import BeautifulSoup
import markdownify
import os

# This needs these pip packages to work
#    beautifulsoup4
#    launchpadlib
#    markdownify
#
# or do pip install -r requirements.txt

inputPath = "InputFiles/"
outputPath = "Output/"
inputFileEx = ".html"
outputFileEx = ".md"

for file in os.listdir(inputPath):
    if file.endswith(inputFileEx):
        HTMLFile = open(inputPath + file, "r")
  
        index = HTMLFile.read()
  
        webPage = BeautifulSoup(index, "html.parser")
        slimmedHTML = webPage.find("div", {"class": "ms-rte-layoutszone-inner"})
        
        parsedPage = markdownify.markdownify(str(slimmedHTML), heading_style="ATX")
  
        f = open(outputPath + file + outputFileEx, "w")
        f.write(str(parsedPage))
        f.close()

