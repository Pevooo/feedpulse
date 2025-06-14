import { HttpRequest, HttpHandlerFn, HttpEvent } from '@angular/common/http';
import { Observable, finalize } from 'rxjs';
import { inject } from '@angular/core';
import { SpinnerService } from '../services/spinner.service';

export function spinnerInterceptor(
  req: HttpRequest<unknown>,
  next: HttpHandlerFn
): Observable<HttpEvent<unknown>> {
  const spinnerService = inject(SpinnerService) as SpinnerService;

  // Skip showing spinner for chatbot requests
  const isChatbotRequest = req.url.includes('/chat'); // <-- Customize this based on your endpoint

  if (!isChatbotRequest) {
    spinnerService.show();
  }

  return next(req).pipe(
    finalize(() => {
      if (!isChatbotRequest) {
        spinnerService.hide();
      }
    })
  );
}
