# MarkTrack

## The Online Gradebook That Puts You in Control!

[![MarkTrack](https://i.imgur.com/mlbAbIc.png)](https://mark-track.vercel.app)

Welcome to **MarkTrack**, the next-level online gradebook designed to help students and teachers keep track of grades effortlessly! Built with a slick UI and cutting-edge technology, MarkTrack ensures you never miss a grade again.

### 🚀 Features

- **Real-time Grade Tracking:** Keep your grades updated in real-time with our seamless integration.
- **User-Friendly Interface:** Navigate through your academic life with ease.
- **Secure Data Handling:** Powered by Firebase, your data is secure and accessible only to you.
- **Fast and Responsive:** Built with FastAPI and Next.js for a lightning-fast experience.
- **Ready for Deployment:** Dockerized for easy deployment and scalability.
- **Future-Ready:** Redis integration planned for ultra-fast data retrieval.

### 🛠 Tech Stack

- **Frontend:** Next.js
- **Backend:** FastAPI
- **Database:** Firebase
- **Deployment:** Docker
- **Caching:** Redis (coming soon)

### 🛠 Getting Started

You have two options to run MarkTrack: using Docker Compose or running the development server directly.

#### Option 1: Using Docker Compose

1. Clone the repository:
    ```sh
    git clone https://github.com/RaevschiCatalin/MarkTrack.git
    cd MarkTrack
    ```

2. Build and run the application using Docker Compose:
    ```sh
    docker-compose up --build
    ```

#### Option 2: Running the Development Server Directly

1. Clone the repository:
    ```sh
    git clone https://github.com/RaevschiCatalin/MarkTrack.git
    cd MarkTrack
    ```

2. Install dependencies:
    ```sh
    npm install
    ```

3. Run the development server for the frontend:
    ```sh
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    # or
    bun dev
    ```

4. Navigate to the backend directory:
    ```sh
    cd backend
    ```

5. Run the backend server:
    ```sh
    uvicorn app:main --reload --host 0.0.0.0 --port 8080
    ```

### 🔧 Environment Setup

1. Create a `.env` file in the root directory with your Firebase credentials:
    ```env
    NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
    NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
    NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_firebase_project_id
    NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
    NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
    NEXT_PUBLIC_FIREBASE_APP_ID=your_firebase_app_id
    ```

2. Create a `credentials` folder in the `backend` directory and place your Firebase admin JSON file there.

3. Create another `.env` file in the `backend` directory with your JWT secret key:
    ```env
    SECRET_KEY=your_secret_key
    ```

### 🌐 Website

Visit the MarkTrack website at [mark-track.vercel.app](https://mark-track.vercel.app).

### 📚 Learn More

To learn more about the technologies used, check out these resources:
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Docker Documentation](https://docs.docker.com/)

### 🤝 Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](https://github.com/RaevschiCatalin/MarkTrack/blob/main/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

### 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/RaevschiCatalin/MarkTrack/blob/main/LICENSE) file for details.
