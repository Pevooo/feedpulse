import { Component, OnDestroy, HostListener  } from '@angular/core';
import { AuthService } from '../../app/services/auth.service';
import { Router, NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnDestroy {
  isScrolled = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    this.isScrolled = window.scrollY > 50; // Change 50 to any value you want
  }

  isLoggedIn = this.authService.isLoggedIn(); // Initialize with current state
  private routerSubscription: Subscription;

  constructor(
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {
    // Subscribe to router events to update isLoggedIn on navigation
    this.routerSubscription = this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.isLoggedIn = this.authService.isLoggedIn();
        this.cdr.detectChanges();
        console.log('Navigation occurred, isLoggedIn:', this.isLoggedIn); // Debug log
      }
    });
  }

  ngOnDestroy(): void {
    this.routerSubscription.unsubscribe();
  }

  onLogout(event: Event): void {
    event.preventDefault();
    this.authService.logout();
    this.isLoggedIn = this.authService.isLoggedIn(); // Manually update after logout
    this.cdr.detectChanges();
    this.router.navigate(['/login']);
  }
}