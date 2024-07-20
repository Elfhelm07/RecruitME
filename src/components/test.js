// import axios from 'axios';
// import { setMaxListeners } from 'form-data';
// import React, { useState } from 'react'

// const Test = () => {
//     const [message,setmessage] = useState("");
//     const [messages,setmessages] = useState([]);
//     const [loading,setloading] = useState(false);
//     async function sendMessage() {
//         if (message.trim() === '') return;

//     const newMessage = { sender: 'user', text: message };
//     setmessages(prevMessages => [...prevMessages, newMessage]);
    
    
//     // setloading(true);
//     try {
        
//         const response = await fetch('http://localhost:5000/chat', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ message, candidate_id:"669a3da9d316eb14ef4282d7" }),
//         });
        
//         const result = await response.json();
//         const newMessage = { sender: 'bot', text: result.response };
//         setmessages(prevMessages => [...prevMessages, newMessage]);
//           console.log(result.response);
//         //   setloading(false)
//         } catch (error) {
//           console.error('Error:', error);
//         }
//       }
      
//   return (
//     <div className="flex flex-col h-screen bg-gray-200 p-4 px-40">
//       <div className="flex flex-col flex-1 overflow-y-auto p-4 space-y-4">
//         {messages.map((m, index) => (
//           <div
//             key={index}
//             className={`p-4 rounded-lg max-w-[80vw] ${
//               m.sender === 'user' ? 'bg-slate-800 text-white self-end' : 'bg-white text-slate-800 self-start'
//             }`}
//           >
//             {m.text}
//           </div>
//         ))}
//         {loading && (
//           <div className="p-4 rounded-lg bg-gray-200 text-gray-600 self-start">Loading...</div>
//         )}
//       </div>
//       <div className="mt-4 flex">
//         <input
//           type="text"
//           value={message}
//           onChange={(e) => setmessage(e.target.value)}
//           className="flex-1 p-2 border rounded-lg focus:outline-none focus:border-slate-800"
//           placeholder="Type your message..."
//         />
//         <button
//           onClick={sendMessage}
//           className="ml-4 p-2 bg-slate-800 text-white rounded-lg hover:bg-slate-700"
//         >
//           Enter
//         </button>
//       </div>
//     </div>
//   )
// }

// export default Test;



import axios from 'axios';
import React, { useState } from 'react';

const Test = () => {
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    async function sendMessage() {
        if (message.trim() === '') return;

        const newMessage = { sender: 'user', text: message };
        setMessages(prevMessages => [...prevMessages, newMessage]);

        setLoading(true);
        try {
            const response = await axios.post('http://localhost:5000/chat_hr', {
                message,
                // candidate_id: "669a3da9d316eb14ef4282d7"
            });

            const result = response.data;
            const responseMessage = { sender: 'bot', text: result.response };
            setMessages(prevMessages => [...prevMessages, responseMessage]);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
        setMessage("");
    }

    return (
        <div className="flex flex-col h-screen bg-gray-200 p-5 px-40">
            <div className="flex flex-col  h-full overflow-y-auto p-4 space-y-4">
                {messages.map((m, index) => (
                    <div
                        key={index}
                        className={`p-4 rounded-lg max-w-[80vh] ${
                            m.sender === 'user' ? 'bg-slate-800 text-white self-end' : 'bg-white text-slate-800 self-start'
                        }`}
                    >
                        {m.text}
                    </div>
                ))}
                {loading && (
                    <div className="p-4 rounded-lg bg-gray-200 text-gray-600 self-start">Loading...</div>
                )}
            </div>
            <div className="mt-4 flex">
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    className="flex-1 p-2 border rounded-lg focus:outline-none focus:border-slate-800"
                    placeholder="Type your message..."
                />
                <button
                    onClick={sendMessage}
                    className="ml-4 p-2 bg-slate-800 text-white rounded-lg hover:bg-slate-700"
                >
                    Enter
                </button>
            </div>
        </div>
    );
}

export default Test;

