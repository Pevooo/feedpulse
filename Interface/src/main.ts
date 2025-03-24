import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router'; // Import Router provider
import { AppComponent } from './app/app.component';
import { spinnerInterceptor } from './app/interceptors/spinner.interceptor';
import { routes } from './app/app.routes'; // Import your routes (we’ll create this next)
import { FacebookLoginProvider, SocialAuthServiceConfig } from '@abacritt/angularx-social-login';
import { provideAnimations } from '@angular/platform-browser/animations';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(
      withInterceptors([spinnerInterceptor])
    ),
    provideRouter(routes) ,// Add Router with your routes
    provideAnimations(),
    {
      provide: 'SocialAuthServiceConfig',
      useValue: {
        autoLogin: false,
        providers: [
          {
            id: FacebookLoginProvider.PROVIDER_ID,
            provider: new FacebookLoginProvider('1213236544138432', {
              scope: 'public_profile,email',
              return_scopes: true,
              enable_profile_selector: true
            })
          }
        ],
        onError: (err) => {
          console.error('Social Auth Error:', err);
        }
      } as SocialAuthServiceConfig}
  ]
});