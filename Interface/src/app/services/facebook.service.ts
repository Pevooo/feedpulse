import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

// Declare Facebook API globally
declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    FB: any;
  }
}

@Injectable({
  providedIn: 'root'
})
export class FacebookService {
  constructor(@Inject(PLATFORM_ID) private platformId: object) {}

  /**
   * Check the login status of the user
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  checkLoginStatus(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (isPlatformBrowser(this.platformId) && window.FB) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        window.FB.getLoginStatus((response: any) => {
          resolve(response);
        });
      } else {
        reject('Not running in browser');
      }
    });
  }

  /**
   * Trigger Facebook Login
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  loginWithFacebook(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (isPlatformBrowser(this.platformId) && window.FB) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        window.FB.login((response: any) => {
          if (response.authResponse) {
            resolve(response.authResponse);
          } else {
            reject('User cancelled login or permission denied');
          }
        }, { scope: 'pages_show_list,pages_read_engagement' });
      } else {
        reject('Not running in browser');
      }
    });
  }

  /**
   * Fetch the logged-in user's profile
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  getUserProfile(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (isPlatformBrowser(this.platformId) && window.FB) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        window.FB.api('/me', { fields: 'id,name,email,picture' }, (profile: any) => {
          if (profile && !profile.error) {
            resolve(profile);
          } else {
            reject(profile?.error || 'Failed to fetch user profile');
          }
        });
      } else {
        reject('Not running in browser');
      }
    });
  }
}
