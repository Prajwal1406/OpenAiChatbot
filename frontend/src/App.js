import React, { useState, useEffect } from "react";
import axios from "axios";
import AudioRecorder from "./AudioRecorder";
import ResponseDisplay from "./ResponseDisplay";
import "./App.css";

const App = () => {
  const [response, setResponse] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [textInput, setTextInput] = useState("");
  const [imageInput, setImageInput] = useState("");

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const res = await axios.get("http://localhost:8000/chat-history");
        setChatHistory(res.data.chat_history);
      } catch (error) {
        console.error("Error fetching chat history:", error);
      }
    };
    fetchChatHistory();
  }, []);

  const handleAudioSubmit = async (audioBlob) => {
    const formData = new FormData();
    formData.append("file", audioBlob, "audio.wav");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      if (res.data.image_url) {
        setImageUrl(res.data.image_url);
        setResponse("");
        setChatHistory([
          ...chatHistory,
          { type: "image", content: res.data.image_url },
        ]);
      } else {
        setResponse(res.data.response);
        setImageUrl("");
        setChatHistory([
          ...chatHistory,
          { type: "text", content: res.data.response },
        ]);
      }
    } catch (error) {
      console.error("Error sending audio to server:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleTextSubmit = async () => {
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/text-input", new URLSearchParams({ prompt: textInput }));
      if (res.data.image_url) {
        setImageUrl(res.data.image_url);
        setResponse("");
        setChatHistory([
          ...chatHistory,
          { type: "image", content: res.data.image_url },
        ]);
      } else {
        setResponse(res.data.response);
        setImageUrl("");
        setChatHistory([
          ...chatHistory,
          { type: "text", content: res.data.response },
        ]);
      }
    } catch (error) {
      console.error("Error sending text to server:", error);
    } finally {
      setLoading(false);
      setTextInput("");
    }
  };

  const handleImageUrlSubmit = async () => {
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/image-url-input", new URLSearchParams({ url: imageInput, prompt: textInput }));
      setResponse(res.data.response);
      setImageUrl("");
      setChatHistory([
        ...chatHistory,
        { type: "text", content: res.data.response },
      ]);
    } catch (error) {
      console.error("Error sending image URL to server:", error);
    } finally {
      setLoading(false);
      setImageInput("");
      setTextInput("");
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert("Text copied to clipboard!");
    }).catch((error) => {
      console.error("Error copying text: ", error);
    });
  };

  const downloadImage = (url) => {
    const element = document.createElement("a");
    element.href = url;
    element.download = "image.png";
    document.body.appendChild(element);
    element.click();
  };

  return (
    <div className="container">
      <h1>Ask a Question</h1>
      <div className="input-container">
        <input
          type="text"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="Type your question here..."
        />
        <button onClick={handleTextSubmit}>Submit</button>
      </div>
      <div className="input-container">
        <input
          type="text"
          value={imageInput}
          onChange={(e) => setImageInput(e.target.value)}
          placeholder="Enter image URL here..."
        />
        <button onClick={handleImageUrlSubmit}>Submit Image URL</button>
      </div>
      <AudioRecorder onAudioSubmit={handleAudioSubmit} />
      {loading && <p className="loading">Loading...</p>}
      <div className="chat-window">
        {chatHistory.map((entry, index) => (
          <div key={index} className={`chat-message ${entry.type === "text" ? "assistant" : "user"}`}>
            {entry.type === "text" ? (
              <div>
                <ResponseDisplay response={entry.content} />
                <button onClick={() => copyToClipboard(entry.content)}>Copy Text</button>
              </div>
            ) : (
              <div>
                <h3>Generated Image:</h3>
                <img src={entry.content} alt="Generated" />
                <button onClick={() => downloadImage(entry.content)}>Download Image</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
