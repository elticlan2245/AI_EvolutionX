import { Capacitor } from '@capacitor/core';
import { Camera } from '@capacitor/camera';
import { Share } from '@capacitor/share';
import { Haptics, ImpactStyle } from '@capacitor/haptics';
import { Network } from '@capacitor/network';

export const isNative = Capacitor.isNativePlatform();
export const platform = Capacitor.getPlatform(); // 'ios', 'android', 'web'

// Helper functions
export const capturePhoto = async () => {
  const image = await Camera.getPhoto({
    quality: 90,
    allowEditing: false,
    resultType: 'dataUrl'
  });
  return image.dataUrl;
};

export const shareContent = async (text, url) => {
  await Share.share({
    title: 'AI EvolutionX',
    text: text,
    url: url,
    dialogTitle: 'Compartir conversación'
  });
};

export const vibrate = async () => {
  await Haptics.impact({ style: ImpactStyle.Light });
};

export const checkNetwork = async () => {
  const status = await Network.getStatus();
  return status.connected;
};
