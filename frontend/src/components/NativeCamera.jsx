import React from 'react';
import { Camera } from '@capacitor/camera';
import { Capacitor } from '@capacitor/core';

export const useNativeCamera = () => {
  const takePicture = async () => {
    if (!Capacitor.isNativePlatform()) {
      // Fallback a cámara web
      return null;
    }

    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: true,
        resultType: 'dataUrl',
        source: 'camera'
      });

      return image.dataUrl;
    } catch (error) {
      console.error('Error capturing photo:', error);
      return null;
    }
  };

  const pickFromGallery = async () => {
    try {
      const image = await Camera.getPhoto({
        quality: 90,
        allowEditing: false,
        resultType: 'dataUrl',
        source: 'photos'
      });

      return image.dataUrl;
    } catch (error) {
      console.error('Error picking photo:', error);
      return null;
    }
  };

  return { takePicture, pickFromGallery };
};
