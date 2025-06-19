declare const FB: any;

export function initFacebookSDK(): void {
  (window as any).fbAsyncInit = function () {
    FB.init({
      appId: '1213236544138432',
      cookie: true,
      xfbml: true,
      version: 'v22.0'
    });
    FB.AppEvents.logPageView();
  };

  const script = document.createElement('script');
  script.src = 'https://connect.facebook.net/en_US/sdk.js';
  script.async = true;
  script.defer = true;
  script.crossOrigin = 'anonymous';
  script.id = 'facebook-jssdk';

  if (!document.getElementById('facebook-jssdk')) {
    document.body.appendChild(script);
  }
}
