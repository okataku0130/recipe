import React, { useState, useRef } from 'react';
import { Upload, X, Image as ImageIcon } from 'lucide-react';

interface ImageUploadProps {
  currentImage: string;
  onImageChange: (imageUrl: string) => void;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({ currentImage, onImageChange }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('画像ファイルを選択してください。');
      return;
    }

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      alert('ファイルサイズは5MB以下にしてください。');
      return;
    }

    setUploading(true);
    
    // Simulate upload process
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      
      // In a real application, you would upload to a server here
      // For demo purposes, we'll use a placeholder service
      setTimeout(() => {
        // Simulate successful upload with a placeholder image
        const placeholderImages = [
          'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800',
          'https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=800',
          'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=800',
          'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?auto=compress&cs=tinysrgb&w=800',
        ];
        const randomImage = placeholderImages[Math.floor(Math.random() * placeholderImages.length)];
        onImageChange(randomImage);
        setUploading(false);
      }, 1500);
    };
    
    reader.readAsDataURL(file);
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  const removeImage = () => {
    onImageChange('');
  };

  return (
    <div className="space-y-4">
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          dragActive 
            ? 'border-orange-500 bg-orange-50' 
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept="image/*"
          onChange={handleChange}
        />
        
        {uploading ? (
          <div className="flex flex-col items-center space-y-3">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-600"></div>
            <p className="text-sm text-gray-600">アップロード中...</p>
          </div>
        ) : (
          <div className="flex flex-col items-center space-y-3">
            <Upload className="w-8 h-8 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600 mb-1">
                画像をドラッグ&ドロップするか、
              </p>
              <button
                type="button"
                onClick={onButtonClick}
                className="text-orange-600 hover:text-orange-700 font-medium text-sm underline"
              >
                ファイルを選択
              </button>
            </div>
            <p className="text-xs text-gray-500">
              PNG, JPG, GIF (最大5MB)
            </p>
          </div>
        )}
      </div>

      {currentImage && (
        <div className="relative">
          <img
            src={currentImage}
            alt="アップロード画像"
            className="w-full h-48 object-cover rounded-lg border"
            onError={(e) => {
              e.currentTarget.style.display = 'none';
            }}
          />
          <button
            type="button"
            onClick={removeImage}
            className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-1 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
};