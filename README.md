# Greivex – AI-Powered Civic Grievance Management Platform

Greivex is an innovative platform that leverages deep learning and large language models (LLMs) to automate, streamline, and enhance the process of civic grievance reporting and resolution. Designed for transparency, speed, and user empowerment, Greivex bridges the gap between citizens and service providers, making public issue management smarter and more effective.

## 🚀 Features

- **AI-Based Department Classification:**
  - Uses a custom-trained ResNet model for image-based complaint routing.
  - Employs LLMs for analyzing complaint descriptions and assigning them to the correct department.
- **Intelligent Prioritization:**
  - Automatically prioritizes complaints (Critical, High, Medium, Low) using NLP and LLMs.
- **Duplicate & Fake Complaint Detection:**
  - Flags duplicate or nonsensical complaints using AI-powered similarity checks.
- **Automated Location Detection:**
  - Captures user GPS and reverse-geocodes to suggest the correct area.
- **Role-Based Dashboards:**
  - Separate dashboards for citizens, providers, and management with tailored features.
- **Amazon-Style Status Timeline:**
  - Track complaints through clear stages: Registered → Accepted → Working On → Completed/Rejected.
- **Automated Email Notifications:**
  - Sends OTPs and status updates via email.
- **Modern, Responsive UI/UX:**
  - Built with React.js for a seamless, accessible experience.
- **Secure Authentication:**
  - JWT-based authentication and role-based access control.

## 🛠️ Tech Stack

- **Frontend:** React.js, HTML5, CSS3, JavaScript, Axios
- **Backend:** Node.js, Express.js, MongoDB, Mongoose, JWT, Nodemailer
- **AI/ML:** ResNet (image classification), LLMs (text analysis), NLP
- **Other:** RESTful APIs, GPS & Reverse Geocoding APIs, Role-Based Access Control

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/greivex.git
   cd greivex
   ```

2. **Install dependencies:**
   - For backend:
     ```bash
     cd backend
     npm install
     ```
   - For frontend:
     ```bash
     cd ../frontend
     npm install
     ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` in the backend folder and fill in the required values.

4. **Run the application:**
   - Start backend:
     ```bash
     npm start
     ```
   - Start frontend:
     ```bash
     npm start
     ```

## 🧠 Project Story & Vision

Greivex was inspired by the need for a smarter, more transparent civic grievance system. Our team combined deep learning and LLMs to automate complaint routing, prioritization, and duplicate detection, making the process efficient for both citizens and authorities.

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgements

- OpenAI, HuggingFace, and the open-source community for LLM and deep learning resources.
- All contributors and testers who helped shape Greivex.

---

*Empowering communities with AI for a smarter, greener future.*
