import React, { useState, useRef } from 'react';

const AudioRecorder = ({ onAudioSubmit }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [status, setStatus] = useState('Click the button to start recording.');
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const handleRecordButtonClick = async () => {
        if (isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            setStatus('Recording stopped. Processing...');
        } else {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            mediaRecorderRef.current.start();
            setIsRecording(true);
            setStatus('Recording...');

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
                audioChunksRef.current = [];
                onAudioSubmit(audioBlob);
            };
        }
    };

    return (
        <div>
            <button onClick={handleRecordButtonClick}>
                {isRecording ? 'Stop Recording' : 'Record Question'}
            </button>
            <p>{status}</p>
        </div>
    );
};

export default AudioRecorder;
