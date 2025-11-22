# FaunaVision Frontend

Modern React frontend for FaunaVision - AI-powered animal health monitoring system.

## Features

- ✅ **Multiple Enclosures**: Manage multiple animal enclosures simultaneously
- ✅ **Video Upload**: Drag-and-drop or click to upload videos
- ✅ **Animal Parameters**: Input species, age, diet, and health conditions
- ✅ **Real-time Analysis**: Connect to backend API for health assessment
- ✅ **Beautiful UI**: Modern, responsive design with gradient themes
- ✅ **Ready for Model Integration**: Prepared for when your CV model is ready

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API URL (Optional)

Create a `.env` file in the `frontend` directory:

```bash
REACT_APP_API_URL=http://localhost:5000
```

If not set, it defaults to `http://localhost:5000`.

### 3. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

## Usage

### Adding Enclosures

1. Click the "Add New Enclosure" button at the bottom
2. Each enclosure can be collapsed/expanded
3. Remove enclosures (minimum 1 required)

### Analyzing Animal Health

1. **Enter Animal Information**:
   - Species (required)
   - Age (optional)
   - Diet (optional)
   - Health Conditions (optional)

2. **Upload Video**:
   - Click the upload area or drag and drop
   - Supported formats: MP4, AVI, MOV, MKV
   - Maximum size: 100MB

3. **Analyze**:
   - Click "🔍 Analyze Animal Health" button
   - Wait for analysis to complete
   - View results including health status, reasoning, and recommendations

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Enclosure.js          # Main enclosure component
│   │   ├── AnimalParameters.js   # Animal info input form
│   │   ├── VideoUpload.js        # Video upload component
│   │   ├── AnalysisResults.js   # Results display
│   │   └── AddEnclosureButton.js
│   ├── App.js                   # Main app component
│   ├── App.css                  # Main styles
│   ├── index.js                 # Entry point
│   └── index.css                # Global styles
├── package.json
└── README.md
```

## API Integration

The frontend connects to the backend API at `/analyze` endpoint:

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `video`: Video file
  - `species`: Animal species
  - `age`: Animal age
  - `diet`: Animal diet
  - `health_conditions`: Existing health conditions

**Response:**
```json
{
  "species": "bear",
  "behavior_observed": "walking the dog",
  "length_seconds": 93.09,
  "length_minutes": 1.55,
  "is_repeating": true,
  "is_healthy": false,
  "reasoning": "...",
  "recommendations": "...",
  "confidence": 0.7172
}
```

## Model Integration (Future)

When your CV model is ready, the backend will automatically use it. The frontend doesn't need changes - it will receive the same response format with improved behavior detection.

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Troubleshooting

### Backend Connection Issues

- Make sure the backend server is running on `http://localhost:5000`
- Check the browser console for CORS errors
- Verify `REACT_APP_API_URL` in `.env` matches your backend URL

### Video Upload Issues

- Check file size (max 100MB)
- Verify file format (MP4, AVI, MOV, MKV)
- Check browser console for errors

## Technologies Used

- **React 18**: UI framework
- **Axios**: HTTP client (for future use)
- **CSS3**: Modern styling with gradients and animations
- **HTML5**: Video upload and drag-and-drop

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

