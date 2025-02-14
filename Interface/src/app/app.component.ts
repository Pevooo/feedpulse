import { HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import {RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LoginComponent } from "../Components/login/login.component";
import { NavbarComponent } from "../Components/navbar/navbar.component";
import { FooterComponent } from "../Components/footer/footer.component";


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive, HttpClientModule, LoginComponent, NavbarComponent, FooterComponent],

  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'adminDashboard';
}
