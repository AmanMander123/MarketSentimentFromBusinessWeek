#Market Sentiment using Business Week archives

##Purpose
The purpose of this program is to create a visualization comparing historical market sentiment alongside the performance of the S&P 500. The hypothesis is that the market sentiment will correlate with market performance.

##Method
This python program scrapes the data from the Business Week archives. All the words in the headline and the article text are analyzed. The words are commpared to the sentiment file (reference below) and a score is tabulated for each month.

##Note
As can be seen from the plot, the correlation is there but not satisfactory. The methods used to determine sentiment will need to be refined further. 

##Next steps
A more detailed analysis will be conducted using the Natural Language ToolKit for Python.

##Sentiment File used
Finn Årup Nielsen

"A new ANEW: Evaluation of a word list for sentiment analysis in microblogs",

Proceedings of the ESWC2011 Workshop on 'Making Sense of Microposts':

Big things come in small packages 718 in CEUR Workshop Proceedings : 93-98. 2011 May.

http://arxiv.org/abs/1103.2903


