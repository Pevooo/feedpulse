import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { DOCUMENT } from '@angular/common';
import { isPlatformBrowser } from '@angular/common';

// Extend the Window interface for Facebook SDK
declare global {
  interface Window {
    FB: {
      init: (params: { appId: string; cookie: boolean; xfbml: boolean; version: string }) => void;
      login: (callback: (response: LoginResponse) => void, options: { scope: string }) => void;
      getLoginStatus: (callback: (response: LoginStatusResponse) => void) => void;
      api: (path: string, params: { fields: string }, callback: (response: UserDataResponse) => void) => void;
      logout: (callback: (response: LogoutResponse) => void) => void;
    };
    fbAsyncInit: () => void;
  }
}

// Define Facebook response types
export interface LogoutResponse {
  status: 'unknown';
}

  export interface LoginResponse {
    authResponse?: {
      accessToken: string;
      userID: string;
      expiresIn: number;
      signedRequest: string;
    };
    status: 'connected' | 'not_authorized' | 'unknown';
  }

  export interface LoginStatusResponse {
    status: 'connected' | 'not_authorized' | 'unknown';
    authResponse?: {
      accessToken: string;
      userID: string;
      expiresIn: number;
      signedRequest: string;
    };}
  

export interface UserDataResponse {
    id?: string;
    name?: string;
    email?: string;
    error?: { message: string; type: string; code: number };
  };


@Injectable({
  providedIn: 'root'
})
export class FacebookService {
  private fbLoaded = false;

  constructor(
    @Inject(DOCUMENT) private document: Document,
    @Inject(PLATFORM_ID) private platformId: object
  ) {}

  loadFacebookSDK(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!isPlatformBrowser(this.platformId)) {
        reject(new Error('Facebook SDK can only be loaded in a browser environment'));
        return;
      }

      if (this.fbLoaded) {
        resolve();
        return;
      }

      window.fbAsyncInit = () => {
        window.FB.init({
          appId: '1213236544138432', // Replace with your Facebook App ID
          cookie: true,
          xfbml: true,
          version: 'v19.0' // Latest as of March 2025
        });
        this.fbLoaded = true;
        resolve();
      };

      const script = this.document.createElement('script');
      script.id = 'facebook-jssdk';
      script.src = 'https://connect.facebook.net/en_US/sdk.js';
      script.async = true;
      script.onload = () => {
        if (!window.FB) {
          reject(new Error('Facebook SDK failed to load'));
        }
      };
      script.onerror = () => reject(new Error('Failed to load Facebook SDK'));
      this.document.body.appendChild(script);
    });
  }

  login(): Promise<LoginResponse> {
    return new Promise((resolve, reject) => {
      if (!isPlatformBrowser(this.platformId) || !window.FB) {
        reject(new Error('Facebook SDK not loaded or not in browser'));
        return;
      }
      window.FB.login(
        (response: LoginResponse) => {
          if (response.authResponse) {
            resolve(response);
          } else {
            reject(new Error('User cancelled login or did not fully authorize'));
          }
        },
        { scope: 'public_profile,email' } // Removed pages_show_list since we don’t need pages
      );
    });
  }

  getLoginStatus(): Promise<LoginStatusResponse> {
    return new Promise((resolve, reject) => {
      if (!isPlatformBrowser(this.platformId) || !window.FB) {
        reject(new Error('Facebook SDK not loaded or not in browser'));
        return;
      }
      window.FB.getLoginStatus((response: LoginStatusResponse) => {
        resolve(response);
      });
    });
  }

  getUserData(): Promise<UserDataResponse> {
    return new Promise((resolve, reject) => {
      if (!isPlatformBrowser(this.platformId) || !window.FB) {
        reject(new Error('Facebook SDK not loaded or not in browser'));
        return;
      }
      window.FB.api('/me', { fields: 'id,name,email' }, (response: UserDataResponse) => {
        if (response.error) {
          reject(response.error);
        } else {
          resolve(response);
        }
      });
    });
  }

  logout(): Promise<LogoutResponse> {
    return new Promise((resolve, reject) => {
      if (!isPlatformBrowser(this.platformId) || !window.FB) {
        reject(new Error('Facebook SDK not loaded or not in browser'));
        return;
      }
      window.FB.logout((response: LogoutResponse) => {
        resolve(response);
      });
    });
  }
}