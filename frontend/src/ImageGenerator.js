import React, { useState } from "react";
import axios from "axios";

const ImageGenerator = () => {
  const [prompt, setPrompt] = useState("");
  const [imageUrl, setImageUrl] = useState("");

  const handleGenerateImage = async () => {
    try {
      const res = await axios.post(
        "https://openaichatbot-8stn.onrender.com/generate-image",
        {
          prompt,
        }
      );
      setImageUrl(res.data.image_url);
    } catch (error) {
      console.error("Error generating image:", error);
    }
  };

  return (
    <div>
      <h2>Generate an Image</h2>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter image prompt"
      />
      <button onClick={handleGenerateImage}>Generate Image</button>
      {imageUrl && (
        <div>
          <h3>Generated Image:</h3>
          <img src={imageUrl} alt="Generated" />
        </div>
      )}
    </div>
  );
};

export default ImageGenerator;
