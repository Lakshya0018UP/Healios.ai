import { useState } from "react";



const Login = () => {

  const [isLogin, setIsLogin] = useState(true);

  

  const LoginForm = () => {
    
      
      return (
      <div className="bg-white rounded-2xl shadow-2xl flex flex-col w-full md:w-1/3 items-center max-w-4xl transition duration-1000 ease-out">
        <h2 className='p-3 text-3xl font-bold text-pink-400'>Hello There!!</h2>
        <div className="inline-block border-[1px] justify-center w-20 border-blue-400 border-solid"></div>
        <h3 className='text-xl font-semibold text-blue-400 pt-2'>Sign In!</h3>
        <div className='flex space-x-2 m-4 items-center justify-center'>
          <div className="h-9 w-9">
            <img src={require('./logo/twitter.png')} alt="logo" />
          </div>
          <div className="h-10 w-10">
            <img src={require('./logo/insta.png')} alt="logo" />
          </div>
          <div className="h-10 w-10">
            <img src={require('./logo/fb.png')} alt="logo" />
          </div>
        </div>
        {/* Inputs */}
        <div className='flex flex-col items-center justify-center'>
          <input type='username' className='rounded-2xl px-2 py-1 w-4/5 md:w-full border-[1px] border-blue-400 m-1 focus:shadow-md focus:border-pink-400 focus:outline-none focus:ring-0' placeholder='Username'></input>
          <input type="password" className='rounded-2xl px-2 py-1 w-4/5 md:w-full border-[1px] border-blue-400 m-1 focus:shadow-md focus:border-pink-400 focus:outline-none focus:ring-0' placeholder='Password'></input>
          <button className='rounded-2xl m-2 text-white bg-blue-400 w-auto px-4 py-2 shadow-md hover:text-blue-400 hover:bg-white transition duration-200 ease-in'>
            Sign In
          </button>
        </div>
        <div className="inline-block border-[1px] justify-center w-20 border-blue-400 border-solid"></div>
        <p className='text-red-400 mt-4 text-sm'>Don't have an account?</p>
        <p className='text-blue-400 mb-4 text-sm font-medium cursor-pointer' onClick={() => setIsLogin(false)}>Create a New Account?</p>
      </div>
    )
  }

  const SignUpForm = () => {
    return (
      <div className="bg-blue-400 rounded-2xl shadow-2xl  flex flex-col w-full  md:w-1/3 items-center max-w-4xl transition duration-1000 ease-in">
        <h2 className='p-3 text-3xl font-bold text-white'>Hello There!!</h2>
        <div className="inline-block border-[1px] justify-center w-20 border-white border-solid"></div>
        <h3 className='text-xl font-semibold text-white pt-2'>Create Account!</h3>
        <div className='flex space-x-2 m-4 items-center justify-center object-cover'>
        <div className="h-8 w-8 bg-white rounded-full">
            <img src={require('./logo/twitter.png')} alt="logo" />
          </div>
          <div className="h-9 w-9  bg-white rounded-full">
            <img src={require('./logo/insta.png')} alt="logo" />
          </div>
          <div className="h-8 w-8 bg-white rounded-full">
            <img src={require('./logo/fb.png')} alt="logo" />
          </div>
        </div>
        {/* Inputs */}
        <div className='flex flex-col items-center justify-center mt-2 text-black hover:text-pink-400'>
          <input type="name" className='rounded-2xl px-2 py-1 w-4/5 md:w-full border-[1px] border-blue-400 m-1 focus:shadow-md focus:border-pink-400 focus:outline-none focus:ring-0' placeholder='Name'></input>
          <input type='username' className='rounded-2xl px-2 py-1 w-4/5 md:w-full border-[1px] border-blue-400 m-1 focus:shadow-md focus:border-pink-400 focus:outline-none focus:ring-0' placeholder='Username'></input>
          <input type="password" className='rounded-2xl px-2 py-1 w-4/5 md:w-full border-[1px] border-blue-400 m-1 focus:shadow-md focus:border-pink-400 focus:outline-none focus:ring-0' placeholder='Password'></input>
          {/* <input type="url" className='rounded-2xl px-2 py-1 w-4/5 md:w-full border-[1px] border-blue-400 m-1 focus:shadow-md focus:border-pink-400 focus:outline-none focus:ring-0' placeholder='Avatar URL'></input> */}
          <button className='rounded-2xl m-4 text-blue-400 bg-white w-3/5 px-4 py-2 shadow-md hover:text-white hover:bg-blue-400 transition duration-200 ease-in'>
            Sign Up
          </button>
        </div>
        <div className="inline-block border-[1px] justify-center w-20 border-white border-solid"></div>
        <p className='text-white mt-4 text-sm'>Already have an account?</p>
        <p className='text-white mb-4 text-sm font-medium cursor-pointer' onClick={() => setIsLogin(true)}>Sign In to your Account?</p>
      </div>
    )
  }

  return (
    <div className="bg-gray-100 flex flex-col items-center justify-center min-h-screen md:py-2">
      <main className="flex items-center w-full px-2 md:px-20">
        <div className="hidden md:inline-flex flex-col flex-1 space-y-1">
          <p className='text-6xl text-blue-500 font-bold'>Hospital App</p>
          <p className='font-medium text-lg leading-1 text-pink-400'>Explore your information, at one place</p>
        </div>
        {
          isLogin ? (
            <LoginForm />
          ) : (
            <SignUpForm />
          )
        }
      </main>
    </div>
  )
}

export default Login

// import React, { useState } from 'react';
// import axios from 'axios';
// import './App.css';

// function App() {
//   const [userMessage, setUserMessage] = useState('');
//   const [chatLog, setChatLog] = useState([]);

//   const sendMessage = async () => {
//     if (!userMessage.trim()) return;

//     // Add user message to the chat log
//     setChatLog([...chatLog, { sender: 'user', text: userMessage }]);
    
//     try {
//       // Make API call to Flask backend
//       const response = await axios.post('http://127.0.0.1:5000/chatbot', {
//         message: userMessage,
//       });
//       const botResponse = response.data.response;

//       // Add bot response to the chat log
//       setChatLog((prevLog) => [...prevLog, { sender: 'bot', text: botResponse }]);
//     } catch (error) {
//       console.error('Error communicating with the chatbot API:', error);
//       setChatLog((prevLog) => [...prevLog, { sender: 'bot', text: 'Error: Unable to connect to chatbot API.' }]);
//     }

//     // Clear user input field
//     setUserMessage('');
//   };

//   return (
//     <div className="App">
//       <h1>Chatbot</h1>
//       <div className="chat-window">
//         {chatLog.map((message, index) => (
//           <div
//             key={index}
//             className={message.sender === 'user' ? 'user-message' : 'bot-message'}
//           >
//             <p>{message.text}</p>
//           </div>
//         ))}
//       </div>
//       <div className="input-area">
//         <input
//           type="text"
//           placeholder="Type your message..."
//           value={userMessage}
//           onChange={(e) => setUserMessage(e.target.value)}
//           onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
//         />
//         <button onClick={sendMessage}>Send</button>
//       </div>
//     </div>
//   );
// }

// export default App;
