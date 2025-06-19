import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import {Component, OnInit} from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { initFacebookSDK } from "./utils/facebook-sdk-loader";

import {
  LanguageService,
} from './services/language.service';
import { FooterComponent } from '../Components/footer/footer.component';
import { LoginComponent } from '../Components/login/login.component';
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


  constructor(public languageService: LanguageService) {}

  ngOnInit() {
    initFacebookSDK();
  }


}
