// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const FB: any;

declare global {
  interface Window {
    fbAsyncInit?: () => void;
  }
}

export function initFacebookSDK(): void {
  window.fbAsyncInit = () => {
    if (typeof FB !== 'undefined') {
      FB.init({
        appId: '1213236544138432',
        cookie: true,
        xfbml: true,
        version: 'v22.0',
      });
      FB.AppEvents.logPageView();
    }
  };

  const scriptId = 'facebook-jssdk';
  if (!document.getElementById(scriptId)) {
    const script = document.createElement('script');
    script.id = scriptId;
    script.src = 'https://connect.facebook.net/en_US/sdk.js';
    script.async = true;
    script.defer = true;
    script.crossOrigin = 'anonymous';
    document.body.appendChild(script);
  }
}
