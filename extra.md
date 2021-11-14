# EXTRA FEATURES

## DARK MODE

A brief explanation of your additions:
- Dark mode was implemented on the front end of the project-frontend repo via a fork. The feature required some work as I had to self-learn at least a small portion of React, but was quite simple once I noticed the central `themes.js` file which I was able to leverage.
- A button is now present at the top nav bar of the page, which allows the user to toggle between light and dark mode theme (light is the default). This state is stored locally and is essentially a boolean which keeps track of whether a user is currently in light or dark mode in order to change the themes accordingly on button press. This state management is handled internally within React.
- Additionally, I noticed that if you swap to "Dark Mode" then refresh the page, the state of what current theme the user has is not saved properly. A solution to this was to implement a `localStorage` entry for `currentTheme` where I was able to track the current theme the user was using regardless of whether they refresh the page or not. 
- Persistence of themes is also implemented, meaning that if the user selects "Dark Mode", and then closes and reopens the page, then the Dark Theme will be the used theme.

## TYPE CHECKING

- type checking is implemented on the backend toward all the functions called by the server.
- type checking mainly focuses on the type correctness of parameters and return types of the function.
- type checking also include some checking toward variables(with complicate data structures) that in the function 
- type checking is done by the module `typing`, the mainly used methods are `Tuple`, `List`, `Dict` and `Union`