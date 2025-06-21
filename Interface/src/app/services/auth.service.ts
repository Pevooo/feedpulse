import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable } from 'rxjs';
import { AuthResponse } from '../interfaces/auth-response';
import {HttpClient} from'@angular/common/http';
import { ApiResponse } from '../interfaces/Api_Response';
import { PLATFORM_ID } from '@angular/core';
import { inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { IRegistrationModel } from '../interfaces/IRegisterModel';
import { CookieService } from 'ngx-cookie-service';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  apiurl:string = environment.apiUrl;
  private platformId:object = inject(PLATFORM_ID);
  constructor(private http:HttpClient, private cookieService: CookieService) {}
  
  // Get access token from cookies
  getAccessToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return this.cookieService.get('accessToken') || null;
    }
    return null;
  }

  // Get refresh token from cookies
  getRefreshToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return this.cookieService.get('refreshToken') || null;
    }
    return null;
  }

  // Check if token is expired using client-side validation
  isTokenExpired(): boolean {
    const token = this.getAccessToken();
    if (!token) return true;
    
    try {
      const decoded: { exp: number } = jwtDecode(token);
      const currentTime = Date.now() / 1000;
      return decoded.exp < currentTime;
    } catch {
      return true;
    }
  }

  // Validate token with backend
  validateToken(): Observable<ApiResponse<string>> {
    const token = this.getAccessToken();
    if (!token) {
      throw new Error('No access token found');
    }
    return this.http.get<ApiResponse<string>>(`${environment.apiUrl}/api/v1/authentication/validate-token?AccessToken=${token}`);
  }

  // Refresh token using backend endpoint
  refreshToken(): Observable<ApiResponse<AuthResponse>> {
    const accessToken = this.getAccessToken();
    const refreshToken = this.getRefreshToken();
    
    if (!accessToken || !refreshToken) {
      throw new Error('Missing tokens for refresh');
    }

    const formData = new FormData();
    formData.append('AccessToken', accessToken);
    formData.append('RefreshToken', refreshToken);

    return this.http.post<ApiResponse<AuthResponse>>(`${environment.apiUrl}/api/v1/authentication/refresh-token`, formData);
  }

  // Store new tokens after refresh
  storeTokens(accessToken: string, refreshToken: string): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cookieService.set('accessToken', accessToken);
      this.cookieService.set('refreshToken', refreshToken);
    }
  }

  login(username: string, password: string): Observable<ApiResponse<AuthResponse>> {
    // Create form data
    const formData = new FormData();
    formData.append('UserName', username);
    formData.append('Password', password);
    console.log(this.apiurl);
    // Send POST request with form data
    return this.http.post<ApiResponse<AuthResponse>>(`${environment.apiUrl}/api/v1/authentication/sign-in`, formData);
  }
 Register(model: IRegistrationModel): Observable<ApiResponse<object>> {
    const formData = new FormData();
    formData.append('FullName', model.fullName);
    formData.append('UserName', model.userName);
    formData.append('Email', model.email);
    formData.append('Password', model.password);
    formData.append('ConfirmPassword', model.confirmPassword);
    formData.append('Country', model.country);
    formData.append('Address', model.address || '');
    formData.append('PhoneNumber', model.phoneNumber);
    
    // Append photo with type assertion to Blob
    if (model.photo) {
      formData.append('Photo', model.photo as Blob, model.photo.name);
    } else {
      console.warn('Photo is missing, backend might reject the request');
    }

    // Debug logging
    console.log('FormData being sent:');
    const formDataKeys = [
      'FullName', 'UserName', 'Email', 'Password', 'ConfirmPassword', 
      'Country', 'Address', 'PhoneNumber', 'Photo'
    ];
    formDataKeys.forEach(key => {
      const value = formData.get(key);
      if (value) {
        console.log(`${key}:`, value);
      }
    });

    return this.http.post<ApiResponse<object>>(
      `${environment.apiUrl}/api/v1/application-users/create`,
      formData
    );
  }
  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cookieService.delete('accessToken');
      this.cookieService.delete('refreshToken');
    }
  }

  isLoggedIn(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return this.cookieService.check('accessToken');
    }
    return false; // Default to false on server side
  }
}
