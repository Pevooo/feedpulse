import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import {  NgForm,ReactiveFormsModule, FormsModule } from '@angular/forms';
import { IRegistrationModel } from '../../app/interfaces/IRegisterModel';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../app/services/auth.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [RouterLink,RouterOutlet,CommonModule,ReactiveFormsModule,FormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent  {
  registration: IRegistrationModel = {
    fullName: '',
    userName: '',
    email: '',
    password: '',
    confirmPassword: '',
    country: '',
    address: '',
    phoneNumber: '',
    photo: undefined // Initialize as undefined instead of null
  };
  constructor(private http: HttpClient,private service:AuthService,private router:Router){
   
  }

  onSubmit(form: NgForm): void {
    console.log(this.registration);
    if (form.valid) {
      if (this.registration.password !== this.registration.confirmPassword) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Passwords do not match!'
        });
        return;
      }

      this.service.Register(this.registration).subscribe({
        next: (response) => {
          console.log(response);
          Swal.fire({
            icon: 'success',
            title: 'Registration Successful',
            text: 'Welcome! :) Confirm Your Account Via Email',
            timer: 1500,
            showConfirmButton: false
          }).then(() => {
            this.router.navigate(['/login']);
          });
        },
        error: (error) => {
          Swal.fire({
            icon: 'error',
            title: 'Registration Failed',
            text: error.message || 'Something went wrong!'
          });
        }
      });
    } else {
      Swal.fire({
        icon: 'warning',
        title: 'Invalid Form',
        text: 'Please fill all required fields correctly!'
      });
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onFileChange(event: any) {
    const file = event.target.files[0];
    if (file && this.isImageFile(file)) {
      this.registration.photo = file;
      console.log('File assigned:', this.registration.photo);
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Invalid File',
        text: 'Please upload a valid image file (jpeg, png, gif, webp)'
      });
      this.registration.photo = undefined; // Reset to undefined instead of null
    }
    console.log(this.registration);
  }

  isImageFile(file: File): boolean {
    const acceptedImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    return file && acceptedImageTypes.includes(file.type);
  }

  
}
