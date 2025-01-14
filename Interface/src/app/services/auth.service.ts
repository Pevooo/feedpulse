import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment.development';
import{LoginRequest} from '../../app/interfaces/login-request'
import { map, Observable } from 'rxjs';
import { AuthResponse } from '../interfaces/auth-response';
import {HttpClient} from'@angular/common/http';
@Injectable({
  providedIn: 'root'
})

export class AuthService {
  apiurl:string = environment.apiUrl;
  private tokenkey= 'token';
  constructor(private http:HttpClient) {}
  login(data:LoginRequest) : Observable<AuthResponse>{
  return this.http.
    post<AuthResponse>(`${this.apiurl}Auth/login`,data).pipe(
      map((res)=>{
        if(res.isAuthenticated){
          localStorage.setItem(this.tokenkey,res.token);
        }
        return res;
      })
    );
  }
}
