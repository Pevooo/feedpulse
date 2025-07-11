import { Routes } from '@angular/router';
import { HomeComponent } from '../Components/home/home.component';

import { LoginComponent } from '../Components/login/login.component';
import { SignupComponent } from '../Components/signup/signup.component';
import { AboutComponent } from '../Components/about/about.component';
import { ServicesComponent } from '../Components/services/services.component';
import { ContactusComponent } from '../Components/contactus/contactus.component';
import { DashboardComponent } from '../Components/dashboard/dashboard.component';
import { AddOrganizationComponent } from '../Components/add-organization/add-organization.component';
import { PageAnalyticsComponent } from '../Components/page-analytics/page-analytics.component';
import { PrivacyPolicyComponent} from '../Components/privacy-policy/privacy-policy.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'about', component:AboutComponent },
  { path: 'login', component: LoginComponent },
  { path: 'services', component: ServicesComponent },
  { path: 'contact-us', component: ContactusComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'add-organization', component: AddOrganizationComponent, canActivate: [AuthGuard] },
  {path:'page-analytics',component:PageAnalyticsComponent, canActivate: [AuthGuard]},
  {path: 'privacy-policy', component: PrivacyPolicyComponent},
  { path: '', redirectTo: '/home', pathMatch: 'full' },
];
