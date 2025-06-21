import { HttpInterceptorFn, HttpErrorResponse, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { throwError, BehaviorSubject } from 'rxjs';
import { catchError, filter, take, switchMap } from 'rxjs/operators';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

// Global state for refresh token handling
let isRefreshing = false;
const refreshTokenSubject = new BehaviorSubject<string | null>(null);

export const TokenInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // Skip token attachment for authentication endpoints
  if (isAuthEndpoint(request.url)) {
    return next(request);
  }

  // Add token to request
  const token = authService.getAccessToken();
  if (token) {
    request = addToken(request, token);
  }

  return next(request).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && !isRefreshing) {
        isRefreshing = true;
        refreshTokenSubject.next(null);

        return authService.refreshToken().pipe(
          switchMap((response) => {
            isRefreshing = false;
            
            if (response.succeeded && response.data) {
              authService.storeTokens(
                response.data.accessToken,
                response.data.refreshToken.token
              );
              refreshTokenSubject.next(response.data.accessToken);
              
              // Retry the original request with new token
              return next(addToken(request, response.data.accessToken));
            } else {
              // Refresh failed, redirect to login
              authService.logout();
              router.navigate(['/login']);
              return throwError(() => error);
            }
          }),
          catchError((refreshError) => {
            isRefreshing = false;
            authService.logout();
            router.navigate(['/login']);
            return throwError(() => refreshError);
          })
        );
      } else if (error.status === 401 && isRefreshing) {
        // Wait for the refresh to complete
        return refreshTokenSubject.pipe(
          filter(token => token !== null),
          take(1),
          switchMap(token => next(addToken(request, token!)))
        );
      }

      return throwError(() => error);
    })
  );
};

function addToken(request: HttpRequest<unknown>, token: string): HttpRequest<unknown> {
  return request.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });
}

function isAuthEndpoint(url: string): boolean {
  const authEndpoints = [
    '/api/v1/authentication/sign-in',
    '/api/v1/authentication/refresh-token',
    '/api/v1/authentication/validate-token',
    '/api/v1/application-users/create'
  ];
  
  return authEndpoints.some(endpoint => url.includes(endpoint));
} 