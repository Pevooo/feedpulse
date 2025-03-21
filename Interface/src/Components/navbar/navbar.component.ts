import { Component } from '@angular/core';
import {  Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../app/services/auth.service';
import Swal from 'sweetalert2';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLinkActive,RouterLink,CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  menuOpen: boolean;
  constructor(private authService:AuthService,private router:Router){
    this.menuOpen=false;
  }
  isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  onLogout(event: Event): void {
    event.preventDefault();
    Swal.fire({
      icon: 'warning',
      title: 'Are you sure?',
      text: 'You will be logged out.',
      showCancelButton: true,
      confirmButtonText: 'Yes, Logout',
      cancelButtonText: 'Cancel'
    }).then((result) => {
      if (result.isConfirmed) {
        this.authService.logout();
        this.router.navigate(['/login']);
        Swal.fire({
          icon: 'success',
          title: 'Logged Out',
          text: 'You have been logged out successfully.',
          timer: 1500,
          showConfirmButton: false
        });
      }
    });
    
  }
}