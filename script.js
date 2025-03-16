// Function to speak a message using SpeechSynthesis
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US"; // Set the language
    speechSynthesis.speak(utterance); // Speak the message
}

// Initialize the speech recognition
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US"; // Set the recognition language
recognition.interimResults = false; // Get final results only

recognition.onresult = function(event) {
    const userLanguage = event.results[0][0].transcript.toLowerCase(); // Get the recognized text
    console.log(`User said: ${userLanguage}`);

    // Respond based on the recognized language
    if (userLanguage.includes("english")) {
        speak("Good job.");
    } else {
        speak("Sorry, I didn't get that. Please try again.");
    }
};

recognition.onerror = function(event) {
    console.error('Speech recognition error:', event.error);
    speak("Choose an option,,,,,,,,. .");
};

// Function to initialize the assistant
function initializeAssistant() {
    // First message
    speak("Our app is now opened");

    // Second message
    setTimeout(() => {
        speak("Which language are you comfortable in? The available options are english and hindi          ");

        recognition.start();
    }, 2000); 

    setTimeout(() => {
        speak("hmmm, so english it is, great work buddy.I am your friend, guider,consoler , moreover, your vision.   Now I would explain how the app works. First, u need to sign up to our app, so spell your email I di WITH the format, dash, at the rate,G mail.com,......say when in 3, 2, 1,,.");
        recognition.start();
    }, 10000);
    setTimeout(() => {
        speak("Now, spell an easy and short password with, alphabets, digits, or, any special character....,");
        recognition.start();
    }, 30000);
    
    setTimeout(() => {
        speak("hmm,,,,,,,,cool,,,");
    }, 40000);
    setTimeout(() => {
        speak("Now, you have been registerd");
    }, 40000);
    setTimeout(() => {
        speak("Second, we have the following options like home, contact, and help. In contact, you could contact the creator of this app named, Aishwarya, Claven, or, Sap.  either by email, call, or Instagram, and they will answer any number of queries. Then there is the help button where I will explain to you what all services I could provide to you, so, choose an option now buddy,within, 3, 2, 1,,");
    }, 40000);
    setTimeout(() => {
        speak("okay, so, seems like,  u chose help, thats nice, now in order to get started with this app first yoy have choose any one of our 2 features, which are, object detection, or, currency detection, for currency detection kindly say the word currency, or, as I spell C, U, R, R, E, N, C, Y, and for object detection say the word object or as i spell O, B, J, E, C, T, out loud, or, you could also go back and choose, the contact button, or say the word, C,O,N,T,A,C,T,, now is the time speak in 3,2,1 ");
    }, 40000);
    setTimeout(() => {
        speak("hmmm, so u chose contact ha, whom would u like to contact, sap,aishwarya, or, claven,say in 3,2,1");
    }, 40000);
    setTimeout(() => {
        speak("okay, so sap it is, now tell me how would u like to contact her, via email, or, via message,say in 3,2,1,  ");
    }, 40000);
    setTimeout(() => {
        speak("So, sending text from your registerd email I di now");
    }, 50000);
    

    


}

// Welcome message on app start
window.onload = function() {
    speak("Welcome to be my sight.  your choice.     our vision"); // Say welcome message
    setTimeout(initializeAssistant, 2000); // Wait for 2 seconds before initializing the assistant
};

// Event listener for the start button
document.getElementById("startButton").addEventListener("click", function() {
    // Start the assistant
    initializeAssistant();

    // Fetch the welcome route from the Flask server
    fetch('/welcome')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            // Update the response paragraph with the message from the server
            document.getElementById("response").innerText = data.message;
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
});
