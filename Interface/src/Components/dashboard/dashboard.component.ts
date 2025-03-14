import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FacebookService, LoginStatusResponse } from '../../app/services/facebook.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  isConnected = false;
  statusMessage = 'Please connect with Facebook';
  accessToken: string | null = null;

  constructor(private fbService: FacebookService) {}

  ngOnInit(): void {
    this.fbService.loadFacebookSDK()
      .then(() => this.checkLoginStatus())
      .catch((error) => {
        console.error('Failed to load Facebook SDK:', error);
        this.statusMessage = 'Error loading Facebook SDK';
      });
  }

  connectWithFacebook(): void {
    this.fbService.login()
      .then((response) => {
        this.handleLoginResponse(response);
      })
      .catch((error) => {
        console.error('Login failed:', error);
        // Provide a more specific message based on the error
        if (error.message === 'User cancelled login or did not fully authorize') {
          this.statusMessage = 'Login cancelled or permissions not granted. Please try again and accept the permissions.';
        } else {
          this.statusMessage = 'Login failed due to an unexpected error. Please try again.';
        }
      });
  }

  logout(): void {
    this.fbService.logout()
      .then((response) => {
        console.log('Logout Response:', response);
        this.isConnected = false;
        this.accessToken = null;
        this.statusMessage = 'Please connect with Facebook';
      })
      .catch((error) => {
        console.error('Logout failed:', error);
        this.statusMessage = 'Logout failed. Please try again.';
      });
  }

  private checkLoginStatus(): void {
    this.fbService.getLoginStatus()
      .then((response) => {
        this.handleLoginResponse(response);
      })
      .catch((error) => console.error('Status check failed:', error));
  }

  private handleLoginResponse(response:LoginStatusResponse): void {
    if (response.status === 'connected' && response.authResponse) {
      this.isConnected = true;
      this.accessToken = response.authResponse.accessToken;
      console.log('Access Token:', this.accessToken);
      this.fbService.getUserData()
        .then((userData) => {
          console.log('User Data (for reference):', userData);
          this.statusMessage = `Welcome, ${userData.name || 'User'}!`;
        })
        .catch((error) => {
          console.error('Failed to fetch user data:', error);
          this.statusMessage = 'Connected, but failed to fetch user data';
        });
    } else {
      this.isConnected = false;
      this.accessToken = null;
      this.statusMessage = 'Please connect with Facebook';
    }
  }
}