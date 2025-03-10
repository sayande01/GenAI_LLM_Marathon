# 🏥 Healthcare Assistant Chatbot

## 🌟 Modern AI-Powered Health Guidance Platform

A visually stunning, AI-powered healthcare assistant built with Streamlit and Google's Gemini Pro model. This application provides informative guidance on health and wellness topics in an interactive, user-friendly interface.

## ✨ Features

- **Topic-Based Health Information**: Browse and select from various health categories including General Health, Nutrition, Fitness, Mental Health, and more
- **Interactive Chat Interface**: Engage in natural conversations with an AI assistant specifically trained on healthcare information
- **Visually Stunning UI**: Enjoy a modern, intuitive interface with beautiful animations and responsive design
- **Expert Health Guidance**: Receive evidence-based information referencing reputable health organizations
- **Personalized Experience**: Explore different health topics with specialized information for each category

## 🎯 Demo Experience

```
👤 User: What foods are good sources of omega-3 fatty acids and why are they important?

🥗 Healthcare Assistant: Omega-3 fatty acids are essential fats that provide numerous health benefits. 
Here are excellent food sources:

1. Fatty fish (salmon, mackerel, sardines, tuna)
2. Walnuts
3. Flaxseeds and flaxseed oil
4. Chia seeds
5. Hemp seeds
6. Algae and algal oil (great for vegetarians)
7. Fortified foods (eggs, yogurt, milk)

Omega-3s are important because they:
- Support heart health by reducing inflammation and triglycerides
- Promote brain health and cognitive function
- May help reduce symptoms of depression and anxiety
- Support eye health and visual development
- Help maintain healthy joints and reduce arthritis symptoms

For optimal health benefits, aim to include omega-3 rich foods in your diet regularly.
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google API key for Gemini models

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/healthcare-assistant.git
   cd healthcare-assistant
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key
   ```bash
   export GOOGLE_API_KEY='your-api-key-here'
   ```

4. Run the application
   ```bash
   streamlit run enhanced-healthcare-chatbot-v2.py
   ```

## 💻 Usage

1. Select a health topic from the sidebar to focus your conversation
2. Type your health question in the input field
3. Receive informative responses from the AI assistant
4. Continue the conversation with follow-up questions

## 🌟 Health Categories

| Category | Description |
|----------|-------------|
| 🏥 General Health | Preventive care and wellness advice |
| 🔍 Symptoms & Conditions | Information about common symptoms and conditions |
| 🥗 Nutrition | Dietary guidance and healthy eating habits |
| 💪 Fitness | Exercise recommendations and physical activity tips |
| 🧠 Mental Health | Mental wellbeing and stress management |
| 💊 Medications | Information about common medications |
| 🚑 First Aid | Basic emergency response guidance |
| 😴 Sleep Health | Tips for better sleep habits |

## ⚠️ Disclaimer

This application provides general health information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## 🧰 Technology Stack

- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **AI Model**: [Google Gemini Pro](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini) via LangChain
- **Styling**: Custom CSS with responsive design
- **Animation**: CSS keyframe animations for enhanced user experience

## 📊 UI Elements

```
┌────────────────────────────────────────────────────┐
│ 🏥 HEALTHCARE ASSISTANT                            │
├────────────────────────────────────────────────────┤
│ Select a Health Topic:                             │
│ ┌──────────────────────────────────────────────┐   │
│ │ 🏥 General Health                            │   │
│ │ 🔍 Symptoms & Conditions                     │   │
│ │ 🥗 Nutrition                                 │   │
│ │ 💪 Fitness                                   │   │
│ │ 🧠 Mental Health                             │   │
│ │ 💊 Medications                               │   │
│ │ 🚑 First Aid                                 │   │
│ │ 😴 Sleep Health                              │   │
│ └──────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the fantastic web app framework
- [Google](https://cloud.google.com/) for the Gemini Pro API
- [LangChain](https://www.langchain.com/) for AI integration tools
- All the contributors who have helped improve this project

---

<p align="center">
  Made with ❤️ for a healthier world
</p>
