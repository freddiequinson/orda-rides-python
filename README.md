# OrDa Rides Python

A Python-based web application for the OrDa Rides motorcycle ride-sharing service in Adeiso, Ghana. This app provides a more stable alternative to the React-based implementation.

## Features

- **Ride Booking**: Book motorcycle rides with local riders
- **Map Integration**: Select pickup and destination locations directly on the map
- **Active Ride Tracking**: View and manage your active rides
- **Rider Selection**: Choose from available riders based on ratings, distance, and price

## Setup Instructions

### Local Development

1. **Install Python Dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```
   python app.py
   ```

3. **Access the Application**:
   Open your web browser and navigate to `http://localhost:5000`

### Deployment to Render

1. **Sign up for Render**:
   Create an account at [render.com](https://render.com)

2. **Create a New Web Service**:
   - Click on "New" and select "Web Service"
   - Connect your GitHub repository or upload your code directly

3. **Configure the Web Service**:
   - Name: `orda-rides` (or your preferred name)
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Select the Free plan

4. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

5. **Access Your Deployed App**:
   - Once deployment is complete, Render will provide a URL to access your app
   - Share this URL with others to access the app on their phones

## Project Structure

- `app.py`: Main Flask application file
- `templates/`: HTML templates for the web pages
- `static/`: Static files (CSS, JavaScript, images)
  - `css/`: Stylesheets
  - `js/`: JavaScript files
  - `img/`: Images

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Maps**: Leaflet.js
- **Session Management**: Flask Session

## About OrDa Rides

OrDa Rides is a mobile web app designed for the Ghanaian community in Adeiso, providing motorcycle ride-sharing services and food ordering from local shops. The app aims to improve transportation options in rural areas with limited access to traditional taxi services.
