import React, { useRef } from "react";
import "./VideoUpload.css";

const VideoUpload = ({ video, onChange }) => {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/quicktime'];
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(mp4|avi|mov|mkv)$/i)) {
        alert("Please upload a valid video file (MP4, AVI, MOV, MKV)");
        return;
      }

      // Validate file size (100MB max)
      const maxSize = 100 * 1024 * 1024; // 100MB
      if (file.size > maxSize) {
        alert("Video file is too large. Maximum size is 100MB.");
        return;
      }

      onChange(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileChange({ target: { files: [file] } });
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="video-upload">
      <h3 className="section-title">Video Upload</h3>
      
      <div
        className="upload-area"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="video/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        
        {video ? (
          <div className="video-preview">
            <div className="video-icon">VIDEO</div>
            <div className="video-info">
              <div className="video-name">{video.name}</div>
              <div className="video-size">{formatFileSize(video.size)}</div>
            </div>
            <button
              className="change-video-button"
              onClick={(e) => {
                e.stopPropagation();
                fileInputRef.current?.click();
              }}
            >
              Change
            </button>
          </div>
        ) : (
          <div className="upload-placeholder">
            <div className="upload-icon">UPLOAD</div>
            <p className="upload-text">
              Click to upload or drag and drop
            </p>
            <p className="upload-hint">
              MP4, AVI, MOV, MKV (Max 100MB)
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoUpload;

