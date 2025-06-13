import { Component, CUSTOM_ELEMENTS_SCHEMA, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FacebookService } from '../../app/services/facebook.service';
import { FacebookPage } from '../../app/interfaces/Facebook_Page';
import { Router } from '@angular/router';
import { OrganizationService } from '../../app/services/organization.service';


@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]  // ✅ Allow Custom Elements
})
export class DashboardComponent implements OnInit{
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  userData: any = null;
  pages: FacebookPage[] = [];
  UnRegistered_Pages:FacebookPage[]=[];
  Registered_Pages: FacebookPage[] = [];
  loading = false;
  errorMessage = '';
  isBrowser: boolean;
  isConnected = false;
  constructor(
    private facebookService: FacebookService,
    private organizationService:OrganizationService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }
  async ngOnInit(): Promise<void> {
    const token = localStorage.getItem('fb_access_token');
    const user = localStorage.getItem('fb_user_profile');
    if(token && user){
      this.isConnected = true;
      this.facebookService.getFacebookPages(token).subscribe({
        next: (res) => {
          if (res.succeeded && res.data) {
            this.pages = res.data;
            this.isConnected = true;
            this.calculateRegisteredPages();
            console.log('✅ Pages:', this.pages);
            console.log('✅ Unregister:', this.UnRegistered_Pages);
            console.log('✅ Registered:', this.Registered_Pages);
          }
          },
        error: (err) => {
          this.isConnected = false;
          console.error('❌ Error fetching pages:', err);
        }
      });
    }

    console.log(token);
    console.log(user);

    if (token && user) {
      this.userData = JSON.parse(user);
      await this.fetchPages(token);
      this.calculateRegisteredPages();
    } else {
      // 🔄 Check login status again in case session exists
      this.facebookService.checkLoginStatus().then(response => {
        if (response.authResponse) {
          localStorage.setItem('fb_access_token', response.authResponse.accessToken);
          this.facebookService.getUserProfile().then(profile => {
            localStorage.setItem('fb_user_profile', JSON.stringify(profile));
            this.userData = profile;
            this.fetchPages(response.authResponse.accessToken);
            this.calculateRegisteredPages();
          });
        }
      }).catch(() => {
        console.warn('User is not logged in.');
      });
    }
    this.calculateRegisteredPages();
  }
  async login() {
    this.loading = true;
    try {
      const authData = await this.facebookService.loginWithFacebook();
      localStorage.setItem('fb_access_token', authData.authResponse.accessToken);
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
                    if (res.succeeded && res.data) {
                      this.pages = res.data;
                      this.isConnected = true;
                      this.calculateRegisteredPages();
                      console.log('✅ Pages:', this.pages);
                      console.log('✅ Unregisted:', this.UnRegistered_Pages);
                      console.log('✅ registerd:', this.Registered_Pages);
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
  goToForm(page: FacebookPage) {
    const userId = this.userData?.id;  // Get the logged-in user ID

    this.router.navigate(['/add-organization'], {
      queryParams: {
        name: page.name,
        pageAccessToken: page.accessToken, // Assuming this exists
        facebookId: page.id,
        userId: userId
      }
    });
  }

  logout() {
    this.facebookService.logout();
    this.pages = [];
    this.Registered_Pages = [];
    this.UnRegistered_Pages = [];
    this.isConnected = false;
  }

  goToAnalytics(page: FacebookPage) {
    const facebookId = page.id;
    console.log('Navigating to page-analytics with ID:', facebookId);
    this.router.navigate(['/page-analytics'], {
      queryParams: { facebookId }
    });
  }
  private calculateRegisteredPages(): void {
    const unregisteredIds = new Set(this.UnRegistered_Pages.map(p => p.id));
    this.Registered_Pages = this.pages.filter(p => !unregisteredIds.has(p.id));
  }
}
