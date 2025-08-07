from flask import Flask, render_template, request, jsonify
import os
import PIL.Image
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('Auth.html')

@app.route('/bunker')
def bunker():
    return render_template('bunker.html')

@app.route('/old')
def old():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "error"
    
    file = request.files['image']
    
    if file.filename == '':
        return "error"
    
    if file:
        # Save the file to the server
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Analyze the image and get the result
        result = getSubject(filename).strip()
        
        # Return the result as a JSON response
        print(result)
        return result


def getSubject(image):
    try:  
        genai.configure(api_key="AIzaSyDU5Ka51cReNkDqMBS-grM-WOHlHNaCmp0")

        # Create the model
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 500,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an Image Detector. When you see an image, if it contains only zombie(s), respond with \"Zombie\", if it contains only human(s), respond with \"Human\", if it contains both, respond with \"Both\", and if it contains neither, reply with \"Neither\", reply with \"not understood\", if image was not viewed.\n",
        )
        
        file = PIL.Image.open(image)
        
        chat_session = model.start_chat(
            history=[]
        )
        prompt = "What is this"
        response = model.generate_content([prompt, file,])
        
        return response.text
    except Exception as e:
        return f"Error processing the image: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
