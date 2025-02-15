import { Routes } from '@angular/router';
import { HomeComponent } from '../Components/home/home.component';

import { LoginComponent } from '../Components/login/login.component';
import { SignupComponent } from '../Components/signup/signup.component';
import { AboutComponent } from '../Components/about/about.component';
import { ServicesComponent } from '../Components/services/services.component';
import { ContactusComponent } from '../Components/contactus/contactus.component';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'about', component:AboutComponent },
  { path: 'login', component: LoginComponent },
  { path: 'services', component: ServicesComponent },
  { path: 'contact-us', component: ContactusComponent },
  { path: 'signup', component: SignupComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
];
