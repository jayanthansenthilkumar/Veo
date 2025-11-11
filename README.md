# 🤖 Gen AI Platform

A comprehensive AI content generation platform powered by Google's Gemini AI models. Create stunning images, cinematic videos, and original music compositions using state-of-the-art AI technology.

![Gen AI Platform](https://img.shields.io/badge/AI-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🎨 Image Generation
- Generate high-quality images using Google's **Imagen 4.0**
- Create up to 4 images simultaneously
- Detailed text-to-image prompts
- Download and share generated images

### 🎬 Video Generation
- Create cinematic videos with Google's **Veo 3.1**
- Support for 720p and 1080p resolutions
- Negative prompts for better control
- Long-form video generation capabilities

### 🎵 Music Composition
- Generate original music with Google's **Lyria**
- Multiple weighted prompts for style blending
- Customizable BPM, temperature, and duration
- Real-time music generation

### 📊 Additional Features
- **Generation History**: Track all your creations
- **SQLite Database**: Persistent storage of generations
- **Responsive Design**: Works on all devices
- **Modern UI**: Beautiful gradient-based interface
- **RESTful API**: Easy integration and automation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google AI API Key ([Get one here](https://ai.google.dev/))
- pip (Python package installer)

### Installation

1. **Clone or navigate to the repository**
   ```powershell
   cd "c:\Users\jayan\OneDrive\Desktop\Veo"
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```powershell
   # Copy the template
   copy .env.template .env
   
   # Edit .env and add your Google AI API key
   notepad .env
   ```

5. **Initialize the database**
   ```powershell
   python -c "from app import app, init_db; app.app_context().push(); init_db()"
   ```

6. **Run the application**
   ```powershell
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
Veo/
├── agents/                    # AI agent modules
│   ├── __init__.py
│   ├── image_agent.py        # Image generation logic
│   ├── video_agent.py        # Video generation logic
│   └── music_agent.py        # Music generation logic
├── static/                    # Static files
│   ├── css/
│   │   └── style.css         # Main stylesheet
│   └── js/
│       └── main.js           # Client-side JavaScript
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Home page
│   ├── image_generator.html  # Image generation page
│   ├── video_generator.html  # Video generation page
│   ├── music_generator.html  # Music generation page
│   └── history.html          # Generation history
├── uploads/                   # User uploads (created automatically)
├── outputs/                   # Generated content (created automatically)
│   ├── images/
│   ├── videos/
│   └── music/
├── app.py                     # Main Flask application
├── database.py                # Database models
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── .env.template             # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🎯 Usage Guide

### Image Generation

1. Navigate to **Images** page
2. Enter a detailed description of the image you want
3. Select number of images (1-4)
4. Click **Generate Images**
5. Download or share your creations

**Example Prompt:**
```
A serene mountain landscape at sunset with a crystal-clear lake 
reflecting golden clouds, surrounded by pine forests and snow-capped peaks
```

### Video Generation

1. Navigate to **Videos** page
2. Describe the video scene in detail
3. Optionally add negative prompts
4. Select resolution (720p or 1080p)
5. Click **Generate Video**
6. Wait for processing (2-10 minutes)
7. Download your video

**Example Prompt:**
```
A drone shot following a red convertible along a winding coastal road 
at sunset, waves crashing against the rocks below. The car accelerates 
and the engine roars loudly.
```

### Music Generation

1. Navigate to **Music** page
2. Add one or more music style prompts
3. Adjust BPM (60-180)
4. Set creativity level (temperature)
5. Choose duration (10-120 seconds)
6. Click **Generate Music**
7. Listen and download

**Example Prompts:**
- Piano (weight: 2.0)
- Jazz (weight: 1.5)
- Upbeat (weight: 1.0)

## 🔧 Configuration

### Environment Variables

Edit `.env` file with your settings:

```env
# Required
GOOGLE_API_KEY=your-api-key-here

# Optional
SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=1
HOST=0.0.0.0
PORT=5000
```

### Advanced Configuration

Modify `config.py` to customize:
- Generation limits
- Default parameters
- Upload restrictions
- Session settings
- Rate limiting

## 🌐 API Endpoints

### Generate Image
```http
POST /api/generate-image
Content-Type: application/json

{
  "prompt": "A beautiful sunset",
  "num_images": 2
}
```

### Generate Video
```http
POST /api/generate-video
Content-Type: application/json

{
  "prompt": "A cinematic scene",
  "negative_prompt": "blurry, low quality",
  "resolution": "720p"
}
```

### Generate Music
```http
POST /api/generate-music
Content-Type: application/json

{
  "prompts": [
    {"text": "Piano", "weight": 1.5},
    {"text": "Jazz", "weight": 1.0}
  ],
  "bpm": 120,
  "temperature": 1.0,
  "duration": 30
}
```

### Get Statistics
```http
GET /api/stats
```

### Get Generation Details
```http
GET /api/generations/{generation_id}
```

## 🎨 Customization

### Styling

The platform uses CSS custom properties for easy theming. Edit `static/css/style.css`:

```css
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --accent: #ec4899;
    /* Add your colors */
}
```

### Adding Features

1. **New Agent**: Create a new agent class in `agents/`
2. **New Route**: Add endpoint in `app.py`
3. **New Template**: Create HTML in `templates/`
4. **Update UI**: Modify CSS/JS in `static/`

## 📊 Database Schema

### Generations Table
- `id`: Unique identifier (UUID)
- `type`: Generation type (image/video/music)
- `prompt`: User prompt
- `parameters`: JSON parameters
- `output_path`: File location
- `status`: Generation status
- `created_at`: Timestamp

### Users Table
- `id`: User identifier
- `username`: Username
- `email`: Email address
- `created_at`: Registration date

## 🐛 Troubleshooting

### API Key Issues
```
Error: Authentication failed
Solution: Check your GOOGLE_API_KEY in .env file
```

### Database Errors
```
Error: Database not found
Solution: Run: python -c "from app import app, init_db; app.app_context().push(); init_db()"
```

### Port Already in Use
```
Error: Address already in use
Solution: Change PORT in .env or kill the process using port 5000
```

### Module Import Errors
```
Error: No module named 'google.genai'
Solution: pip install -r requirements.txt
```

## 🚀 Deployment

### Production Setup

1. **Set environment to production**
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=0
   ```

2. **Use a production server**
   ```powershell
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Set up HTTPS** (recommended)

4. **Configure firewall** and security settings

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```powershell
docker build -t genai-platform .
docker run -p 5000:5000 --env-file .env genai-platform
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- **Google AI** for providing the Gemini API
- **Flask** for the web framework
- **Font Awesome** for icons
- All contributors and users

## 📧 Support

For support, email your-email@example.com or open an issue on GitHub.

## 🔮 Roadmap

- [ ] User authentication and accounts
- [ ] Image-to-video generation
- [ ] Video extension/editing features
- [ ] Music visualization
- [ ] Batch generation
- [ ] API rate limiting dashboard
- [ ] Advanced prompt templates
- [ ] Generation analytics
- [ ] Export to various formats
- [ ] Social sharing integration

## ⚡ Performance Tips

1. **Optimize prompts**: Be specific and detailed
2. **Use appropriate resolutions**: Higher quality = longer generation time
3. **Batch similar requests**: Generate multiple images at once
4. **Monitor API usage**: Keep track of your quota
5. **Cache results**: Save generated content for reuse

---

**Built with ❤️ using Google Gemini AI**

For more information, visit [Google AI Developer Documentation](https://ai.google.dev/)
