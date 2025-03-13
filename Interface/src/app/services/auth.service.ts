import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import { Observable } from 'rxjs';
import { AuthResponse } from '../interfaces/auth-response';
import {HttpClient} from'@angular/common/http';
import { ApiResponse } from '../interfaces/Api_Response';
import { PLATFORM_ID } from '@angular/core';
import { inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
@Injectable({
  providedIn: 'root'
})

export class AuthService {
  apiurl:string = environment.apiUrl;
  private platformId:object = inject(PLATFORM_ID);
  constructor(private http:HttpClient) {}
  login(username: string, password: string): Observable<ApiResponse<AuthResponse>> {
    // Create form data
    const formData = new FormData();
    formData.append('UserName', username);
    formData.append('Password', password);
    console.log(this.apiurl);
    // Send POST request with form data
    return this.http.post<ApiResponse<AuthResponse>>(`https://localhost:7284/api/v1/authentication/sign-in`, formData);
  }
  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  }

  isLoggedIn(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return !!localStorage.getItem('accessToken');
    }
    return false; // Default to false on server side
  }
}
