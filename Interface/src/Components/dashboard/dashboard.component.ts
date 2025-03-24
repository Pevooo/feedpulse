import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FacebookService } from '../../app/services/facebook.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]  // ✅ Allow Custom Elements
})
export class DashboardComponent {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  userData: any = null;

  constructor(private facebookService: FacebookService) {}

  async login() {
    try {
      const authData = await this.facebookService.loginWithFacebook();
      console.log('✅ Auth Data:', authData);

      if (authData.authResponse) {
        const profile = await this.facebookService.getUserProfile();
        console.log('✅ Facebook Profile:', profile);
        this.userData = profile;
      }
    } catch (error) {
      console.error('❌ Login Error:', error);
    }
  }
}
