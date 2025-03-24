import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SpinnerService {
  private activeRequests = 0;
  private isLoading = new BehaviorSubject<boolean>(false);
  isLoading$ = this.isLoading.asObservable();

  show() {
    this.activeRequests++;
    this.isLoading.next(true);
    console.log('Spinner show, active requests:', this.activeRequests); // Debug
  }

  hide() {
    this.activeRequests--;
    if (this.activeRequests <= 0) {
      this.isLoading.next(false);
      this.activeRequests = 0;
    }
    console.log('Spinner hide, active requests:', this.activeRequests); // Debug
  }
}