from flask import Flask, render_template ,redirect,request
import caption_it
#__name__=__main__
app=Flask(__name__)




@app.route('/')
def hello():
    return render_template('index.html')
    
@app.route('/s',methods=['POST'])
def image_caption():
	if request.method=="POST":
		fi=request.files['userfile']
		path='./static/{}'.format(fi.filename)
		fi.save(path)
		
		#f=request.form['hou']
		#caption=str(f)
		caption=caption_it.final_caption(path)

	#return render_template('index.html',your_caption=caption)
	return "<h2> {}".format(caption)

if __name__=="__main__":
    app.run(debug=False,threaded=False)