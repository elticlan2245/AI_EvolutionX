# 🤖 AI EvolutionX Platform

Plataforma profesional de IA con soporte multi-modelo, aprendizaje continuo y sistema de afiliados.

## ✨ Features

### 🎯 Core Features
- ✅ Chat inteligente con múltiples modelos de IA
- ✅ Soporte para Claude 3.5 Sonnet, GPT-4, Gemini Pro, y modelos locales (Ollama)
- ✅ Sistema de autenticación completo
- ✅ Aprendizaje continuo y personalización
- ✅ Historial de conversaciones
- ✅ Interface responsive (Web + Mobile)

### 💰 Monetización
- ✅ Sistema de planes (Free, Pro, Enterprise)
- ✅ Programa de afiliados con 20% de comisión
- ✅ Dashboard con métricas y analytics
- ✅ Comparador de modelos IA

### 🔧 Tech Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- React Router
- Capacitor (Android/iOS)

**Backend:**
- FastAPI (Python)
- MongoDB
- JWT Authentication
- Multi-provider AI system

**AI Providers:**
- Anthropic Claude
- OpenAI GPT
- Google Gemini
- Ollama (local models)

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- MongoDB
- Ollama (optional, for local models)

### Installation
```bash
# Clone
git clone https://github.com/elticlan2245/ai-evolutionx.git
cd ai-evolutionx

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python -m uvicorn app.main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev
```

### Environment Variables

Create `backend/.env`:
```env
MONGODB_URL=mongodb://localhost:27017
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## 📱 Build Android APK
```bash
npm run build
npx cap sync android
npx cap open android
```

## 📊 Pricing Plans

### Free
- 100 messages/month
- Ollama models only
- Basic support

### Pro ($10/month)
- 5,000 messages/month
- Claude 3 Haiku
- GPT-3.5 Turbo
- Gemini Pro
- Priority support

### Enterprise ($50/month)
- Unlimited messages
- Claude 3.5 Sonnet
- GPT-4 Turbo
- All premium models
- 24/7 support
- Custom integrations

## 🤝 Affiliate Program

Earn 20% lifetime commission on all referrals. No limits, no expiration.

## 📄 License

Proprietary - © 2024 AI EvolutionX

## 🔗 Links

- Website: https://iaevolutionxm.asuscomm.com
- Documentation: Coming soon
- Support: support@aievolutionx.com

## 👨‍💻 Author

Built with ❤️ by [Your Name]
