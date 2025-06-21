import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { catchError, map, of } from 'rxjs';

export const AuthGuard: CanActivateFn = (
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  route,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  state
) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // First check if user is logged in locally
  if (!authService.isLoggedIn()) {
    router.navigate(['/login']);
    return false;
  }

  // Then validate token with backend
  return authService.validateToken().pipe(
    map(response => {
      if (response.succeeded && response.data === 'NotExpired') {
        return true;
      } else {
        authService.logout();
        router.navigate(['/login']);
        return false;
      }
    }),
    catchError(error => {
      console.error('Token validation error:', error);
      authService.logout();
      router.navigate(['/login']);
      return of(false);
    })
  );
}; 