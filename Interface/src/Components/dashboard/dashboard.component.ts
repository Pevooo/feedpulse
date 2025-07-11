import {
  CommonModule,
  isPlatformBrowser,
} from '@angular/common';
import {
  Component,
  CUSTOM_ELEMENTS_SCHEMA,
  Inject,
  OnInit,
  PLATFORM_ID,
} from '@angular/core';
import { Router } from '@angular/router';

import { TranslateModule } from '@ngx-translate/core';

import { FacebookPage } from '../../app/interfaces/Facebook_Page';
import { FacebookService } from '../../app/services/facebook.service';
import { PageAnalyticsService } from '../../app/services/page-analytics.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule,TranslateModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]  // ✅ Allow Custom Elements
})
export class DashboardComponent implements OnInit{
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  userData: any = null;
  pages: FacebookPage[] = [];
  unregisteredPages:FacebookPage[]=[];
  registeredPages: FacebookPage[] = [];
  loading = false;
  errorMessage = '';
  isBrowser: boolean;
  isConnected = false;
  constructor(
    private facebookService: FacebookService,
    private router: Router,
    private pageAnalyticsService: PageAnalyticsService,
    @Inject(PLATFORM_ID) private platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }
  async ngOnInit(): Promise<void> {
    const token = localStorage.getItem('fb_access_token');
    const user = localStorage.getItem('fb_user_profile');
    if(token && user) {
      this.isConnected = true;
      this.facebookService.getFacebookPages(token).subscribe({
        next: (res) => {
          if (res.succeeded && res.data) {
            this.pages = res.data;
            this.userData = JSON.parse(user);
            this.calculateRegisteredPages();
            console.log('✅ Pages:', this.pages);
            console.log('✅ Unregister:', this.unregisteredPages);
            console.log('✅ Registered:', this.registeredPages);
          }
        },
        error: (err) => {
          this.facebookService.checkLoginStatus().then(response => {
            if (response.authResponse) {
              this.facebookService.getUserProfile().then(profile => {
                localStorage.setItem('fb_access_token', response.authResponse.accessToken);
                localStorage.setItem('fb_user_profile', JSON.stringify(profile));
                this.userData = profile;
                this.fetchPages(response.authResponse.accessToken);
                this.calculateRegisteredPages();
              });
            } else {
              this.userData = null;
              this.isConnected = false;
            }
          }).catch(() => {
            console.warn('User is not logged in.');
            console.error('❌ Error fetching pages:', err);
            this.userData = null;
            this.isConnected = false;
          });
        }
      });
    }
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
              console.log('✅ Unregistered:', this.unregisteredPages);
              console.log('✅ Registered:', this.registeredPages);
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
    this.registeredPages = [];
    this.unregisteredPages = [];
    this.isConnected = false;
    this.userData = null;
    localStorage.removeItem('fb_access_token');
    localStorage.removeItem('fb_user_profile');
  }

  goToAnalytics(page: FacebookPage) {
    const analyticsData = {
      facebookId: page.id,
      pageName: page.name,
      userId: this.userData?.id,
      accessToken: page.accessToken
    };
    
    // Set data in service (hidden from URL)
    this.pageAnalyticsService.setAnalyticsData(analyticsData);
    
    // Navigate without query parameters
    this.router.navigate(['/page-analytics']);
  }

  goToMockPage() {
    const analyticsData = {
      facebookId: "448242228374517",
      pageName: "Mock Page"
    };
    
    // Set data in service (hidden from URL)
    this.pageAnalyticsService.setAnalyticsData(analyticsData);
    
    // Navigate without query parameters
    this.router.navigate(['/page-analytics']);
  }

  private calculateRegisteredPages(): void {
    const unregisteredIds = new Set(this.unregisteredPages.map(p => p.id));
    this.registeredPages = this.pages.filter(p => !unregisteredIds.has(p.id));
  }
}
