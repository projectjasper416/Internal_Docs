# Internal Docs Q&A Agent - Frontend

This is the React frontend for the Internal Docs Q&A Agent, providing a modern, responsive chat interface for querying internal company documentation.

## Features

- Modern, responsive chat interface
- Real-time connection status with backend
- Message history with timestamps
- Source attribution for answers
- Loading animations and typing indicators
- Mobile-friendly design
- Accessibility features

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm start
```

The application will open at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Chatbot.js
│   │   ├── Chatbot.css
│   │   ├── Header.js
│   │   ├── Header.css
│   │   ├── Message.js
│   │   └── Message.css
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Components

### Chatbot
The main chat interface component that handles:
- Message display and history
- User input and submission
- Loading states
- Connection status

### Header
Navigation header with:
- Application title
- Backend connection status
- Navigation buttons

### Message
Individual message component with:
- User/bot message styling
- Timestamp display
- Source attribution
- Error message handling

## API Integration

The frontend communicates with the Flask backend through the `api.js` service:

- `healthCheck()` - Check backend connectivity
- `askQuestion(question)` - Send questions to the backend
- `indexDocuments()` - Trigger document indexing
- `getChatHistory()` - Retrieve chat history

## Styling

The application uses modern CSS with:
- CSS Grid and Flexbox for layout
- CSS custom properties for theming
- Responsive design with mobile-first approach
- Smooth animations and transitions
- Glassmorphism effects

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Environment Variables

- `REACT_APP_API_URL` - Backend API URL (defaults to http://localhost:5000)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Accessibility

- Keyboard navigation support
- Screen reader compatibility
- High contrast focus indicators
- Semantic HTML structure

## Performance

- Lazy loading of components
- Optimized bundle size
- Efficient re-rendering
- Debounced API calls 