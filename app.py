from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div',attrs = {'class':'table-responsive'})

row=table.find_all('td', attrs={'class' : 'text-narrow-screen-hidden'})
row_length = len(row)

temp = [] #initiating a list 

for i in range(1, 130):
#insert the scrapping process here
     ##get 'the date' lisbt
    Date = table.find_all('td')[4*(i)-4].text
    
    #get 'the rate' list
    Rate = table.find_all('td')[4*(i)-2].text
    Rate_1 = Rate.strip()
    
    temp.append((Date,Rate_1))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns=('Date','Rate'))

#insert data wrangling here
df['Rate']=df['Rate'].str.replace('IDR','')
df['Rate']=df['Rate'].str.replace(',','')
df['Date'] = df['Date'].astype('datetime64')
df['Rate'] = df['Rate'].astype('float64')
df=df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (12,5)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)