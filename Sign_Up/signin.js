// Import the functions you need from the Firebase SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-analytics.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA3g3WD6c3w9cNJYAm_gNtju9P7qxEz6_A",
    authDomain: "rakshak-sign-up.firebaseapp.com",
    projectId: "rakshak-sign-up",
    storageBucket: "rakshak-sign-up.firebasestorage.app",
    messagingSenderId: "672485507041",
    appId: "1:672485507041:web:359ac6c522e8207dee9ca0",
    measurementId: "G-M49PV10GK1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function() {
    const signinForm = document.getElementById('signinForm');

    signinForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        // Get values from input fields
        const username = document.getElementById('loginusername').value; // Optional if not used for auth
        const email = document.getElementById('loginemail').value;
        const password = document.getElementById('loginpassword').value;

        const auth = getAuth();
        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                // Signed in 
                const user = userCredential.user;
                alert("Sign In Successful! Redirecting...");
                window.location.href = "welcome.html"; // Redirect to welcome page
            })
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                alert(`Error: ${errorMessage}`); // Display error message
            });
    });
});
