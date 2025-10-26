# 🚀 AI EvolutionX Platform

Advanced AI Platform with Continuous Learning and Multi-Model Support

## ✨ Features

- 🤖 **15+ AI Models** - Ollama integration with multiple models
- 💬 **Real-time Chat** - Streaming responses with SSE
- 👤 **User Authentication** - JWT-based secure authentication
- 📊 **Dashboard** - Usage statistics and model selection
- 🎯 **Training System** - Continuous learning from conversations
- 💰 **Affiliate System** - Built-in referral program (20% commission)
- 💳 **Payment Integration** - Stripe ready (configurable)
- 📱 **Mobile App** - Android/iOS via Ionic Capacitor

## 🏗️ Architecture

### Backend (FastAPI)
- Python 3.12
- FastAPI + Uvicorn
- MongoDB (Motor async driver)
- JWT Authentication
- Ollama integration

### Frontend (React)
- React 18
- Vite
- TailwindCSS
- Lucide Icons
- Ionic Capacitor (for mobile)

## 🚀 Quick Start

### Prerequisites
```bash
# Required
- Python 3.12+
- Node.js 18+
- MongoDB
- Ollama with models installed
```

### Backend Setup
```bash
cd backend
pip3 install -r requirements.txt --break-system-packages

# Configure .env
cp .env.example .env
# Edit .env with your settings

# Start backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📱 Build Mobile App

### Android
```bash
cd frontend
npm run build
npx cap sync android
npx cap open android
```

### iOS
```bash
cd frontend
npm run build
npx cap sync ios
npx cap open ios
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_evolutionx
JWT_SECRET=your_secret_key
OLLAMA_HOST=http://localhost:11434
STRIPE_SECRET_KEY=sk_test_...
```

**Frontend**
```env
VITE_API_URL=http://localhost:8000
```

## 💳 Payment Plans

- **Free**: 100 messages/month
- **Pro**: $10/month - 5000 messages
- **Enterprise**: $50/month - Unlimited

## 🤝 Affiliate Program

- **Commission**: 20% per referred user
- **Minimum Payout**: $50
- **Lifetime Commissions**: Earn while user stays subscribed

## 📊 Available Models

- deepseek-coder-v2:236b
- deepseek-v3.1:671b
- llama3.1:70b
- qwen3:32b
- And 11 more...

## 🛠️ Tech Stack

**Backend**
- FastAPI
- MongoDB
- Ollama
- Stripe API
- JWT

**Frontend**
- React + Vite
- TailwindCSS
- Ionic Capacitor
- Lucide Icons

## 📝 License

MIT License - See LICENSE file

## 👥 Support

- Email: elgalatico2280@gmail.com
- Website: https://iaevolutionxm.asuscomm.com

## 🌟 Features Coming Soon

- [ ] Voice synthesis integration
- [ ] Image analysis with vision models
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features

---

Made with ❤️ by AI EvolutionX Team
