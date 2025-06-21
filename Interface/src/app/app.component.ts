import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import {Component, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { initFacebookSDK } from "./utils/facebook-sdk-loader";

import {
  LanguageService,
} from './services/language.service';
import { AuthService } from './services/auth.service';
import { FooterComponent } from '../Components/footer/footer.component';
import { NavbarComponent } from '../Components/navbar/navbar.component';
import { SpinnerComponent } from '../Components/spinner/spinner.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    HttpClientModule,
    NavbarComponent,
    FooterComponent,
    SpinnerComponent,
    CommonModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'FeedPulse';


  constructor(
    public languageService: LanguageService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    initFacebookSDK();
    
    // Validate token on application startup
    if (this.authService.isLoggedIn()) {
      this.authService.validateToken().subscribe({
        next: (response) => {
          if (!response.succeeded || response.data !== 'NotExpired') {
            console.log('Token validation failed on startup, logging out');
            this.authService.logout();
          }
        },
        error: (error) => {
          console.error('Token validation error on startup:', error);
          this.authService.logout();
        }
      });
    }
  }


}
