import { HttpRequest, HttpHandlerFn, HttpEvent } from '@angular/common/http';
import { Observable, finalize } from 'rxjs';
import { inject } from '@angular/core';
import { SpinnerService } from '../services/spinner.service';

export function spinnerInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
  const spinnerService = inject(SpinnerService) as SpinnerService; // Explicitly cast to SpinnerService
  spinnerService.show(); // Show spinner when request starts
  return next(req).pipe(
    finalize(() => spinnerService.hide()) // Hide spinner when request completes
  );
}