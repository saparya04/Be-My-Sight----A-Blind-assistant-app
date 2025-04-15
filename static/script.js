// Function to speak a message using SpeechSynthesis
function speak(text, callback) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.onend = callback; // Trigger callback after speech ends
    speechSynthesis.speak(utterance);
}

// Setup Speech Recognition
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.interimResults = false;

let step = 0;

// Handle recognition results
recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript.toLowerCase();
    console.log("User said:", transcript);

    if (step === 1 && transcript.includes("english")) {
        step = 2;
        speak("hmmm, so english it is, great work buddy. I am your friend, guider, consoler, moreover, your vision. Now I would explain how the app works. First, you need to sign up to our app, so spell your email ID with the format, dash, at the rate, gmail.com. Say when in 3, 2, 1.", () => {
            recognition.start();
        });
    } else if (step === 2) {
        step = 3;
        speak("Now, spell an easy and short password with alphabets, digits, or any special character.", () => {
            recognition.start();
        });
    } else if (step === 3) {
        step = 4;
        speak("hmm, cool. Now, you have been registered.", () => {
            speak("Second, we have the following options like home, contact, and help. In contact, you could contact the creator of this app named Aishwarya, Claven, or Sap either by email, call, or Instagram. Then there is the help button where I will explain what services I could provide. So choose an option now buddy, within 3, 2, 1.", () => {
                recognition.start();
            });
        });
    } else if (step === 4 && transcript.includes("help")) {
        step = 5;
        speak("okay, so, seems like you chose help, that's nice. Now in order to get started with this app, choose any one of our two features: object detection or currency detection. Say 'currency' or spell it C, U, R, R, E, N, C, Y. For object detection say 'object' or O, B, J, E, C, T. You can also say 'contact' to go back. Speak now in 3, 2, 1.", () => {
            recognition.start();
        });
    } else if (step === 5) {
        if (transcript.includes("object")) {
            step = 6;
            speak("Opening object detection camera module now.", () => {
                openCameraModule();
            });
        } else if (transcript.includes("currency")) {
            speak("Starting currency detection now.");
        } else if (transcript.includes("contact")) {
            speak("Redirecting you to contact section.");
        } else {
            speak("Sorry, I didn't understand. Please try again.", () => recognition.start());
        }
    } else {
        speak("Sorry, I didn't get that. Please try again.", () => recognition.start());
    }
};

// Handle errors
recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
    speak("Oops, something went wrong. Please try again.");
};

// Open camera module
function openCameraModule() {
    console.log("Camera module triggered!");
    document.getElementById("camera").innerText = "Launching object detection...";

    fetch('/run-object-detection', {
        method: 'POST'
    })
    .then(response => response.text())
    .then(data => {
        console.log("Server response:", data);
        document.getElementById("camera").innerText = data;
    })
    .catch(error => {
        console.error("Error launching object detection:", error);
        document.getElementById("camera").innerText = "Failed to start object detection.";
    });
}


// Initialize the Assistant
function initializeAssistant() {
    step = 1;
    speak("Welcome to Be My Sight. Your choice. Our vision.", () => {
        speak("Our app is now opened.", () => {
            speak("Which language are you comfortable in? The available options are English and Hindi.", () => {
                recognition.start();
            });
        });
    });
}

// On page load
window.onload = function () {
    setTimeout(initializeAssistant, 2000);
};

// Start button logic
document.getElementById("startButton").addEventListener("click", function () {
    initializeAssistant();
    fetch('/welcome')
        .then(response => response.ok ? response.json() : Promise.reject('Fetch failed'))
        .then(data => {
            document.getElementById("response").innerText = data.message;
        })
        .catch(error => console.error("Fetch error:", error));
});