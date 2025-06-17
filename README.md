#                                                          🚀 Smart-Learner — Personalized Study Assistant
**Smart‑Learner** is a Streamlit-based educational app that adapts to your learning style—Visual, Auditory, Reader/Writer, or Kinesthetic. It delivers tailored quizzes, explanations, videos, simulations, and physical activities to make learning truly interactive and fun.

## ⚙️ Getting Started
### Prerequisites
- Python 3.8+  
- YouTube API Key (for Visual mode)  
- (Optional) `.env` with `GEMINI_API_KEY` (for AI features)(check out requirements.txt tab)


📚 Usage


Run the app locally:

bash


Copy this -->
streamlit run app.py
![WhatsApp Image 2025-06-16 at 21 14 17_67667b0b](https://github.com/user-attachments/assets/7fa0deff-c184-47bf-a6aa-fde5e8b7ef89)

Then:
Choose your language (English, Hindi, Tamil)



complete the 30 question just curated to find out ur type
![WhatsApp Image 2025-06-16 at 21 14 19_806f8e6c](https://github.com/user-attachments/assets/0a6ad989-3ebe-4d35-b6c8-60ca9a0a0065)
Upload a PDF, PPTX, or DOCX
![WhatsApp Image 2025-06-16 at 21 14 18_cd10389c](https://github.com/user-attachments/assets/0f7c99ca-2922-4694-ba85-42206a165095)

Get personalized resources and activities


🧩 How It Works


Text Extraction – Reads content from uploaded files


Learning Style Handling – Branches logic based on style


AI Integration – Uses Gemini AI for content generation and topic extraction


Mode-Specific Output  ⬇



Kinesthetic: Provides gestures and movement prompts
![WhatsApp Image 2025-06-16 at 23 08 53_b3c79019](https://github.com/user-attachments/assets/8f2518e7-ca10-48ad-aa21-4ed434119d6c)



Auditory: Launches Vapi-powered voice interface

demo video
    
    
check this out ---->auditory/listener



Reader/Writer: Offers interactive summaries and stories
![WhatsApp Image 2025-06-16 at 23 08 52_2b2a5b0a](https://github.com/user-attachments/assets/fe9ddf99-5911-4d32-b343-af9efcd5d7b4)
![WhatsApp Image 2025-06-16 at 23 08 52_7d214183](https://github.com/user-attachments/assets/6fd5aa1a-d14a-4999-b802-36f04b80a29e)



Visual: Embeds top YouTube videos 
![WhatsApp Image 2025-06-16 at 23 08 53_521dbd40](https://github.com/user-attachments/assets/e4a7646a-7df5-45f9-9e99-eb093a27128f)



💡 Learning Styles


 Visual – Auto-generated video resources


Auditory – Real-time voice-based tutor


Reader/Writer – Generates summaries, stories, explanations


Kinesthetic – Encourages movement, gestures, and physical interaction



Future works


-**Visual**: Suggests YouTube videos dynamically ,generates animations and videos,graphs and images


- **Auditory**: Embeds an interactive voice tutor that solves all the queries with very freat accuracy

- 
- **Reader/Writer**: Generates summaries, stories, explanations  and makes hard concepts into fiction story books

- 
- **Kinesthetic**: Offers physical prompts and gestures , simulations,anologies 
- Supports English, Hindi, and Tamil with built-in translations


🤝 Contributing

Want to help out? We'd love your input!


1)Fork the repo

2)Create your feature branch (git checkout -b feature/xyz)


3)Make your changes and test


4)Commit (git commit -m 'Add feature')
5)Push (git push origin feature/xyz)
6)Open a Pull Request
