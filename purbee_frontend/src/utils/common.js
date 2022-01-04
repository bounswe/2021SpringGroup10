// return the user data from the session storage
export const getUser = () => {
    const userStr = sessionStorage.getItem('user');
    if (userStr) return JSON.parse(userStr);
    else return null;
  }
   
  
  // remove the user from the session storage
  export const removeUserSession = () => {
    sessionStorage.removeItem('user');
  }
   
  // set the user from the session storage
  export const setUserSession = (user) => {
    sessionStorage.setItem('user', JSON.stringify(user));
  }
