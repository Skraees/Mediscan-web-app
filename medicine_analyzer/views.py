from django.shortcuts import render
from .forms import UploadImageForm
from PIL import Image
import easyocr
import google.generativeai as genai

# Configure the Gemini API
AI_API_KEY = "AIzaSyDorVjZBGg9-MKYP11AHHHg6yzyQw8JdAI"  # Replace with your actual API key
genai.configure(api_key=AI_API_KEY)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def analyze_medicine(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Retrieve the uploaded image
            image_file = form.cleaned_data['image']
            image = Image.open(image_file)

            # Perform OCR on the image
            result = reader.readtext(image)
            extracted_text = " ".join([text[1] for text in result])

            # Prepare prompt for AI analysis
            prompt = f"Analyze the following text from a medicine package and give use cases, prescriptions, and details only  in 300word and in bullet point and dont use # ,*  and response should be in structure format like when any subheading start then use : and for every new heading or subheadimg start with new line dont use * and #.\nText: {extracted_text}"
            
            # AI Configuration
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 300,
                "response_mime_type": "text/plain",
            }
            
            # Create chat session with the Gemini API
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )
            chat_session = model.start_chat(history=[])

            # Send extracted text to the AI model
            response = chat_session.send_message(prompt)

            # Extract AI response or handle errors
            ai_response_text = response.text if response else "Error: No response received from the AI model."

            # Pass the results to the template for display
            context = {
                'form': form,
                'extracted_text': extracted_text,
                'ai_response_text': ai_response_text
            }
            return render(request, 'result.html', context)
    
    # If GET request, render the form
    else:
        form = UploadImageForm()
    
    return render(request, 'upload.html', {'form': form})
