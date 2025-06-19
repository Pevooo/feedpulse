import { CommonModule } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  HostListener,
  OnDestroy,
} from '@angular/core';
import {
  NavigationEnd,
  Router,
  RouterLink,
  RouterLinkActive,
} from '@angular/router';

import { Subscription } from 'rxjs';

import { TranslateModule } from '@ngx-translate/core';

import { AuthService } from '../../app/services/auth.service';
import { LanguageService } from '../../app/services/language.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive, TranslateModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnDestroy {
  isScrolled = false;
  menuOpen = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.isScrolled = window.scrollY > 50; // Change 50 to any value you want
  }

  isLoggedIn = this.authService.isLoggedIn(); // Initialize with current state

  private routerSubscription: Subscription;


  constructor(
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private languageService: LanguageService
  ) {
    this.routerSubscription = this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.isLoggedIn = this.authService.isLoggedIn();
        this.cdr.detectChanges();
        console.log('Navigation occurred, isLoggedIn:', this.isLoggedIn);
      }
    });
  }

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.isScrolled = window.scrollY > 50;
  }

  ngOnDestroy(): void {
    this.routerSubscription.unsubscribe();
  }

  onLogout(event: Event): void {
    event.preventDefault();
    this.authService.logout();
    this.isLoggedIn = this.authService.isLoggedIn();
    this.cdr.detectChanges();
    this.router.navigate(['/login']);
  }



  switchLanguage(lang: string) {
    this.languageService.switchLang(lang);
  }

  toggleMenu() {
    this.menuOpen = !this.menuOpen;
  }
}
