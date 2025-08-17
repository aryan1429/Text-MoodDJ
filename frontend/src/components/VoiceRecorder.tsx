import { useState, useRef, useEffect } from 'react';

interface VoiceRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void;
  disabled?: boolean;
}

export default function VoiceRecorder({ onRecordingComplete, disabled }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const [recordingTime, setRecordingTime] = useState(0);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      setRecordingTime(0);

      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        onRecordingComplete(audioBlob);
        
        // Clean up
        stream.getTracks().forEach(track => track.stop());
        setIsRecording(false); // Ensure recording state is reset
        if (timerRef.current) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      setIsSupported(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    // Always set recording to false and clear timer, regardless of MediaRecorder state
    setIsRecording(false);
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!isSupported) {
    return (
      <div className="text-center p-6 bg-red-50 rounded-xl border border-red-200">
        <div className="text-red-500 text-lg">🎤 Voice recording not supported</div>
        <div className="text-red-400 text-sm mt-2">
          Please use a modern browser like Chrome, Firefox, or Safari
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-6 p-6">
      {/* Recording Button */}
      <div className="relative">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={disabled}
          className={`
            relative w-24 h-24 rounded-full border-4 transition-all duration-300 transform
            ${isRecording 
              ? 'bg-gradient-to-r from-red-500 to-red-600 border-red-300 animate-pulse scale-110 shadow-lg shadow-red-300' 
              : 'bg-gradient-to-r from-blue-500 to-blue-600 border-blue-300 hover:from-blue-600 hover:to-blue-700 hover:scale-105 hover:shadow-lg shadow-blue-300'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-xl'}
            flex items-center justify-center text-white text-3xl font-bold
          `}
          style={{
            boxShadow: isRecording 
              ? '0 0 30px rgba(239, 68, 68, 0.5)' 
              : '0 10px 25px rgba(59, 130, 246, 0.3)'
          }}
        >
          {isRecording ? '⏹️' : '🎤'}
        </button>
        
        {/* Recording pulse effect */}
        {isRecording && (
          <div className="absolute inset-0 rounded-full border-4 border-red-400 animate-ping opacity-30 pointer-events-none"></div>
        )}
      </div>
      
      {/* Recording Status */}
      <div className="text-center">
        {isRecording ? (
          <div className="space-y-2">
            <div className="text-red-600 font-bold text-lg flex items-center justify-center gap-2">
              🔴 Recording 
              <span className="bg-red-100 px-2 py-1 rounded text-sm">
                {formatTime(recordingTime)}
              </span>
            </div>
            <div className="text-gray-600 text-sm animate-pulse">
              Click stop when you're done speaking
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="text-gray-700 font-medium text-lg">
              🎙️ Ready to Record
            </div>
            <div className="text-gray-500 text-sm">
              Click the microphone to start
            </div>
          </div>
        )}
      </div>
      
      {/* Instructions */}
      {isRecording && (
        <div className="bg-blue-50 p-4 rounded-xl border border-blue-200 max-w-sm text-center">
          <div className="text-blue-800 text-sm">
            💡 <strong>Tip:</strong> Speak clearly about your feelings. 
            Say things like "I'm feeling happy today" or "I'm really stressed about work"
          </div>
        </div>
      )}
      
      {!isRecording && !disabled && (
        <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 max-w-sm text-center">
          <div className="text-gray-600 text-sm">
            🎯 <strong>How it works:</strong> Record your voice → AI transcribes → 
            Analyzes emotions → Finds matching music & memes!
          </div>
        </div>
      )}
    </div>
  );
}
