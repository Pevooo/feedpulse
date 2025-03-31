

export interface IRegistrationModel {
    fullName: string;
    userName: string;
    email: string;
    password: string;
    confirmPassword: string;
    country: string; // Optional
    address: string; // Optional
    phoneNumber: string;
    photo?: File; // Optional (for file upload)
    }