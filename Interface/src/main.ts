import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter } from '@angular/router'; // Import Router provider
import { AppComponent } from './app/app.component';
import { spinnerInterceptor } from './app/interceptors/spinner.interceptor';
import { routes } from './app/app.routes'; // Import your routes (we’ll create this next)

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(
      withInterceptors([spinnerInterceptor])
    ),
    provideRouter(routes) // Add Router with your routes
  ]
});