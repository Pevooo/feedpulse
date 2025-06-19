import { HttpClientModule } from '@angular/common/http';
import {Component, OnInit} from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LoginComponent } from "../Components/login/login.component";
import { NavbarComponent } from "../Components/navbar/navbar.component";
import { FooterComponent } from "../Components/footer/footer.component";
import { SpinnerComponent } from '../Components/spinner/spinner.component';
import { CommonModule } from '@angular/common';
import {initFacebookSDK} from "./utils/facebook-sdk-loader";


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, HttpClientModule, LoginComponent, NavbarComponent, FooterComponent,SpinnerComponent,CommonModule],

  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'FeedPulse';

  ngOnInit() {
    initFacebookSDK();
  }

}
