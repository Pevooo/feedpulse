import { Component } from '@angular/core';
import { SpinnerService } from '../../app/services/spinner.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-spinner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="isLoading$ | async" class="spinner-overlay">
      <img src="assets/gif/spinner.gif" alt="Loading..." class="spinner-gif">
    </div>
  `,
  styles: [`
    .spinner-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(10, 38, 64, 0.7);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }
    .spinner-gif {
      width: 120px;
      height: 120px;
      filter: blur(0.04rem);
    }
  `]
})
export class SpinnerComponent {
  isLoading$ = this.spinnerService.isLoading$;

  constructor(private spinnerService: SpinnerService) {}
}
