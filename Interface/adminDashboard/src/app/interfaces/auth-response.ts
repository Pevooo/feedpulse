export interface AuthResponse {
  "message": null;
  "isAuthenticated": true;
  "username": string;
  "email": string;
  "roles": [];
  "token": string;
  "expiresOn": string;
  "refreshTokenExpiration": string;
}
