import { Component, CUSTOM_ELEMENTS_SCHEMA, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FacebookService } from '../../app/services/facebook.service';
import { FacebookPage } from '../../app/interfaces/Facebook_Page';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]  // ✅ Allow Custom Elements
})
export class DashboardComponent  implements OnInit{
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  userData: any = null;
  pages: FacebookPage[] = [];
  loading = false;
  errorMessage = '';
  isBrowser: boolean;
  constructor(private facebookService: FacebookService,
    @Inject(PLATFORM_ID) private platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }
  async ngOnInit(): Promise<void> {
    const token = localStorage.getItem('fb_access_token');
    const user = localStorage.getItem('fb_user_profile');
    console.log(token);
    console.log(user);

    if (token && user) {
      this.userData = JSON.parse(user);
      await this.fetchPages(token);
    }
  }
  async login() {
    this.loading = true;
    try {
      const authData = await this.facebookService.loginWithFacebook();
      localStorage.setItem('fb_access_token', authData.accessToken);
      console.log('✅ Auth Data:', authData);

      if (authData.authResponse) {
        const profile = await this.facebookService.getUserProfile();
        localStorage.setItem('fb_user_profile', JSON.stringify(profile));
        console.log('✅ Facebook Profile:', profile);
        this.userData = profile;
        const accessToken = authData.authResponse.accessToken;
        
                // 🌐 Fetch Pages
                this.facebookService.getFacebookPages(accessToken).subscribe({
                  next: (res) => {
                    if (res.succeeded&& res.data) {
                      this.pages = res.data;
                      
                      console.log('✅ Pages:', this.pages);
                    }
                  },
                  error: (err) => {
                    console.error('❌ Error fetching pages:', err);
                  }
                });
      }
    } catch (error) {
      console.error('❌ Login Error:', error);
    }
    this.loading = false;
  }
  async fetchPages(token: string): Promise<void> {
    try {
      this.facebookService.getFacebookPages(token).subscribe({
        next: (res) => {
          if(res.data)
          this.pages = res.data;
        },
        error: (err) => {
          this.errorMessage = 'Failed to fetch pages';
          console.error(err);
        },
      });
    } catch (error) {
      this.errorMessage = 'Error fetching pages';
      console.error(error);
    }
  }
}
