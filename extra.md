#EXTRA FEATURES

##DARK MODE

A brief explanation of your additions:
- Dark mode was implemented on the front end of the project-frontend repo via a fork. The feature required some work as I had to self-learn at least a small portion of React, but was quite simple once I noticed the central `themes.js` file which I was able to leverage.
- A button is now present at the top nav bar of the page, which allows the user to toggle between light and dark mode theme (light is the default). This state is stored locally and is essentially a boolean which keeps track of whether a user is currently in light or dark mode in order to change the themes accordingly on button press. This state management is handled internally within React.
