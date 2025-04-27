export interface CustomJwtPayload {
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name': string;
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier': string;
    'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress': string;
    PhoneNumber: string;
    Id: string;
    'http://schemas.microsoft.com/ws/2008/06/identity/claims/role': string;
    exp: number;
    iss: string;
    aud: string;
  }